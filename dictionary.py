class Dict(dict):
    def __init__(self):
        super(Dict, self).__init__()

    def add_item(self, key: str, value: int):
        if key in self.keys():
            self.update({key: self.get(key) + value})
        self.setdefault(key, value)

    def remove_item(self, key: str):
        if key in self.keys():
            self.__delitem__(key)
