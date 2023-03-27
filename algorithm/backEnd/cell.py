from container import Container
from enum import Enum


class Condition(Enum):
    HULL = 0
    OCCUPIED = 1
    EMPTY = 2
    UNOCCUPIABLE = 3


class Cell:
    def __init__(self, state: Condition = Condition.EMPTY, container: Container = None):
        self.state = state
        self.container = container

    def __str__(self) -> str:
        if self.state is Condition.HULL:
            return "Hull"
        elif self.state is Condition.OCCUPIED:
            if self.container is None:
                exception()
            return "Occupied " + self.container
