from functools import wraps

_sentinel = object()

def method_with_slice(method):

    def _getitem(self, indexes):
        results = []
        for index in indexes:
            results.append(method(self, index))
        return self.__class__(results)

    def _setitem(self, indexes, values):
        raise NotImplementedError()

    def _delitem(self, indexes):
        raise NotImplementedError()

    methods = {"__getitem__": _getitem, "__setitem__": _setitem, "__delitem__": _delitem}

    @wraps(method)
    def _inner(self, index, value=_sentinel):
        value = [value] if value is not _sentinel else []
        if not isinstance(index, slice):
            return method(self, index, *value)
        indexes = range(*index.indices(len(self)))
        return methods[method.__name__](self, indexes, *value)

    return _inner


class SliceableSequenceMixin:

    def __init_subclass__(cls, *args, **kwargs):
        for method_name in "__getitem__ __setitem__ __delitem__".split():
            method = getattr(cls, method_name, _sentinel)
            if method is _sentinel:
                continue
            setattr(cls, method_name, method_with_slice(method))
        super().__init_subclass__(*args, **kwargs)



