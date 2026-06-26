"""Tests for extralist.SlicedView."""

import pytest

from extralist import SlicedView


def test_full_view_over_sequence():
    data = list(range(5))
    v = SlicedView(data)
    assert len(v) == 5
    assert list(v) == data


def test_window_view_scalar_get_and_set_aliases_parent():
    data = list(range(20))
    v = SlicedView(data, slice(5, 15))
    assert len(v) == 10
    assert v[0] == 5
    assert v[9] == 14
    v[0] = 99
    assert data[5] == 99
    data[6] = 77
    assert v[1] == 77


def test_constructor_accepts_start_stop_step_tuple():
    data = list(range(10))
    v = SlicedView(data, (2, 8, 2))
    assert list(v) == [2, 4, 6]


def test_nested_slice_returns_sliced_view_on_same_data_object():
    data = list(range(20))
    v = SlicedView(data, slice(5, 15))
    v2 = v[1:4]
    assert type(v2) is SlicedView
    assert v2.data is data


def test_negative_index_raises_not_implemented():
    v = SlicedView(list(range(5)))
    with pytest.raises(NotImplementedError, match="negative"):
        _ = v[-1]
    with pytest.raises(NotImplementedError, match="negative"):
        v[-1] = 0


def test_slice_assignment_raises_not_implemented():
    v = SlicedView(list(range(5)))
    with pytest.raises(NotImplementedError, match="slice"):
        v[1:3] = [8, 9]


def test_scalar_delete_updates_parent_and_shortens_view():
    data = [0, 1, 2, 3, 4, 5]
    v = SlicedView(data, slice(2, 5))
    assert list(v) == [2, 3, 4]
    del v[1]
    assert 3 not in data
    assert len(v) == 2


def test_insert_into_view_updates_parent():
    data = [0, 1, 2, 3, 4, 5]
    v = SlicedView(data, slice(2, 5))
    v.insert(1, 99)
    assert data[3] == 99
    assert len(v) == 4


def test_insert_out_of_range_raises():
    v = SlicedView([0, 1, 2], slice(0, 2))
    with pytest.raises(IndexError):
        v.insert(5, 1)


def test_empty_underlying_relative_to_start():
    data = []
    v = SlicedView(data, slice(0, 5))
    assert len(v) == 0
    assert list(v) == []
