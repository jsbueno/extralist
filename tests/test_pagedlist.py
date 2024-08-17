import pytest
from extralist import PagedList

def test_single_item_access():
    x = PagedList(list(range(100)), 10)
    assert x[0] == 0
    assert x[99] == 99
    with pytest.raises(IndexError):
        x[100]
    assert x[35] == 35

def test_single_item_deletion():
    x = PagedList(list(range(100)), 10)
    del x[35]
    assert x[35] == 36
    assert x[39] == 40
    assert x[49] == 50
    assert x[98] == 99
    with pytest.raises(IndexError):
        x[99]

def test_single_item_insertion():
    x = PagedList(list(range(100)), 10)
    x.insert(48, "bla")
    assert x[48] == "bla"
    assert x[49] == 49
    assert x[50] == 50
    x.insert(48, "ble")
    assert x[50] == 49

def test_slice_access():
    x = PagedList(range(100), 10)
    y = x[25:35]
    assert list(y) == [25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
    assert y.__class__ is list
    y = x[0:15:4]
    assert list(y) == [0, 4, 8, 12]

def test_slice_deletion():
    x = PagedList(range(100), 10)
    del x[98]
    assert list(x[-5:]) == [94, 95, 96, 97, 99]
    del x[88]
    assert list(x[-15:]) == [83, 84, 85, 86, 87, 89, 90, 91, 92, 93, 94, 95, 96, 97, 99]

def test_slice_insertion():
    x = PagedList(range(100), 10)
    x[12:15] = range(9)  # intra_page slice insertion
    assert x[:30] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    x[5:12] = range(200, 220)
    assert list(x[:35]) == [0, 1, 2, 3, 4, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

def test_slice_assignment():
    x = PagedList(range(100), 10)
    x[12:15] = range(9)
    assert x[:30] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23]

def test_length():
    x = PagedList(range(100), 10)
    x[:] = []
    assert len(x) == 0
    assert len(x.pages) == 2
    assert len(x.pages[0].data) == 0
    x[5:15] = range(30)
    assert len(x) == 120
    assert len(x.pages) == 12
    x[5:35] = range(100, 160)
    assert len(x) == 130
    assert len(x.pages) == 13
    assert len(x.pages[0].data) == 10
    x[5:85] = range(100, 110)
    assert len(x) == 30

def test_emptying_the_list():
    x = PagedList(range(100), 10)
    del x[:]
    assert len(x) == 0
    assert list(x) == []

def test_slicing_with_negative_indices():
    x = PagedList(range(100), 10)
    assert x[-5] == 95
    y = x[-5:]
    assert list(y) == [95, 96, 97, 98, 99]

def test_slicing_with_step():
    x = PagedList(range(100), 10)
    y = x[0:15:4]
    assert list(y) == [0, 4, 8, 12]

def test_slicing_with_slice_to_paged_true():
    x = PagedList(range(100), 10)
    x.slice_to_paged = True
    y = x[25:35]
    assert list(y) == [25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
    assert y.pagesize == 10
    del y[5]
    assert list(y) == [25, 26, 27, 28, 29, 31, 32, 33, 34]
    assert y[5] == 31
    assert y[4] == 29
    assert x[30] == 30
    y = x[0:15:4]
    assert list(y) == [0, 4, 8, 12]
    assert x[-5] == 95
    y = x[-5:]
    assert list(y) == [95, 96, 97, 98, 99]
    del x[98]
    assert list(x[-5:]) == [94, 95, 96, 97, 99]
    del x[88]
    assert list(x[-15:]) == [83, 84, 85, 86, 87, 89, 90, 91, 92, 93, 94, 95, 96, 97, 99]

def test_slicing_with_slice_to_paged_false():
    x = PagedList(range(100), 10)
    x.slice_to_paged = False
    y = x
