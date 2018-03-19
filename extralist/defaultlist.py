# coding: utf-8
# Author: João S. O. Bueno
# License: LGPL v 3.0
from inspect import signature


class DefaultList(list):
    """
    Analogue to 'collections.defaultdict',
    ======================================

    this allows one to fetch an item past the sequence length,
    retrieving an element produced by a passed in factory at
    instantiation time.

    Unlike defaultdict, produced values are just returned, not created
    and added to the list, unless 'append_on_extra_ is passed = True.
    The reason being all intermediate values
    between the current list length and the requested missing index
    would have to be filled.

    The factory function may have
    a single parameter, in which case the requested index
    is passed. If no factory function is passed, a
    "None" producing factory is used by default.
    """

    def __init__(self, *args, default_factory=None, append_on_extra=False):
        super(DefaultList, self).__init__(*args)
        if default_factory is None:
            default_factory = lambda i: None
        self.default_factory = default_factory
        self.takes_index = bool(signature(default_factory).parameters)

    def __getitem__(self, index):
        try:
            return super(DefaultList, self).__getitem__(index)
        except IndexError:
            if index < 0:
                raise IndexError("Can't create default element at negative index")
            for i in range(len(self), index + 1):
                new = self.default_factory(*((i,) if self.takes_index else ()))
                self.append(new)
            return new

