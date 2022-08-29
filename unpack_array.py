from typing import Iterable


class UnpackArray:
    def __init__(self):
        self._list = list()

    def __repr__(self):
        return f"{self._list}"

    def __getitem__(self, item):
        return self._list[item]

    def unpack_array(self, iterable: Iterable, datatype) -> None:
        if isinstance(iterable, datatype):
            for item in iterable:
                if isinstance(item, datatype):
                    self.unpack_array(item, datatype)
                else:
                    self._list.append(item)
        else:
            self._list.append(iterable)
