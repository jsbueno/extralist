Extra Sequence Types and Helpers
================================


## PagedList

A paged mutable sequence designed
not to suffer heavy performance its when elements must be deleted
or inserted inside a large sequence.

From an initializer sequence, the data is split in pages, each with
`pagesize` size. By default the data type of pages is a Python list.
From them on, all insetion or deletion happens on the individual pages
and PagedList keeps track of pages size changes - so that it can always
retrieve the correct values for the coinained sequence.

[WIP] The PagedList API is under construction right now, and does not
work with slices yet.
[WIP] At this point of the implementation, for a   10_000_000 sized sequence, using page_size = 10000
there is a 250 fold __gain__ (25000%) in deleting consecutive elements one by one, and a 40 fold
(36700%) performance __loss__ in random acess reading to elements on the same sequence afterwards.

[WIP] getitem slice and negative indexes handling implemented

## Future
Planned helpers/sequence types to be featured here:

### SequenceWindow
    Returns slices of a larger sequence as an inplace window to the
    main sequence, instead of copies.
    (If you need that before it is done here, check the ListView implementation
     at https://github.com/lhc/lhcpython/blob/master/tree.py for now)

### SliceableMutableSequence
    Like collections.abc.MutableSequence but automatically handles
    slices for your `__getitem__`, `__setitem__`, `__delitem__` methods
    if they support integer indexes. (The stdlib's version requires one to
    support both integer indexes and slices for these methods). It should also
    handle negative indexes properly.



