from collections.abc import Sequence, MutableSequence

import pytest
from extralist.slicable import SlicableSequenceMixin # SlicableMutableSequence

@pytest.fixture
def slicable_fixed_seq():
    class TestImutableSeq(SlicableSequenceMixin, Sequence):
        def __init__(self, data):
            self._data = tuple(data)

        def __getitem__(self, index):
            return self._data[index]

        def __len__(self):
            return len(self._data)

        def __hash__(self):
            if not hasattr(self, "hash"):
                self.hash = hash(self.__dict__["_data"])
            return self.hash

    content = list(range(10))
    data = TestImutableSeq(content)
    return content, data


@pytest.fixture
def slicable_mutable_seq():
    class TestMutableSeq(SlicableSequenceMixin, Sequence):
        def __init__(self, data):
            self._data = tuple(data)

        def __getitem__(self, index):
            return self._data[index]

        def __setiem__(self, index, value):
            self._data[index] = value

        def __delitem__(self, index):
            del self._data[index]

        def insert(self, index, value):
            self._data.insert(index, value)

        def __len__(self):
            return len(self._data)


    content = list(range(10))
    data = TestMutableSeq(content)
    return content, data


def test_can_read_simple_itens(slicable_fixed_seq):
    content, imutable_seq = slicable_fixed_seq
    for i in range(len(content)):
        assert imutable_seq[i] == content[i]


@pytest.mark.parametrize("start,stop,step",[
    (0, 5, None),
    (None, None, None),
    (-5, None, None),
    (1,None,None),
    (None, None, 2),
    (None, None, -1),
])
def test_can_read_slices(slicable_fixed_seq, start, stop, step):
    content, imutable_seq = slicable_fixed_seq

    assert imutable_seq[start:stop:step] == content[start:stop:step]


def test_can_write_simple_itens(slicable_mutable_seq):
    content, mutable_seq = slicable_mutable_seq
    for i, val in enumerate(range(100, 100 + len(content))):
        mutable_seq[i] = val
    for val, stored in zip(range(100, 100 + len(content)), mutable_seq):
        assert val == stored
