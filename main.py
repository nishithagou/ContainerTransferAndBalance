#cell.hpp
from enum import Enum

class Condition(Enum):
    HULL = 1
    OCCUPIED = 2
    EMPTY = 3
    UNOCCUPIABLE = 4

class Cell:
    def __init__(self, state='EMPTY'):
        self.state = state
        self.container = None

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

#container.hpp
class Container:
    def __init__(self, description, weight, toOffload=False):
        self.weight = weight
        self.description = description
        self.toOffload = toOffload

    def getDescription(self):
        return self.description

    def toString(self):
        return self.description + " (weight: " + str(self.weight) + ")"

    def getWeight(self):
        return self.weight

    def isToBeOffloaded(self):
        return self.toOffload


#coordinate.cpp
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __ne__(self, other):
        return (other.x != self.x) or (other.y != self.y)

    def __eq__(self, other):
        return (other.x == self.x) and (other.y == self.y)

    def toString(self):
        return f"({self.x}, {self.y})"


class ContainerCoordinate(Coordinate):
    def __init__(self, x, y, isInBuffer=False):
        super().__init__(x, y)
        self.isInBuffer = isInBuffer

#port.cpp
class Port:
    def __init__(self, shipSize, bufferSize):
        # field initialization
        self.moveDescription = ""
        self.parent = None
        self.cranePosition = Coordinate(0, 0)
        self.craneState = "SHIP"
        self.costToGetHere = 0
        self.aStarCost = 0
        self.solved = False
        self.ship = Space(shipSize.x, shipSize.y)
        self.buffer = Space(bufferSize.x, bufferSize.y)

    def __init__(self):
        self.moveDescription = ""
        self.parent = None
        self.cranePosition = Coordinate(0, 0)
        self.craneState = "SHIP"
        self.costToGetHere = 0
        self.aStarCost = 0
        self.solved = False
        self.ship = Space(0, 0)
        self.buffer = Space(0, 0)

    def __lt__(self, rhs):
        return self.aStarCost < rhs.aStarCost

    def calculateAStar(self):
        self.aStarCost = self.costToGetHere + self.calculateHeuristic()

    def getMoveDescription(self):
        return self.moveDescription

    def isSolved(self):
        return self.solved


class Transfer(Port):
    def __init__(self, shipSize, bufferSize, shipLoad, toLoad):
        # Field Initialization
        super().__init__(shipSize, bufferSize)
        self.toOffload = []
        self.toStay = []

        for i in range(len(shipLoad)):
            CO = shipLoad[i][1]
            CELL = shipLoad[i][0]
            if CELL.getState() == "HULL":
                self.ship.setAsHull(CO.x, CO.y)
            elif CELL.getState() == "OCCUPIED":
                self.ship.setAsOccupied(CO.x, CO.y, CELL.getContainer())
            else:
                # what are you trying to pull?
                raise Exception("Invalid State")

            # handles where we have containers that need to be offloaded
            if shipLoad[i][0].getState() == "OCCUPIED" and shipLoad[i][0].getContainer().isToBeOffloaded():
                containerToOffload = (ContainerCoordinate(CO.x, CO.y), shipLoad[i][0].getContainer())
                self.toOffload.append(containerToOffload)
            # handles where we have containers that just need to stay in the ship after the operation
            elif shipLoad[i][0].getState() == "OCCUPIED" and not shipLoad[i][0].getContainer().isToBeOffloaded():
                containerToStay = (ContainerCoordinate(CO.x, CO.y), shipLoad[i][0].getContainer())
                self.toStay.append(containerToStay)

        # preallocate memory minor optimization
        self.toLoad = []
        self.toLoad.reserve(len(toLoad))
        # negative values are sentinel values that indicate the containers are not in the buffer
        # nor the ship but rather on the trucks
        notOnShip = ContainerCoordinate(-1, -1)
        for c in toLoad:
            containerToLoad = (notOnShip, c)
            self.toLoad.append(containerToLoad)

