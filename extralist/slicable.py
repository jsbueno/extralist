from functools import wraps

_sentinel = object()

def method_with_slice(method):
    @wraps(method)
    def _inner(self, index, value=_sentinel):
        value = [value] if value is not _sentinel else []
        if not isinstance(index, slice):
            return method(self, index, *value)
        indexes = index
        if method.__name__ == "__getitem__":
            results = []
            for index in indexes.indices(len(self)):
                results.append(method(self, index))
            return results
        raise NotImplementedError()

    return _inner




class SlicableSequenceMixin:

    def __init_subclass__(cls, *args, **kwargs):
        for method_name in "__getitem__ __setitem__ __delitem__".split():
            method = getattr(cls, method_name, _sentinel)
            if method is _sentinel:
                continue
            setattr(cls, method_name, method_with_slice(method))
        super().__init_subclass__(*args, **kwargs)



