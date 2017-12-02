from collections.abc import MutableSequence
from threading import Lock

_sentinel = object()

class DoubleLinkedList(MutableSequence):
    """Sequence stored as a linked list of Python Objects.

    Creates a classic "double linked list", complient with
    Python MutableSequence protocol. Each node has a value,
    which is retrieved and set by indexed operations,
    and references for previous and next nodes.

    One can change another node to be the "head"
    by just retrieving it by index.

    The "rotate" method rotates the list "in place".

    This is much less space eficient than normal
    Python sequences, due to the extra wrapper object
    and pointers to values -
    however, insertion and deletion are guarantted
    at O[n] at any point of the object, and if it needs
    to get faster, all one needs is a reference
    to a node close where the insertions and deletions
    are taking place, as the linear time is spend just
    to get to insertion place, not shifting data around.

    TODO: implment get/insert/delete slices capability
    """

    def __new__(cls, initial=None):
        return cls._inner_new__(iter(initial or []))

    @classmethod
    def _inner_new__(cls, initial=None, length_marker=None, lock=None, prev=None):
        self =  super().__new__(cls)
        self.lock = lock if lock else Lock()
        if length_marker is None:
            self._len = [0]
        else:
            self._len = length_marker

        self.prev = prev
        try:
            value = next(initial)
        except (StopIteration, TypeError):
            value = _sentinel
        if value is not _sentinel:
            self._len[0] += 1
            self.value = value
            if prev is not _sentinel:
                self.next = cls._inner_new__(initial, length_marker=self._len, lock=self.lock, prev=self)
        else:
            if prev is None:
                #  We've been created as an empty list
                del self.prev
                return self
            self = self.get_prev(length_marker[0])
            self.prev = prev

        return self

    def get_prev(self, n=0):
        if not n:
            return self
        return self.prev.get_prev(n - 1)


    def get_next(self, n=0):
        if not n:
            return self
        return self.next.get_next(n - 1)

    def _prepare_search(self, index):
        if not self._len[0]:
            raise IndexError
        return self.get_next if index >= 0 else (lambda index: self.get_prev(-index))

    def __getitem__(self, index):
        func = self._prepare_search(index)
        with self.lock:
            return func(index).value

    def __setitem__(self, item, value):
        func = self._prepare_search(index)
        with self.lock:
            node = func(index)
            node.value = value

    def __delitem__(self, index):
        func = self._prepare_search(index)
        with self.lock:
            node = func(index)
            self._len[0] -= 1
            if self._len[0] == 0:
                # del all instance attributes:
                self.__dict__ = {}
                self.__class__ = EmptyDoubleLinkedList
                return
            if index == 0:
                # deleting our own node: we have to replace ourselves
                # so we take the role of the next node,
                # and delete it.
                self.value = self.next.value
                self.next = self.next.next
                self.next.prev = self
                return
            node.next.prev = node.prev
            node.prev.next = node.next

    def __len__(self):
        return self._len[0]

    def insert(self, index, value):
        if self._len[0] == 0:
            with self.lock:
                self.prev = self
                self.next = self
                self._len[0] = 1
                self.value = value
                return
        func = self._prepare_search(index)
        with self.lock:
            node = func(index)
            new_node = DoubleLinkedList._inner_new__(iter([value]), length_marker=self._len, lock=self.lock, prev=_sentinel)
            if index == 0:
                # new_node should take our place on the container
                # so the new node actually carries our old value,
                # and we assume the new value
                new_node.value = self.value
                self.value = value
                new_node.next = self.next
                new_node.prev = self
                self.next.prev = new_node
                self.next = new_node
                return
            node.prev.next = new_node
            new_node.prev = node.prev
            node.prev = new_node
            new_node.next = node

    def __iter__(self):
        node = self
        for i in range(self._len[0]):
            yield node.value
            node = node.next

    def rotate(self, index):
        """Works the same as deque.rotate"""
        index = -index
        func = self._prepare_search(index)
        other = func(index)
        # We swap our links with the other node

        self.__dict__, other.__dict__ = other.__dict__, self.__dict__

        # and fix referencers for all neighbors:

        if self.next is self:
            self.next = other
        if self.prev is self:
            self.prev = other
        if other.next is other:
            other.next = self
        if other.prev is other:
            other.prev = self
        self.prev.next = self
        self.next.prev = self
        other.prev.next = other
        other.next.prev = other



    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, list(self))
