class Dict:
    def __init__(self):
        self.dict = dict()

    def add_item(self, key: str, value: int):
        if key in self.dict.keys():
            self.dict[key] += value
        self.dict.setdefault(key, value)

    def remove_item(self, key: str):
        if key in self.dict.keys():
            self.dict.__delitem__(key)

    def clear(self):
        self.dict.clear()


# if __name__ == '__main__':
    # d = Dict()
    # d.add_item("mates", 10)
    # print(d.dict)
    # d.remove_item("mates")
    # print(d.dict)

