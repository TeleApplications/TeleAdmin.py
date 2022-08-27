import os
from dotenv import load_dotenv


class DotEnv:
    def __init__(self, environment: str = ".env"):
        self.data = load_dotenv(environment)

    @staticmethod
    def get(key: str):
        return os.getenv(key)
