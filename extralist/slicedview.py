from collections.abc import MutableSequence


class SlicedView(MutableSequence):
    """A View on a sequence.
    Allows one to have sub-lists of a list without duplicating te underlying data.

    Reading a slice from an object of this class will produce a new view
    on the original data. (But passing a SlicedView as data to it,
    will wrap that view in an extra layer)


    """

    def __init__(self, data, slice=None):
        self.data = data
        given_slice = slice
        slice = __builtins__["slice"]
        if isinstance(given_slice, slice):
            start = given_slice.start
            stop = given_slice.stop
            step = given_slice.step
        else:
            start, stop, step = given_slice if given_slice is not None else (0, len(data), 1)
        if start is None:
            start = 0
        if stop is None:
            stop = len(data)
        if step is None:
            step = 1

        self.slice = slice(start, stop, step)

    def _real_index(self, index):
        real_index = self.slice.start + index * self.slice.step
        if real_index > len(self.data):
            raise IndexError("Index out of range.")
        return real_index

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.__class__(self.data, slice(
                self.slice.start + index.start,
                min(self.slice.start + (index.start or 0), self.slice.stop),
                self.slice.step * (index.step or 1)
            ))
        if index < 0:
            raise NotImplementedError("Can't use negative indexes on a SlicedView")
        return  self.data[self._real_index(index)]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            raise NotImplementedError("Can't assign to slice on SlicedView")
        if index < 0:
            raise NotImplementedError("Can't use negative indexes on a SlicedView")
        self.data[self._real_index(index)] = value

    def __delitem__(self, index):
        if isinstance(index, slice):
            self.data.__delitem__(slice(
                self.slice.start + (index.start or 0),
                min(self.slice.stop, self.slice.start + (
                    item.stop if item.stop is not None else (self.slice.start + len(self)) // self.slice.step
                )),
                self.slice.step * (index.step or 1)
            ))

        else:
            del self.data[self._real_index(index)]

    def __len__(self):
        if len(self.data) < self.slice.start:
            return 0
        return (min(self.slice.stop, len(self.data)) - self.slice.start) // self.slice.step


    def __iter__(self):
        for i in range(self.slice.start, self.slice.stop, self.slice.step):
            yield self.data[i]

    def insert(self, position, value):
        self.data.insert(self._real_index(position), value)


