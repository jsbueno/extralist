"""Tests for extralist.DefaultList."""

import pytest

from extralist import DefaultList


def test_create_from_iterable_preserves_elements():
    d = DefaultList([1, 2, 3])
    assert list(d) == [1, 2, 3]
    assert len(d) == 3


def test_in_range_getitem_behaves_like_list():
    d = DefaultList(["a", "b"])
    assert d[0] == "a"
    assert d[1] == "b"
    assert d[-1] == "b"


def test_past_end_without_append_returns_factory_result_and_does_not_grow():
    seen = []

    def factory(index):
        seen.append(index)
        return f"gen-{index}"

    d = DefaultList([0], default_factory=factory, append_on_extra=False)
    assert d[5] == "gen-5"
    assert seen == [5]
    assert len(d) == 1
    assert list(d) == [0]


def test_default_factory_none_when_omitted():
    d = DefaultList()
    assert d[0] is None
    assert len(d) == 0


def test_factory_without_parameters():
    d = DefaultList(default_factory=lambda: "constant", append_on_extra=False)
    assert d[2] == "constant"
    assert len(d) == 0


def test_append_on_extra_fills_intermediate_indices():
    d = DefaultList(default_factory=lambda i: i * 10, append_on_extra=True)
    assert d[3] == 30
    assert list(d) == [0, 10, 20, 30]
    assert len(d) == 4


def test_append_on_extra_negative_index_raises():
    d = DefaultList(default_factory=lambda: 0, append_on_extra=True)
    with pytest.raises(IndexError, match="negative"):
        _ = d[-1]


def test_append_on_extra_false_negative_past_range_uses_list_semantics():
    d = DefaultList([10, 20], append_on_extra=False)
    assert d[-1] == 20


def test_mutation_methods_from_list():
    d = DefaultList([1])
    d.append(2)
    d.insert(0, 0)
    assert list(d) == [0, 1, 2]
    del d[1]
    assert list(d) == [0, 2]
