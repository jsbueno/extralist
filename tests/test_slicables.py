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


def test_can_read_slices(slicable_fixed_seq):
    content, imutable_seq = slicable_fixed_seq

    assert imutable_seq[0:5] == content[0:5]
    assert imutable_seq[:] == content[:]
    assert imutable_seq[-5:] == content[-5:]
    assert imutable_seq[1] == content[1]
