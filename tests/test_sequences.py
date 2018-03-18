import pytest

from extralist import DoubleLinkedList, PagedList

sequences = [list, DoubleLinkedList, PagedList]

@pytest.mark.parametrize("sequence", sequences)
def test_create_new_seq_from_iterable_preserve_elements(sequence):
    data = sequence(iter(range(20)))
    assert len(data) == 20
    assert list(data) == list(range(20))


