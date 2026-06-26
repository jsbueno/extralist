"""Tests for extralist.StructSequence."""

import pytest

from extralist import StructSequence


def _points():
    return StructSequence("Point", ("x", "y"), "=ii")


def test_append_and_len():
    s = _points()
    s.append((1, 2))
    s.append((3, 4))
    assert len(s) == 2


def test_getitem_field_access():
    s = _points()
    s.append((1, 2))
    item = s[0]
    assert item.x == 1
    assert item.y == 2


def test_setitem_replaces_record():
    s = _points()
    s.append((1, 2))
    s[0] = (9, 8)
    assert s[0].x == 9
    assert s[0].y == 8


def test_field_setattr_writes_through():
    s = _points()
    s.append((1, 2))
    s[0].x = 7
    assert s[0].x == 7
    assert s[0].y == 2


def test_field_names_from_string():
    s = StructSequence("Point", "x y", "=ii")
    s.append((0, 1))
    assert s.field_names == ("x", "y")
    assert s[0].y == 1


def test_delitem_not_implemented():
    s = _points()
    s.append((0, 0))
    with pytest.raises(NotImplementedError):
        del s[0]


def test_insert_not_implemented():
    s = _points()
    s.append((0, 0))
    with pytest.raises(NotImplementedError):
        s.insert(0, (1, 1))


def test_repr_contains_name_and_length():
    s = _points()
    s.append((1, 2))
    text = repr(s)
    assert "Point" in text
    assert "1" in text
