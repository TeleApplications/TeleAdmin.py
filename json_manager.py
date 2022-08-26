import json


class Json:
    def __init__(self, filename="settings.json"):
        self.filename = filename

    def load(self):
        with open(self.filename, "r") as f:
            return json.loads(f.read())


if __name__ == '__main__':
    j = Json()
    print(j.load()["orders"]["denyButton"])
