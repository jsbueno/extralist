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
    and added to the list. The reason being all intermediate values
    between the current list length and the requested missing index
    would have to be filled.

    The factory function may have
    a single parameter, in which case the requested index
    is passed. If no factory function is passed, a
    "None" producing factory is used by default.
    """

    def __init__(self, *args, default_factory=None):
        super(DefaultList, self).__init__(*args)
        if default_factory is None:
            default_factory = lambda i: None
        self.default_factory = default_factory
        self.takes_index = bool(signature(default_factory).parameters)

    def __getitem__(self, attr):
        try:
            return super(DefaultList, self).__getitem__(attr)
        except IndexError:
            if self.takes_index:
                return self.default_factory(index)
            else:
                return self.default_factory()

