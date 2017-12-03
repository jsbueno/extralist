import pytest

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


def test_iterate_on_empty():
    d = DoubleLinkedList([1,])
    del d[0]
    assert list(d) == []


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


def test_assign_to_index():
    d = DoubleLinkedList([0, 1, 2])
    d[0] = 3
    assert d[0] == 3
    d[-1] = 4
    assert d[-1] == 4


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


def test_eq():
    d = DoubleLinkedList([1, 2, 3])
    d1 = DoubleLinkedList([1, 2, 3])
    assert d == d1
    d1.append(4)
    assert d != d1
    d1.pop()
    d1[-1] = "4"
    assert d != d1
    assert d == [1, 2, 3]


def test_slice_get_results_is_correct_class():
    d = DoubleLinkedList([0, 1, 2, 3])
    assert type(d[0:1]) is DoubleLinkedList
    t1 = type("t1", (DoubleLinkedList,), {})
    d1 = t1([0, 1, 2, 3])
    assert type(d1[0:1]) is t1


@pytest.mark.parametrize("name,input,result", [
    ("unit_slice", (0, 1, None), [0]),
    ("anonymous_start", (None, 2, None), [0, 1]),
    ("anonymous_stop", (2, None, None), [2, 3]),
    ("normal_slice", (1, 3 ,None), [1,2]),
    ("anonymous_double_step_slice", (None, None, 2), [0, 2]),
    ("anonymous_negative_step_slice", (None, None, -1), [3, 2, 1, 0]),
    ("larger_than_original_slice", (0, 8, None), [0, 1, 2, 3, 0, 1, 2, 3]),
])
def test_slice_get_(name, input, result):
    d = DoubleLinkedList([0, 1, 2, 3])
    index = slice(*input)
    assert list(d[index]) == result
    #assert list(d[0:1]) == [0]
    #assert list(d[1:3]) == [1,2]
    #assert type(d[0:1]) is DoubleLinkedList
    #assert list(d[::2]) == [0, 2]
    #assert list(d[::-1]) == [3, 2, 1, 0]
    #assert list(d[0: 8]) == [0, 1, 2, 3, 0, 1, 2, 3]


def backwards_path_get_all_values(d):
    """Verifies integrity of double linked list
    by checking the elements visited if going backwards
    are the same visited if going forward.
    """
    backward = []
    node = d.prev
    for i in range(len(d)):
        backward.append(node.value)
        node = node.prev
    assert backward[::-1] == list(d)


def test_backward_path_get_all_values():
    d = DoubleLinkedList([0, 1, 2, 3])
    backwards_path_get_all_values(d)


@pytest.mark.parametrize("name,input,result", [
    ("unit_slice", (0, 1, None), [1, 2, 3]),
    ("normal_slice", (1, 3 ,None), [0, 3]),
    ("anonymous_double_step_slice", (None, None, 2), [1, 3]),
    ("anonymous_negative_step_slice", (None, None, -1), []),
    ("anonymous_negative_step_slice_with_stop", (None, 0, -1), [0]),
    ("larger_than_original_slice", (0, 8, None), []),
])
def test_slice_del_(name, input, result):
    d = DoubleLinkedList([0, 1, 2, 3])
    index = slice(*input)
    del d[index]
    assert list(d) == result
    if d:
        backwards_path_get_all_values(d)


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
