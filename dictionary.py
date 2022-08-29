class Dictionary:
    def __init__(self):
        super(Dictionary, self).__init__()
        self._dict = dict()

    def __getitem__(self, item):
        return self._dict[item]

    def add_item(self, key: str, value: int):
        if key in self._dict.keys():
            self._dict.update({key: self._dict.get(key) + value})
        self._dict.setdefault(key, value)

    def remove_item(self, key: str):
        if key in self._dict.keys():
            self._dict.__delitem__(key)

    def clear(self):
        self._dict.clear()

    def items(self):
        return self._dict.items()
