# coding: utf-8
from .defaultlist import DefaultList
from .linked import DoubleLinkedList
from .pagedlist import PagedList, chunk_sequence
from .sliceable import SliceableSequenceMixin
from .slicedview import SlicedView
from .structsequence import StructSequence
from .version import __version__

__author__ = "João S. O. Bueno"
__license__ = "LGPL v3.0+"

__all__ = [
    "DefaultList",
    "DoubleLinkedList",
    "PagedList",
    "SlicedView",
    "StructSequence",
    "SliceableSequenceMixin",
    "chunk_sequence",
    "__version__",
]