def calculate_heuristic(self):
    # this is just the remaining number of containers that need to load. Will just
    # assume all containers can just phase through one another
    minutes_to_load = len(self.to_load) * 2

    # this is the remaining number of containers that need to offload
    # thanks to how we defined the coordinate system the manhattan distance is
    # calculated the same for both the ship and buffer
    minutes_to_offload = 0
    for coord, container in self.to_offload.items():
        minutes_to_offload += 2 + coord.x + coord.y

    # for the edge case of having a container in the buffer that needs to be put
    # back onto the ship. If the container that needs to stay on the ship is already
    # on the ship, the heuristic for that will be 0
    minutes_to_move_from_buffer_to_ship = 0
    for coord, container in self.to_stay.items():
        if coord.is_in_buffer:
            minutes_to_move_from_buffer_to_ship += 4 + coord.x + coord.y

    # okay heuristic to be finetuned. Can certainly be better
    # TODO: finetune
    lower_bound_time_left = minutes_to_load + minutes_to_offload + minutes_to_move_from_buffer_to_ship
    if lower_bound_time_left == 0:
        self.solved = True
    return lower_bound_time_left


def move_container_and_crane(self, container, start, end, start_space, end_space):
    # just moving the crane
    if container is None:
        # another sanity check
        if end_space == "SHIP":
            if self.ship.get_cell_state(end.x, end.y) != "OCCUPIED":
                raise ValueError("Invalid end coordinate, it is not occupied by a container")
        elif end_space == "BUFFER":
            if self.buffer.get_cell_state(end.x, end.y) != "OCCUPIED":
                raise ValueError("Invalid end coordinate, it is not occupied by a container")
        self.crane_position = end
        self.crane_state = end_space
        self.move_description += "\nMoving crane only from " + self.to_string_from_state(start_space) + " " + str(start) + " to " + self.to_string_from_state(end_space) + " " + str(end)
    # moving the crane and the container c
    else:
        self.crane_position = end
        self.crane_state = end_space
        # add container at end
        if end_space == "BUFFER":
            self.buffer.add_container(end.x, end.y, container)
        elif end_space == "SHIP":
            self.ship.add_container(end.x, end.y, container)
        self.update_container_coordinate_vectors(container, end, end_space)
        # remove container at beginning
        if start_space == "BUFFER":
            self.buffer.remove_container(start.x, start.y)
        elif start_space == "SHIP":
            self.ship.remove_container(start.x, start.y)
        self.move_description += "\nMoving container " + container.to_string() + " from " + self.to_string_from_state(start_space) + " " + str(start) + " to " + self.to_string_from_state(end_space) + " " + str(end)

from typing import List

class Transfer:
    def __init__(self, cranePosition: Coordinate, craneState: CraneState, costToGetHere: int):
        self.cranePosition = cranePosition
        self.craneState = craneState
        self.costToGetHere = costToGetHere
        self.parent = None
        self.moveDescription = ""

    def createDerivatative(self, container: Container, end: Coordinate, endSpace: str) -> 'Transfer':
        deriv = Transfer(self.cranePosition, self.craneState, self.costToGetHere)
        deriv.parent = self
        deriv.moveDescription = self.moveDescription
        translationMove = self.calculateManhattanDistance(self.cranePosition, end, self.craneState, endSpace)
        deriv.moveContainerAndCrane(container, self.cranePosition, end, self.craneState, endSpace)
        deriv.costToGetHere += translationMove
        deriv.calculateAStar()
        return deriv

    def updateContainerCoordinateVectors(self, container: Container, newPosition: Coordinate, newSpace: str):
        if container.isToBeOffloaded:
            for i, to_offload in enumerate(self.toOffload):
                if to_offload[1] == container:
                    if newSpace == "TRUCKBAY":
                        self.toOffload.pop(i)
                        return

                    new_coord = ContainerCoordinate(newPosition.x, newPosition.y)
                    new_coord.isInBuffer = newSpace == "BUFFER"
                    to_offload[0] = new_coord
                    return

            raise Exception("Did not find the appropriate container")
        else:
            for i, to_stay in enumerate(self.toStay):
                if to_stay[1] == container:
                    new_coord = ContainerCoordinate(newPosition.x, newPosition.y)
                    new_coord.isInBuffer = newSpace == "BUFFER"
                    to_stay[0] = new_coord
                    return

            new_coord = ContainerCoordinate(newPosition.x, newPosition.y)
            new_coord.isInBuffer = newSpace == "BUFFER"
            to_add = (new_coord, container)
            self.toStay.append(to_add)

