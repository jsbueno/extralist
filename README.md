Extra Sequence Types and Helpers
================================


## PagedList

A paged mutable sequence designed
not to suffer heavy performance its when elements must be deleted
or inserted inside a large sequence.

From an initializer sequence, the data is split in pages, each with
`pagesize` size. By default the data type of pages is a Python list.
From them on, all insertion or deletion happens on the individual pages
and PagedList keeps track of pages size changes - so that it can always
retrieve the correct values for the contained sequence.

Important: "pagesize" is not an absolute page size - it rather is an
indication of desired page size - insertions and deletions can change
individual pages to be larger or smaller than this amount.
Insertions made through slicing (`x[5:15] = range(100)`) will
respect maximum page size if the slice cross a page boundary -
but not otherwise.

[WIP] At this point of the implementation, for a   10_000_000 sized sequence, using page_size = 10000
there is a 250 fold __gain__ (25000%) in deleting consecutive elements one by one, and a 40 fold
(36700%) performance __loss__ in random acess reading to elements on the same sequence afterwards.

[WIP] getitem slice and negative indexes handling implemented


## DefaultList
    A DefaultDict analogue class

## LinkedList
    Linked list implementation of mutable sequence

## SlicedView
    Returns slices of a larger sequence as an inplace window to the
    main sequence, instead of copies.
    (If you need that before it is done here, check the ListView implementation
     at https://github.com/lhc/lhcpython/blob/master/tree.py for now)

## Future
Planned helpers/sequence types to be featured here:



### SliceableMutableSequence
    Like collections.abc.MutableSequence but automatically handles
    slices for your `__getitem__`, `__setitem__`, `__delitem__` methods
    if they support integer indexes. (The stdlib's version requires one to
    support both integer indexes and slices for these methods). It should also
    handle negative indexes properly.

### SomeTreeishSequence
    Some Tree Based Sequence  :-)


