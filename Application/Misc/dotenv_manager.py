import os
from dotenv import load_dotenv


class DotEnv:
    load_dotenv(".env")

    def get(self, key: str):
        return self.__getitem__(key)

    def __getitem__(self, item):
        return os.getenv(item)
