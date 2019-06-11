from functools import wraps

_sentinel = object()

def method_with_slice(method):

    def _getitem(self, indices, slice_):
        results = []
        for index in indices:
            try:
                results.append(method(self, index))
            except IndexError:
                if index > 0 and (slice_.step or 1) > 0 or index < 0:
                    break
                continue

        return self.__class__(results)

    def _setitem(self, indices, slice_, values):
        if not hasattr(type(values), "__len__"):
            values = list(values)
        if slice_.step not in (None, 1) and len(values) != len(indices):
            raise ValueError(f"attempt to assign sequence of size {len(values)} to extended slice of size {len(indices)}")
        if len(values) == len(indices):
            for index, value in zip(indices, values):
                method(self, index, value)
            return
        # Remove previous content
        self.__delitem__(slice_)
        counter = 0
        for i, value in enumerate(values):
            self.insert(slice_.start + i, value)
        return


    def _delitem(self, indices, slice_):
        if slice_.step is None or slice_.step > 0:
            indices = reversed(indices)
        for index in indices:
            method(self, index)
        return

    methods = {"__getitem__": _getitem, "__setitem__": _setitem, "__delitem__": _delitem}

    @wraps(method)
    def _inner(self, index, value=_sentinel):
        value = [value] if value is not _sentinel else []
        if not isinstance(index, slice):
            return method(self, index, *value)
        indices = range(*index.indices(len(self)))
        return methods[method.__name__](self, indices, index, *value)

    return _inner


class SliceableSequenceMixin:

    def __init_subclass__(cls, *args, **kwargs):
        for method_name in "__getitem__ __setitem__ __delitem__".split():
            method = getattr(cls, method_name, _sentinel)
            if method is _sentinel:
                continue
            setattr(cls, method_name, method_with_slice(method))
        super().__init_subclass__(*args, **kwargs)