def calculateManhattanDistance(start, end, startSpace, endSpace):
    if startSpace == endSpace:
        if startSpace == "BUFFER":
            currSpace = buffer
        else:
            currSpace = ship

        toMoveX = start[0] - end[0]
        SPACE_HEIGHT = currSpace.getHeight()

        if toMoveX > 0:
            minDepth = start[1]
            for x in range(start[0], end[0]-1, -1):
                minClearance = SPACE_HEIGHT - currSpace.getStackHeight(x)
                if minDepth <= minClearance:
                    minDepth = minClearance
            return (start[1] - minDepth) + toMoveX + (end[1] - minDepth)

        elif toMoveX < 0:
            minDepth = start[1]
            for x in range(start[0], end[0]+1):
                minClearance = SPACE_HEIGHT - currSpace.getStackHeight(x)
                if minDepth <= minClearance:
                    minDepth = minClearance
            return (start[1] - minDepth) + (-toMoveX) + (end[1] - minDepth)

        else:
            raise Exception("Why are you trying to move within the same column?")

    else:
        if startSpace == "TRUCKBAY" and endSpace == "TRUCKBAY":
            raise Exception("Illogical move")

        if startSpace == "TRUCKBAY":
            return end[0] + end[1] + 2

        if endSpace == "TRUCKBAY":
            return start[0] + start[1] + 2

        return start[0] + start[1] + end[0] + end[1] + 4

def toStringFromState(state: str) -> str:
    # CraneState {SHIP, BUFFER, TRUCKBAY};
    if state == 'SHIP':
        return 'Ship'
    elif state == 'BUFFER':
        return 'Buffer'
    elif state == 'TRUCKBAY':
        return 'Truck Bay'
    else:
        # why did you send a invalid state
        raise ValueError('Invalid state')

def __eq__(self, rhs):
    if self.craneState != rhs.craneState:
        return False
    if self.cranePosition != rhs.cranePosition:
        return False
    # find the first thing that is unequal
    # go through the ship's space
    for row in range(self.ship.getHeight()):
        for col in range(self.ship.getWidth()):
            if rhs.ship.getCell(col, row).getState() != self.ship.getCell(col, row).getState():
                return False
    # then the buffer's space room for optimization
    for row in range(self.buffer.getHeight()):
        for col in range(self.buffer.getWidth()):
            if rhs.buffer.getCell(col, row).getState() != self.buffer.getCell(col, row).getState():
                return False
    return True

