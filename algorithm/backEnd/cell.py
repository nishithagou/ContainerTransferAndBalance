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
    
    def __init__(self, state: Condition = Condition.EMPTY):
        self.state = state
        self.container = None

    def __init__(self, container=None):
        self.state = Condition.OCCUPIED
        self.container = container
