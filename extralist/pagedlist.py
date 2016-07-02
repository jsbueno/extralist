# coding: utf-8
# Author: João S. O. Bueno
# License: LGPL v 3.0
from __future__ import unicode_literals
from __future__ import division

import sys

import bisect

from functools import reduce

try:
    from collections.abc import MutableSequence
except ImportError:
    from collections import MutableSequence

try:
    range = xrange
except NameError:
    pass

def chunk_sequence(sequence, size):
    sequence = iter(sequence)
    while True:
        chunk = []
        try:
            for i in range(size):
                chunk.append(next(sequence))
        except StopIteration:
            break
        yield chunk
    if chunk:
        yield chunk


class DefaultList(list):
    def __init__(self, *args, default_factory=None):
        super(DefaultList, self).__init__(*args)
        self.default_factory = default_factory

    def __getitem__(self, attr):
        try:
            return super(DefaultList, self).__getitem__(attr)
        except IndexError:
            return self.default_factory()

class Page(object):
    __slots__ = "start end data".split()

def _empty_page():
    p = Page()
    p.start = p.end = 0
    p.data = []
    return p

class PagedList(MutableSequence):
    """
    Sequence designed for high performance inserting/deleting of elements in the middle

    Python's list and other stdlib sequence types by default need a sequence of objects -
    so there is no easy sequence that allows arbitrary insertion or erasing of items
    in the middle of the body without a huge performance cost, as any insertion or
    deleting implies copying over all the remaining elements of the sequence to another
    position.

    PagedList amortizes that by holding several "pages" with sequence parts, so that each
    insertion only affects one page at a time.

    """

    # Change this to True on an instance if slices should be PagedList -
    # otherwise they will be unpaged.

    slice_to_paged = False

    _lock_pagesize = False

    def __init__(self, sequence=None, pagesize=1000, page_class=list):
        self._reset(pagesize, page_class)
        self._fill(sequence)

    def _reset(self, pagesize, page_class):
        self.pagesize = pagesize
        self.page_class = page_class
        # DefaultList is used because when computing slices that extend to
        # self.END the page number will be one more than the actual existing pages.
        # (and len(self.pages) is super-usefull to keep track of the actual number of
        # pages
        self.pages = DefaultList(default_factory=_empty_page)
        self._dirt_log = []

    @classmethod
    def _from_pages(cls, pages, pagesize, page_class):
        self = cls.__new__(cls)
        self._reset(pagesize, page_class)
        for i, page in enumerate(pages):
            self._append_page(page)
            if len(page) != pagesize:
                self._dirt_log.append([i, len(page) - pagesize])
        return self

    @property
    def pagesize(self):
        return self._pagesize

    @pagesize.setter
    def pagesize(self, value):
        if not self._lock_pagesize:
            self._pagesize = value
            self._lock_pagesize = True
            return
        raise RuntimeError("Pagesize for {} can't be changed after instantiation".format(self.__class__.__name__))

    def _fill(self, sequence):
        if not hasattr(sequence, "__len__"):
            for chunk in chunk_sequence(sequence, self.pagesize):
                self._append_page(self.page_class(chunk))
            return
        for page_start in range(0, len(sequence), self.pagesize):
            self._append_page(self.page_class(sequence[page_start: page_start + self.pagesize]))

    def _append_page(self, chunk):
        page = Page()
        page.start = len(self.pages) * self.pagesize
        page.data = chunk
        self.pages.append(page)

    def _adjust_dirt(self, page_number, amount):
        dirt_record = bisect.bisect_left(self._dirt_log, [page_number, -sys.maxsize])
        if len(self._dirt_log) <= dirt_record or not self._dirt_log[dirt_record][0] == page_number:
            bisect.insort(self._dirt_log, [page_number, amount])
        else:
            self._dirt_log[dirt_record][1] += amount
            if self._dirt_log[dirt_record][1] == 0:
                del self._dirt_log[dirt_record]

    def _local_offset(self, page_number):
        dirt_record = bisect.bisect_left(self._dirt_log, [page_number, -sys.maxsize])
        if len(self._dirt_log) <= dirt_record or not self._dirt_log[dirt_record][0] == page_number:
            return 0
        return self._dirt_log[dirt_record][1]

    def _get_indexes(self, index):
        page_number= index // self.pagesize
        if not self._dirt_log:
            return page_number,  index % self.pagesize

        while True:
            # TODO: optimize this by enabling relative offset seeks:
            page_offset = self._get_offset_for_page(page_number)

            element_index = (index - page_offset) - (page_number * self.pagesize)
            if 0 <= element_index < self.pagesize + self._local_offset(page_number):
                break
            if element_index < 0:
                page_number -= 1
                if page_number < 0:
                    raise IndexError
            else:
                page_number += 1
        return page_number, element_index

    def _get_offset_for_page(self, page_number):
        offset = 0
        for dirt in self._dirt_log:
            if dirt[0] >= page_number:
                break
            offset += dirt[1]
        return offset

    def _get_slice_interval(self, slice_):
        s_start, s_stop, s_step = slice_.indices(len(self))
        s_stop = s_start + (s_stop - s_start) - (s_stop - s_start) % s_step

        lower_page, start_index = self._get_indexes(s_start)
        upper_page, end_index = self._get_indexes(s_stop)
        middle_pages = list(range(lower_page + 1, upper_page))

        return lower_page, start_index, middle_pages, upper_page, end_index

    def __getitem__(self, index):
        if isinstance(index, slice):
            if index.step is not None and index.step != 1:
                result_generator = (self[i] for i in range(*index.indices(len(self))))
                return (
                    self.__class__(result_generator, pagesize=self.pagesize, page_class=self.page_class)
                        if self.slice_to_paged else
                    self.page_class(result_generator)
                )
            lower_page, start_index, middle_pages, upper_page, end_index = self._get_slice_interval(index)
            if not self.slice_to_paged:
                if lower_page < upper_page:
                    result_slice = reduce(lambda prev, next: prev + next,
                                    (self.pages[i].data for i in middle_pages),
                                    self.pages[lower_page].data[start_index:]
                    ) + self.pages[upper_page].data[:end_index]
                else:
                    result_slice = self.pages[lower_page].data[start_index: end_index]

                return result_slice if self.page_class is list else self.page_class(result_slice)
            if lower_page < upper_page:
                return (self.__class__._from_pages((
                        [self.pages[lower_page].data[start_index:]] +
                        [self.pages[i].data[:] for i in middle_pages] +
                        [self.pages[upper_page].data[:end_index] ]
                    ),
                    pagesize = self.pagesize,
                    page_class = self.page_class
                ))
            else:
                return self._class(
                    self.pages[lower_page].data[start_index: end_index],
                    pagesize = self.pagesize,
                    page_class = self.page_class
                )

        if index < 0:
            index += len(self)
        page_number, page_index = self._get_indexes(index)
        return self.pages[page_number].data[page_index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            if not hasattr(value, "__len__"):
                value = list(value)
            if index.step is None or index.step == 1:
                lower_page, start_index, middle_pages, upper_page, end_index = self._get_slice_interval(index)
                # TODO :specialize if value is instance of PagedList
                if len(value) <= self.pagesize:
                    if lower_page == upper_page:
                        self.pages[lower_page].data[start_index: end_index] = value
                        self._adjust_dirt(lower_page, len(value) - (end_index - start_index))
                        return
                    # just extend the lower page with value and remove
                    # the remaining pages/values
                    raise NotImplementedError("Cross page insertion for small pages")
                else:
                    raise NotImplementedError("Cross page insertion for large pages")
                    pass
                    # split value in pages of self.pagesize lenght
                    # append

            else:
                all_indices = range(*index.indices(len(self)))
                if not hasattr(value, "__len__"):
                    value = list(value)
                if len(all_indices) != len(value):
                    raise ValueError(
                        "attempt to assign sequence of size {} to extended slice of size {}".format(
                        len(value), len(all_indices))
                    )
                for i, v in zip(all_indices, value):
                    self[i] = v
                return

        if index < 0:
            index += len(self)
        page_number, page_index = self._get_indexes(index)
        self.pages[page_number].data[page_index] = value

    def __delitem__(self, index):
        if isinstance(index, slice):
            raise NotImplementedError()
        page_number, page_index = self._get_indexes(index)
        del self.pages[page_number].data[page_index]
        self._adjust_dirt(page_number, -1)

    def __len__(self):
        last_page_number = len(self.pages) - 1
        return self.pagesize * last_page_number + len(self.pages[-1].data) + self._get_offset_for_page(last_page_number)

    def insert(self, index, value):
        page_number, page_index = self._get_indexes(index)
        self.pages[page_number].data.insert(page_index, value)
        self._adjust_dirt(page_number, +1)


