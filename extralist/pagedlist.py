# coding: utf-8
# Author: João S. O. Bueno
# License: LGPL v 3.0
from __future__ import unicode_literals
from __future__ import division

import bisect

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
    if ch:
        yield chunk




class Page(object):
    __slots__ = "start end data".split()
    
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
    _lock_pagesize = False
    def __init__(self, sequence=None, pagesize=1000):
        self.pagesize = pagesize
        self.pages = []
        self._fill(sequence)
        self._dirt_log = [] 

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
                self._append_page(page)
            return
        for page_start in range(0, len(sequence), self.pagesize):
            self._append_page(sequence[page_start: page_start + self.pagesize])
    
    def _append_page(self, chunk):
        page = Page()
        page.start = len(self.pages) * self.pagesize
        page.data = chunk
        self.pages.append(page)

    def _adjust_dirt(self, page_number, amount):
        dirt_record = bisect.bisect_left(self._dirt_log, page_number)
        if not self._dirt_log or not self._dirt_log[dirt_record][0] == page_number:
            bisect.insort(self._dirt_log, [page_number, amount])
        else:
            self._dirt_log[dirt_record][1] += amount
            if self._dirt_log[dirt_record][1] == 0:
                del self._dirt_log[dirt_record]

    def _local_offset(self, page_number):
        dirt_record = bisect.bisect_left(self._dirt_log, page_number)
        if not self._dirt_log or not self._dirt_log[dirt_record][0] == page_number:
            return 0
        return self._dirt_log[dirt_record][1]

    def _get_indexes(self, index):
        if not self._dirt_log:
            return index // self.pagesize, index % self.pagesize

        page_number= index // self.pagesize

        while True:
            # TODO: optimize this by enabling relative offset seeks:
            page_offset = self._get_offset_for_page(page_number)

            element_index = (index - page_offset) % (page_number * self.pagesize)
            if 0 <= element_index < self.pagesize + self._local_offset(page_number):
                break
            if element_index < 0:
                page_number -= 1
                if page_number < 0:
                    raise IndexError
            else:
                page_number += 1
                if page_number >= len(self.pages):
                    page_number -= 1 
                    break

        return page_number, element_index

    def _get_offset_for_page(self, page_number):
        offset = 0
        for dirt in self._dirt_log:
            if dirt[0] >= page_number:
                break
            offset += dirt[1]
        return offset
        

    def __getitem__(self, index):
        if isinstance(index, slice):
            raise NotImplementedError()
        page_number, page_index = self._get_indexes(index)
        return self.pages[page_number].data[page_index]


    def __setitem__(self, index, value):
        if isinstance(index, slice):
            raise NotImplementedError()
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

            
