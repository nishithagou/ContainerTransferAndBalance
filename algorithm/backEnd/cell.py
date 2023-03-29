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
        if self.state == Condition.HULL:
            return "Hull"
        elif self.state == Condition.OCCUPIED:
            if self.container is None:
                raise Exception("Error: Occupied cell has no container")
            else:
                return "Occupied " + str(self.container)
        elif self.state == Condition.EMPTY:
            return "Empty"
        else:
            return "Unoccupiable"

    def __eq__(self, other) -> bool:
        if isinstance(other, Cell):
            return self.state == other.state
        if isinstance(other, Condition):
            return self.state == other
