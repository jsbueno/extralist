"""
Ordinary things that should work for all sequences,
regardless of extra properties they have.
"""

import pytest
import random
import warnings

from extralist import DefaultList, DoubleLinkedList, PagedList, SlicedView

SAMPLE_LENGTH = 500


def _get_sample():
    return list(range(SAMPLE_LENGTH))


def _paged_small(seq):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return PagedList(seq, pagesize=5)


def _double_linked(seq):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return DoubleLinkedList(seq)


def _paged_default(seq):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return PagedList(seq)


# Shared mutable-sequence smoke tests for exported sequence types (+ list control).
sequences = [
    list,
    DefaultList,
    SlicedView,
    _double_linked,
    _paged_small,
    _paged_default,
]


@pytest.mark.parametrize("sequence", sequences)
def test_create_new_seq_from_other_seq_preserve_elements(sequence):
    data = sequence(_get_sample())
    assert len(data) == SAMPLE_LENGTH
    assert list(data) == _get_sample()


@pytest.mark.parametrize("sequence", sequences)
def test_create_sequence_can_delete_elements(sequence):
    data = sequence(_get_sample())
    control = _get_sample()
    random.seed(0)
    for _ in range(SAMPLE_LENGTH):
        i = random.randrange(0, len(data))
        del data[i]
        del control[i]
        assert list(data) == control


@pytest.mark.parametrize("sequence", sequences)
def test_create_sequence_can_append_elements(sequence):
    data = sequence(_get_sample())
    control = _get_sample()
    random.seed(0)
    for i in range(SAMPLE_LENGTH):
        i += SAMPLE_LENGTH
        data.append(i)
        control.append(i)
        assert list(data) == control


@pytest.mark.parametrize("sequence", sequences)
def test_create_sequence_can_insert_elements_at_0(sequence):
    data = sequence(_get_sample())
    control = _get_sample()
    random.seed(0)
    for i in range(SAMPLE_LENGTH):
        i += SAMPLE_LENGTH
        data.insert(0, i)
        control.insert(0, i)
        assert list(data) == control


@pytest.mark.parametrize("sequence", sequences)
def test_create_sequence_can_insert_elements_at_random(sequence):
    data = sequence(_get_sample())
    control = _get_sample()
    random.seed(0)
    for j in range(SAMPLE_LENGTH // 10):
        i = random.randrange(0, SAMPLE_LENGTH)
        data.insert(i, j)
        control.insert(i, j)
        assert list(data) == control



