import datetime
import os


class LogManager:
    def __init__(self, file: str = "logs.txt"):
        self.file = file
        self.__create_file()

    def __create_file(self):
        if not os.path.exists(self.file):
            open(self.file, "x")

    def write(self, text: str, mode: str = "a", new_line: str = "\n"):
        with open(self.file, mode) as f:
            f.write(f"[{datetime.datetime.now().strftime('%settings.json-%m-%Y %H:%M:%S')}] " + text + new_line)


if __name__ == '__main__':
    l = LogManager()
    l.write("test")
