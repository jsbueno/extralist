"""Tests for extralist.chunk_sequence."""

from extralist import chunk_sequence


def test_chunk_sequence_splits_with_partial_last_chunk():
    assert list(chunk_sequence(range(10), 4)) == [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9],
    ]


def test_chunk_sequence_exact_multiple():
    assert list(chunk_sequence(range(8), 4)) == [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
    ]


def test_chunk_sequence_empty_input():
    assert list(chunk_sequence([], 3)) == []


def test_chunk_sequence_size_one():
    assert list(chunk_sequence("ab", 1)) == [["a"], ["b"]]


def test_chunk_sequence_accepts_iterator():
    assert list(chunk_sequence(iter([1, 2, 3, 4, 5]), 2)) == [[1, 2], [3, 4], [5]]
