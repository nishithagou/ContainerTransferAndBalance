
from enum import Enum


class Condition(Enum):
    HULL = 0
    OCCUPIED = 1
    EMPTY = 2
    UNOCCUPIABLE = 3

class Cell:
    def __init__(self, state='EMPTY', container=None):
        self.state = state
        self.container = container
        ("* msg: Cell init(state=empty) was called")

    def __init__(self, state='nonEMPTY', container="dog"):
        self.state = state
        self.container = container
        ("* msg: Cell init(state=nonEmpty) was called")

    def setContainer(self, newContainer):
        self.container = newContainer

    def clearContainer(self):
        self.container = None

    def getContainer(self):
        return self.container

    def getState(self):
        return self.state

    def setState(self, newState):
        self.state = newState
