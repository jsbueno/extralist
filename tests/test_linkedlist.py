from extralist.linked import DoubleLinkedList


def test_create():
    d = DoubleLinkedList()
    assert (len(d)) == 0


def test_create_with_range():
    d = DoubleLinkedList(range(5))
    assert (len(d)) == 5
    assert list(d) == list(range(5))


def test_create_with_list():
    d = DoubleLinkedList([0, 1, 2])
    assert (len(d)) == 3
    assert list(d) == [0, 1, 2]


def test_insert_on_empty():
    d = DoubleLinkedList()
    d.insert(0, 1)
    assert (len(d)) == 1
    assert d[0] == 1


def test_insert_on_position_0():
    d = DoubleLinkedList([1])
    d.insert(0, 0)
    print("\n", d, "\n")
    assert (len(d)) == 2
    assert d[0] == 0
    assert list(d) == [0, 1]


def test_insert_on_position_0_larger():
    d = DoubleLinkedList([1, 2])
    d.insert(0, 0)
    assert (len(d)) == 3
    assert d[0] == 0
    assert list(d) == [0, 1, 2]


def test_insert_on_position_0():
    d = DoubleLinkedList([1])
    d.insert(0, 0)
    assert (len(d)) == 2
    assert d[0] == 0
    assert list(d) == [0, 1]


def test_insert_on_position_1():
    d = DoubleLinkedList([1, 3, 4])
    d.insert(1, 2)
    assert (len(d)) == 4
    assert d[1] == 2
    assert list(d) == [1, 2, 3, 4]


def test_get_on_position_minus_1():
    d = DoubleLinkedList([0, 1, 2])
    assert d[-1] == 2


def test_insert_on_position_minus_1():
    d = DoubleLinkedList([1, 2, 4])
    d.insert(-1, 3)
    assert (len(d)) == 4
    assert d[2] == 3
    assert list(d) == [1, 2, 3, 4]


def test_append():
    d = DoubleLinkedList([1, 2, 3])
    d.append(4)
    assert (len(d)) == 4
    assert d[-1] == 4
    assert list(d) == [1, 2, 3, 4]


def test_extend():
    d = DoubleLinkedList([1, 2, 3])
    d.extend([4, 5])
    assert (len(d)) == 5
    assert d[-1] == 5
    assert list(d) == [1, 2, 3, 4, 5]


def test_del_at_0():
    d = DoubleLinkedList([1, 2, 3])
    del d[0]
    assert (len(d)) == 2
    assert list(d) == [2, 3]


def test_del_at_1():
    d = DoubleLinkedList([1, 2, 3])
    del d[1]
    assert (len(d)) == 2
    assert list(d) == [1, 3]


def test_pop():
    d = DoubleLinkedList([1, 2, 3])
    assert d.pop() == 3
    assert (len(d)) == 2
    assert list(d) == [1, 2]


def test_rotate_1():
    d = DoubleLinkedList([1, 2, 3, 4])
    d.rotate(1)
    assert (len(d)) == 4
    assert list(d) == [4, 1, 2, 3]


def test_rotate_2():
    d = DoubleLinkedList([1, 2, 3, 4, 5, 6])
    d.rotate(2)
    assert (len(d)) == 6
    assert list(d) == [5, 6, 1, 2, 3, 4]


def test_rotate_5():
    d = DoubleLinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    d.rotate(5)
    assert (len(d)) == 10
    assert list(d) == [6, 7, 8, 9, 10, 1, 2, 3, 4, 5]


def test_rotate__minus_1():
    d = DoubleLinkedList([1, 2, 3, 4])
    d.rotate(-1)
    assert list(d) == [2, 3, 4, 1]


def test_rotate_minus_5():
    d = DoubleLinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    d.rotate(-5)
    assert (len(d)) == 10
    assert list(d) == [6, 7 ,8 , 9, 10, 1, 2, 3, 4, 5]


# TODO: tests using slices