def tryAllOperators(self) -> List[Port]:
    CRANE_COLUMN = self.cranePosition.x
    acc = []

    if self.craneState == CraneState.SHIP:
        if self.cranePosition == Coordinate(0, 0):
            for i in range(self.ship.getWidth()):
                if self.ship.getStackHeight(i) > 0 and self.ship.getTopPhysicalCell(i).getState() != CellState.HULL and i != CRANE_COLUMN:
                    NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                    acc.append(createDerivatative(None, NEW_COORD, Port.TRUCKBAY))

            if len(self.toLoad) != 0:
                acc.append(createDerivatative(None, Coordinate(0, 0), Port.TRUCKBAY))
        else:
            if self.ship.getCell(self.cranePosition.x, self.cranePosition.y).getState() != CellState.OCCUPIED:
                raise Exception(5)

            toMove = self.ship.getCell(self.cranePosition.x, self.cranePosition.y).getContainer()

            if toMove.isToBeOffloaded():
                acc.append(createDerivatative(toMove, Coordinate(0, 0), Port.TRUCKBAY))
                return acc

            for i in range(self.ship.getWidth()):
                if self.ship.getStackHeight(i) < self.ship.getHeight() - 1 and i != CRANE_COLUMN:
                    NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                    acc.append(createDerivatative(toMove, NEW_COORD, Port.SHIP))

            for i in range(self.buffer.getWidth()):
                if self.buffer.getStackHeight(i) < self.buffer.getHeight() - 1:
                    NEW_COORD = Coordinate(i, self.buffer.getHeight() - self.buffer.getStackHeight(i) - 1)
                    acc.append(createDerivatative(toMove, NEW_COORD, Port.BUFFER))

            for i in range(self.ship.getWidth()):
                if self.ship.getStackHeight(i) > 0 and self.ship.getTopPhysicalCell(i).getState() != CellState.HULL and i != CRANE_COLUMN:
                    NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                    acc.append(createDerivatative(None, NEW_COORD, Port.SHIP))

            for i in range(self.buffer.getWidth()):
                if self.buffer.getStackHeight(i) > 0:
                    NEW_COORD = Coordinate(i, self.buffer.getHeight() - self.buffer.getStackHeight(i) - 1)
                    acc.append(createDerivatative(None, NEW_COORD, Port.BUFFER))

            if len(self.toLoad) != 0:
                acc.append(createDerivatative(None, Coordinate(0, 0), Port.TRUCKBAY))

   if self.craneState == CraneState.BUFFER:
        if self.buffer.getCell(self.cranePosition.x, self.cranePosition.y).getState() != CellState.OCCUPIED:
            raise Exception(5)

        toMove = self.buffer.getCell(self.cranePosition.x, self.cranePosition.y).getContainer()

        if toMove.isToBeOffloaded():
            acc.append(createDerivatative(toMove, Coordinate(0, 0), CraneState.TRUCKBAY))
        for i in range(self.ship.getWidth()):
            if self.ship.getStackHeight(i) < self.ship.getHeight() - 1:
                NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                acc.append(createDerivatative(toMove, NEW_COORD, CraneState.SHIP))

        for i in range(self.buffer.getWidth()):
            if self.buffer.getStackHeight(i) > 0 and i != CRANE_COLUMN:
                NEW_COORD = Coordinate(i, self.buffer.getHeight() - self.buffer.getStackHeight(i) - 1)
                acc.append(createDerivatative(None, NEW_COORD, CraneState.BUFFER))

        for i in range(self.ship.getWidth()):
            if self.ship.getStackHeight(i) > 0 and self.ship.getTopPhysicalCell(i).getState() != CellState.HULL:
                NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                acc.append(createDerivatative(None, NEW_COORD, CraneState.SHIP))

        acc.append(createDerivatative(None, Coordinate(0, 0), CraneState.TRUCKBAY))
    elif self.craneState == CraneState.TRUCKBAY:
        for i in range(self.buffer.getWidth()):
            if self.buffer.getStackHeight(i) > 0:
                NEW_COORD = Coordinate(i, self.buffer.getHeight() - self.buffer.getStackHeight(i) - 1)
                acc.append(createDerivatative(None, NEW_COORD, CraneState.BUFFER))

        for i in range(self.ship.getWidth()):
            if self.ship.getStackHeight(i) > 0 and self.ship.getTopPhysicalCell(i).getState() != CellState.HULL:
                NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                acc.append(createDerivatative(None, NEW_COORD, CraneState.SHIP))

        if len(self.toLoad) != 0:
            toMove = self.toLoad[-1][1]
            newToLoad = self.toLoad.copy()
            newToLoad.pop()
            for i in range(self.buffer.getWidth()):
                if self.buffer.getStackHeight(i) < self.buffer.getHeight() - 1:
                    NEW_COORD = Coordinate(i, self.buffer.getHeight() - self.buffer.getStackHeight(i) - 1)
                    acc.append(createDerivatative(toMove, NEW_COORD, CraneState.BUFFER))
            for i in range(self.ship.getWidth()):
                if self.ship.getStackHeight(i) < self.ship.getHeight() - 1:
                    NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                    acc.append(createDerivatative(toMove, NEW_COORD, CraneState.SHIP))
    else:
        raise Exception(2)
    return acc


