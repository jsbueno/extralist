"""
Ordinary things that should work for all sequences,
regardless of extra properties they have.
"""

import pytest

from extralist import DoubleLinkedList, PagedList, DefaultList, SlicedView

sequences = [list, DoubleLinkedList, DefaultList, PagedList, SlicedView]

@pytest.mark.parametrize("sequence", sequences)
def test_create_new_seq_from_other_seq_preserve_elements(sequence):
    data = sequence(list(range(20)))
    assert len(data) == 20
    assert list(data) == list(range(20))


