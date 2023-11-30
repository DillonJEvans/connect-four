from enum import Enum


class Player(Enum):
    ONE = False
    TWO = True

    def __bool__(self):
        return bool(self.value)