def toStringBasic(self):
    acc = ''
    acc_capacity = self.buffer.getHeight() * (self.buffer.getWidth() + 1) + \
                   self.ship.getHeight() * (self.ship.getWidth() + 1)
    acc = ['0'] * acc_capacity
    acc_idx = 0

    empty_buffer_stack = '0' * self.buffer.getHeight() + '\n'
    for i in range(self.buffer.getWidth()):
        if self.buffer.getStackHeight(i) == 0:
            acc += empty_buffer_stack
            acc_idx += len(empty_buffer_stack)
        else:
            for j in range(self.buffer.getHeight()):
                if self.buffer.getCellState(i, j) == EMPTY or \
                        self.buffer.getCellState(i, j) == UNOCCUPIABLE:
                    acc[acc_idx] = '0'
                elif self.buffer.getCellState(i, j) == OCCUPIED:
                    if self.buffer.getCell(i, j).getContainer().isToBeOffloaded():
                        acc[acc_idx] = '2'
                    else:
                        acc[acc_idx] = '1'
                acc_idx += 1
            acc[acc_idx] = '\n'
            acc_idx += 1

    if self.craneState == TRUCKBAY:
        acc += "1\n"
    else:
        acc += "0\n"

    empty_ship_stack = '0' * self.ship.getHeight() + '\n'
    for i in range(self.ship.getWidth()):
        if self.ship.getStackHeight(i) == 0:
            acc += empty_ship_stack
            acc_idx += len(empty_ship_stack)
        else:
            for j in range(self.ship.getHeight()):
                if self.ship.getCellState(i, j) == EMPTY or \
                        self.ship.getCellState(i, j) == HULL or \
                        self.ship.getCellState(i, j) == UNOCCUPIABLE:
                    acc[acc_idx] = '0'
                elif self.ship.getCellState(i, j) == OCCUPIED:
                    if self.ship.getCell(i, j).getContainer().isToBeOffloaded():
                        acc[acc_idx] = '2'
                    else:
                        acc[acc_idx] = '1'
                acc_idx += 1
            acc[acc_idx] = '\n'
            acc_idx += 1

    return ''.join(acc)




#space.cpp
class Space:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell(UNOCCUPIABLE) for _ in range(height)] for _ in range(width)]
        self.stackHeights = [0] * width

    def getCell(self, col, row):
        return self.cells[col][row]

    def getCellState(self, col, row):
        return self.cells[col][row].getState()

    def setAsHull(self, col, row):
        self.increaseStackHeight(col, row)
        self.cells[col][row].setState(HULL)

    def setAsOccupied(self, col, row, container):
        self.increaseStackHeight(col, row)
        self.cells[col][row].setState(OCCUPIED)
        self.cells[col][row].setContainer(container)

    def increaseStackHeight(self, col, row):
        self.stackHeights[col] += 1

    def addContainer(self, col, row, container):
        if self.cells[col][row].getState() != EMPTY:
            raise Exception(10)
        self.cells[col][row].setState(OCCUPIED)
        self.cells[col][row].setContainer(container)
        self.increaseStackHeight(col, row)

   def removeContainer(self, col, row):
        if self.cells[col][row].getState() != OCCUPIED:
            raise Exception(9)
        self.cells[col][row].setState(EMPTY)
        self.stackHeights[col] = self.stackHeights[col] - 1
    def getStackHeight(self, col):
        return self.stackHeights[col]

    def getTopPhysicalCell(self, col):
        if self.stackHeights[col] == 0:
            return Cell(EMPTY)
        else:
            return self.cells[col][self.height - self.stackHeights[col] - 1]

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height




]
