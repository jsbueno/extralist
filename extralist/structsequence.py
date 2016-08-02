"""NamedTuple like class factory - but which accepts
a string compatible with Python's 'struct' type to hold
each element on the tuple.

moreover, data can be writable
"""

import struct

try:
    from collections.abc import MutableSequence
except ImportError:
    from collections import MutableSequence


class StructItem(object):

    _p_cache = None
    def __init__(self, sequence_class, index=None, values=None):
        self._sequence_class = sequence_class
        self._index = index
        if values is not None:
            self._update_values(values)
        if index is None and values is None:
            raise TypeError("You must either pass an index or a values-object to create a StructItem")

    def _refresh(self):
        if self._index is not None:
            self._p_cache = self._sequence_class._todict(index=self._index)
        else:
            self._p_cache = self._sequence_class._todict(values=self._values)

    @property
    def _cache(self):
        if self._p_cache is None:
            self._refresh()
        return self._p_cache

    def __getattr__(self, attr):
        return self._cache[attr]

    def __setattr__(self, attr, value):
        if attr.startswith("_"):
            return super(StructItem, self).__setattr__(attr, value)
        self._refresh()
        if attr not in self._sequence_class.field_names:
            raise AttributeError('{} item does not have {} attribute'.format(self._sequence_class.__name__, attr))
        self._cache[attr] = value
        if self._index is not None:
            self._store()
        else:
            self._update_values()

    def _update_values(self,  values):
        self._values = self._sequence_class._serialize_item(values)

    def _store(self):
        self._update_values(self._cache)
        if self._index is None:
            self._sequence_class.append(self)
        else:
            self._sequence_class[self._index] = self


    def __eq__(self, other):
        if isinstance(other, StructItem):
            return self._cache == other._cache
        return False

    def __dir__(self):
        return list(self._sequence_class.field_names)

    def __repr__(self):
        return "<{} object[{}]: {}>".format(
            self._sequence_class.name,
            self._index if self._index is not None else "standalone",
            "{{{}}}".format(", ".join(
                "{}:{}".format(repr(key), repr(self._cache[key]))
                    for key in self._sequence_class.field_names
                ))
        )


class StructSequence(MutableSequence):
    slots = ()

    def __init__(self, name, field_names, field_desc):
        if not isinstance(field_names, tuple):
            field_names = tuple(field_names.split())

        self.name = name
        self.field_desc = field_desc
        self.field_names = field_names
        self.data = bytearray()

    def __sizeof__(self):
        return struct.calcsize(self.field_desc)

    def _serialize_item(self, item):
        if isinstance(item, (tuple, list)):
            return struct.pack(self.field_desc, *item)
        return struct.pack(self.field_desc, *(getattr(item, field, item.get(field)) for field in self.field_names ))

    def append(self, item):
        if isinstance(item,  StructItem) and item._sequence_class is self:
            self.data.extend(item._values)
            item._index = len(self) - 1
        else:
            self.data.extend(self._serialize_item(item))

    def __len__(self):
        return len(self.data) // self.__sizeof__()

    def __getitem__(self, index):
        return StructItem(self, index=index)

    def _todict(self, index=None, values=None):
        if index is not None:
            size = self.__sizeof__()
            values = self.data[size * index: (index + 1) * size]
        return {key: value for key, value in zip(self.field_names, struct.unpack(self.field_desc, values))}

    def __setitem__(self, index, item):
        if isinstance(item,  StructItem) and item._sequence_class is self:
            values = item._values
        else:
            values = self._serialize_item(item)
        size = self.__sizeof__()
        self.data[index * size: (index + 1) * size] = values

    def __delitem__(self):
        raise NotImplementedError("StructSequence can't delete items")

    def insert(self):
        raise NotImplementedError("StructSequence can't insert items in random locations. Use append!")



