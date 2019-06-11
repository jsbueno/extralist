from collections.abc import Sequence, MutableSequence

import pytest
from extralist.sliceable import SliceableSequenceMixin # SlicableMutableSequence


offset = 100
test_seq_size = 1000

@pytest.fixture
def sliceable_fixed_seq():
    class TestImutableSeq(SliceableSequenceMixin, Sequence):
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

    content = list(range(test_seq_size))
    data = TestImutableSeq(content)
    return content, data


@pytest.fixture
def sliceable_mutable_seq():
    class TestMutableSeq(SliceableSequenceMixin, Sequence):
        def __init__(self, data):
            self._data = list(data)

        def __getitem__(self, index):
            return self._data[index]

        def __setitem__(self, index, value):
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


def test_can_read_simple_itens(sliceable_fixed_seq):
    content, immutable_seq = sliceable_fixed_seq
    for i in range(len(content)):
        assert immutable_seq[i] == content[i]


@pytest.mark.parametrize("start,stop,step",[
    (0, 5, None),
    (None, None, None),
    (-5, None, None),
    (1,None,None),
    (None, None, 2),
    (None, None, -1),
])
def test_can_read_slices(sliceable_fixed_seq, start, stop, step):
    content, immutable_seq = sliceable_fixed_seq

    assert list(immutable_seq[start:stop:step]) == content[start:stop:step]


def test_returned_slice_same_class_as_parent(sliceable_fixed_seq):
    content, immutable_seq = sliceable_fixed_seq

    assert type(immutable_seq[:]) is type(immutable_seq)


def test_can_write_simple_itens(sliceable_mutable_seq):
    content, mutable_seq = sliceable_mutable_seq
    for i, val in enumerate(range(offset, offset + len(content))):
        mutable_seq[i] = val
    for val, stored in zip(range(offset, offset + len(content)), mutable_seq):
        assert val == stored


def test_can_change_same_size_slices(sliceable_mutable_seq):
    content, mutable_seq = sliceable_mutable_seq

    start = test_seq_size // 3
    stop = 2 * start

    mutable_seq[start:stop] = range(stop - start)

    for val, index in enumerate(range(start, stop)):
        assert mutable_seq[index] == val


def test_can_change_stepped_slices(sliceable_mutable_seq):
    content, mutable_seq = sliceable_mutable_seq

    start = test_seq_size // 3
    stop = 2 * start
    step = 3

    size1 = len(range(start, stop, step))

    mutable_seq[start:stop:step] = ["sentinel"] * size1

    cont = 0
    for index in range(len(seq)):
        if not cont % step and start <= index < stop:
            assert mutable_seq[index] == "sentinel"
        else:
            assert mutable_seq[index] == content[index]
        cont += 1


@pytest.mark.parametrize("factor", [
    0.2, 0.5, 0.8, 1, 1.2, 3, 5
])
def test_can_change_slices_for_different_sized_seqs(sliceable_mutable_seq, factor):
    content, mutable_seq = sliceable_mutable_seq

    start = test_seq_size // 3
    stop = 2 * start
    step = 3

    size1 = len(range(start, stop, 1))
    size2 = int(size1 * factor)
    new_content = ["sentinel"] * size2

    mutable_seq[start:stop] = new_content

    assert len(content) == len(mutable_seq) - size2 + size1
    assert all(content[i] == mutable_seq[i] for i in range(start))
    assert all(content[i] == mutable_seq[i] for i in range(len(content) -1, stop, -1))
    assert all(mutable_seq[i] == "sentinel" for i in range(start, start + size2))



def test_change_stepped_slices_with_different_sizes_should_fail(sliceable_mutable_seq):
    content, mutable_seq = sliceable_mutable_seq

    start = test_seq_size // 3
    stop = 2 * start
    step = 3


    size1 = len(range(start, stop, 1))
    with pytest.raises(ValueError):
        mutable_seq[start: stop: step] = range(start, stop)


def test_can_delete_slices(sliceable_mutable_seq):
    content, mutable_seq = sliceable_mutable_seq

    start = test_seq_size // 3
    stop = 2 * start

    del mutable_seq[start:stop]
    del content[start:stop]

    assert list(mutable_seq) == content


def test_can_delete_stepped_slices(sliceable_mutable_seq):
    content, mutable_seq = sliceable_mutable_seq

    start = test_seq_size // 3
    stop = 2 * start
    step = 3

    del mutable_seq[start:stop:step]
    del content[start:stop:step]

    assert list(mutable_seq) == content
