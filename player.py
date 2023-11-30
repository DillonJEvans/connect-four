from enum import Enum


class Player(Enum):
    """A player for a game of Connect 4."""

    ONE = False
    TWO = True

    def __bool__(self):
        return bool(self.value)
