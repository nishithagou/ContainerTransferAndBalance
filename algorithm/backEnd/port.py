from enum import Enum
from abc import ABC, abstractmethod
from space import *

from coordinate import *
from cell import *
from space import *


class CraneState(Enum):
    SHIP = 1
    BUFFER = 2
    TRUCKBAY = 3


class Port(ABC):
    # cost defined as minutes i.e. Manhattan Distance
    #shipSize => Coordinate
    #bufferSize => Coordinate
    def __init__(self, ship_size: Coordinate, buffer_size: Coordinate):
        # describes the move done; only to be modified in tryAllOperators
        self.moveDescription = ""
        # parent describes how the Port is derived from
        self.parent = None
        self.cranePosition = Coordinate(0, 0)
        self.craneState = CraneState.SHIP
        # the number of minutes it took to reach this Port i.e. g(n)
        self.costToGetHere = 0
        # The lower bound number of minutes it has taken and will take for the Port to finish
        self.aStarCost = 0
        self.solved = False
        self.ship = Space(ship_size.x, ship_size.y)
        self.buffer = Space(buffer_size.x, buffer_size.y)

    def eq(self, rhs):
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

    def lessThan(self, rhs):
        return self.aStarCost < rhs.aStarCost

    def greaterThan(lhs, rhs):
        return lhs.aStarCost > rhs.aStarCost

    def calculateAStar(self):
        self.aStarCost = self.costToGetHere + self.calculateHeuristic()

    def getMoveDescription(self):
        return self.moveDescription

    def isSolved(self):
        return self.solved

    def calculateHeuristic(self):
        pass

    def calculateManhattanDistance(self, start, end, startSpace, endSpace):
        if startSpace == endSpace:
            # Are we in the buffer or ship?
            if startSpace == "BUFFER":
                currSpace = self.buffer
            else:
                currSpace = self.ship
            
            # Actually the most complicated to calculate
            toMoveX = start.x - end.x
            SPACE_HEIGHT = currSpace.getHeight()
            if toMoveX > 0:
                # Need to decrement x
                minDepth = start.y
                for x in range(start.x, end.x-1, -1):
                    minClearance = SPACE_HEIGHT - currSpace.getStackHeight(x)
                    if minDepth <= minClearance:
                        minDepth = minClearance
                return (start.y - minDepth) + toMoveX + (end.y - minDepth)
            elif toMoveX < 0:
                # Need to increment x
                minDepth = start.y
                for x in range(start.x, end.x+1):
                    minClearance = SPACE_HEIGHT - currSpace.getStackHeight(x)
                    if minDepth <= minClearance:
                        minDepth = minClearance
                return (start.y - minDepth) + (-toMoveX) + (end.y - minDepth)
            else:
                # Why are you trying to move within the same column?
                raise ValueError("Trying to move within the same column")
        # This is an "interspace" transfer so like moving between the buffer/ship/truckbay
        # Actually made easier since the crane always has to go up to 0,0 coordinate
        else:
            if startSpace == "TRUCKBAY" and endSpace == "TRUCKBAY":
                # Illogical move, throw error
                raise ValueError("Trying to move within the same truckbay")
            # Quite trivial
            if startSpace == "TRUCKBAY":
                return end.x + end.y + 2
            if endSpace == "TRUCKBAY":
                return start.x + start.y + 2
            # Only dealing with distance between ship and buffer also pretty trivial
            return start.x + start.y + end.x + end.y + 4


    def toStringFromState(state):
        if state == "SHIP":
            return "Ship"
        elif state == "BUFFER":
            return "Buffer"
        elif state == "TRUCKBAY":
            return "Truck Bay"
        else:
            raise ValueError("Invalid state")
        

    def tryAllOperators(self):
        CRANE_COLUMN = self.cranePosition.x
        acc = []
        
        if self.craneState == CraneState.SHIP:
            if self.cranePosition == Coordinate(0, 0):
                for i in range(self.ship.getWidth()):
                    if self.ship.getStackHeight(i) > 0 and self.ship.getTopPhysicalCell(i).getState() != Condition.Hull and i != CRANE_COLUMN:
                        NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                        acc.append(self.createDerivatative(None, NEW_COORD, CraneState.SHIP))
                if len(self.toLoad) != 0:
                    acc.append(self.createDerivatative(None, Coordinate(0, 0), CraneState.TRUCKBAY))
            else:
                if self.ship.getCell(self.cranePosition.x, self.cranePosition.y).getState() != Condition.Occupied:
                    raise ValueError(5)
                toMove = self.ship.getCell(self.cranePosition.x, self.cranePosition.y).getContainer()
                if toMove.isToBeOffloaded():
                    acc.append(self.createDerivatative(toMove, Coordinate(0, 0), CraneState.TRUCKBAY))
                    return acc
                for i in range(self.ship.getWidth()):
                    if self.ship.getStackHeight(i) < self.ship.getHeight() - 1 and i != CRANE_COLUMN:
                        NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                        acc.append(self.createDerivatative(toMove, NEW_COORD, CraneState.SHIP))
                for i in range(self.buffer.getWidth()):
                    if self.buffer.getStackHeight(i) < self.buffer.getHeight() - 1:
                        NEW_COORD = Coordinate(i, self.buffer.getHeight() - self.buffer.getStackHeight(i) - 1)
                        acc.append(self.createDerivatative(toMove, NEW_COORD, CraneState.BUFFER))
                for i in range(self.ship.getWidth()):
                    if self.ship.getStackHeight(i) > 0 and self.ship.getTopPhysicalCell(i).getState() != Condition.Hull and i != CRANE_COLUMN:
                        NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                        acc.append(self.createDerivatative(None, NEW_COORD, CraneState.SHIP))
                for i in range(self.buffer.getWidth()):
                    if self.buffer.getStackHeight(i) > 0:
                        NEW_COORD = Coordinate(i, self.buffer.getHeight() - self.buffer.getStackHeight(i) - 1)
                        acc.append(self.createDerivatative(None, NEW_COORD, CraneState.BUFFER))
                if len(self.toLoad) != 0:
                    acc.append(self.createDerivatative(None, Coordinate(0, 0), CraneState.TRUCKBAY))
                    
        elif self.craneState == CraneState.BUFFER:
            if self.buffer.getCell(self.cranePosition.x, self.cranePosition.y).getState() != Condition.Occupied:
                raise ValueError(5)
            toMove = self.buffer.getCell(self.cranePosition.x, self.cranePosition.y).getContainer()
            if toMove.isToBeOffloaded():
                acc.append(self.createDerivatative(toMove, Coordinate(0, 0), CraneState.TRUCKBAY))
                return acc
            for i in range(self.ship.getWidth()):
                if self.ship.getStackHeight(i) < self.ship.getHeight() - 1:
                    NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                    acc.append(self.createDerivatative(toMove, NEW_COORD, CraneState.SHIP))
            for i in range(self.buffer.getWidth()):
                if self.buffer.getStackHeight(i) > 0 and i != CRANE_COLUMN:
                    NEW_COORD = Coordinate(i, self.buffer.getHeight() - self.buffer.getStackHeight(i)-1)
                    acc.append(self.createDerivatative(None, NEW_COORD, CraneState.BUFFER))
            for i in range(self.ship.getWidth()):
                if self.ship.getStackHeight(i) > 0 and self.ship.getTopPhysicalCell(i).getState() != Condition.HULL:
                # to create a new ContainerCoordinate in the ship
                    NEW_COORD = Coordinate(i, self.ship.getHeight() - self.ship.getStackHeight(i) - 1)
                    acc.append(self.createDerivatative(None, NEW_COORD, CraneState.SHIP))
            acc.append(self.createDerivatative(None, NEW_COORD, CraneState.SHIP))
        
        elif self.craneState == CraneState.TRUCKBAY:
            for i in range(self.buffer.get_width()):
                if self.buffer.get_stack_height(i) > 0:
                    new_coord = Coordinate(i, self.buffer.get_height() - self.buffer.get_stack_height(i) - 1)
                    acc.append(self.create_derivative(None, new_coord, self.BufferLocation()))

            for i in range(self.ship.get_width()):
                if self.ship.get_stack_height(i) > 0 and self.ship.get_top_physical_cell(i).get_state() != Condition.HULL:
                    new_coord = Coordinate(i, self.ship.get_height() - self.ship.get_stack_height(i) - 1)
                    acc.append(self.create_derivative(None, new_coord, self.ShipLocation()))

            if len(self.toLoad):
                to_move = self.toLoad[-1][1]
                new_to_load = self.toLoad[:-1]
                for i in range(self.buffer.get_width()):
                    if self.buffer.get_stack_height(i) < self.buffer.get_height() - 1:
                        new_coord = Coordinate(i, self.buffer.get_height() - self.buffer.get_stack_height(i) - 1)
                        acc.append(self.create_derivative(to_move, new_coord, self.BufferLocation()))

                for i in range(self.ship.get_width()):
                    if self.ship.get_stack_height(i) < self.ship.get_height() - 1:
                        new_coord = Coordinate(i, self.ship.get_height() - self.ship.get_stack_height(i) - 1)
                        acc.append(self.create_derivative(to_move, new_coord, self.ShipLocation()))
        else:
            raise ValueError(5)
        return acc
                    
            
    def toStringBasic(self):
        pass


#class Transfer extends Port
class Transfer(Port):
    #shipload is a list of pairs that contain (Cell, Coordinate)
    def __init__(self, shipSize, bufferSize, shipLoad, toLoad):
        Port.__init__(self, shipSize, bufferSize)
        self.toOffload = []
        self.toLoad = []
        self.toStay = []
        for i in range(len(shipLoad)):
            CO = Coordinate(shipLoad[i][1])
            CELL = Cell(shipLoad[i][0])
            if CELL.getState().name == "HULL":
                self.ship.setAsHull(CO.x, CO.y)
            elif CELL.getState().name == "OCCUPIED":
                self.ship.setAsOccupied(CO.x, CO.y, CELL.getContainer())
            else:
                raise Exception("Invalid state")
            if CELL.getState().name == "OCCUPIED" and CELL.getContainer().isToBeOffloaded():
                containerToOffload = (ContainerCoordinate(CO.x, CO.y), CELL.getContainer())
                self.toOffload.append(containerToOffload)
            elif CELL.getState().name == "OCCUPIED" and not CELL.getContainer().isToBeOffloaded():
                containerToStay = (ContainerCoordinate(CO.x, CO.y), CELL.getContainer())
                self.toStay.append(containerToStay)
        self.toLoad = [(ContainerCoordinate(-1, -1), c) for c in toLoad]
    
    
    def toStringBasic(self):
        pass  # implementation to be added
    
    def calculateHeuristic(self):
        # this is just the remaining number of containers that need to load. Will just
        # assume all containers can just phase through one another
        minutesToLoad = len(self.toLoad) * 2

        # this is the remaining number of containers that need to offload
        # thanks to how we defined the coordinate system the manhattan distance is
        # calculated the same for both the ship and buffer
        minutesToOffload = 0
        for p in self.toOffload:
            coord = p[0]
            minutesToOffload += 2 + coord.x + coord.y

        # for the edge case of having a container in the buffer that needs to be put
        # back onto the ship. If the container that needs to stay on the ship is already
        # on the ship, the heuristic for that will be 0
        minutesToMoveFromBufferToShip = 0
        for p in self.toStay:
            coord = p[0]
            if coord.isInBuffer:
                minutesToMoveFromBufferToShip += 4 + coord.x + coord.y

        # okay heuristic to be finetuned. Can certainly be better
        # TODO: finetune
        lowerBoundTimeLeft = minutesToLoad + minutesToOffload + minutesToMoveFromBufferToShip
        if lowerBoundTimeLeft == 0:
            self.solved = True
        return lowerBoundTimeLeft

    
    def moveContainerAndCrane(self, container, start, end, startSpace, endSpace):
        # just moving the crane
        if container is None:
            # another sanity check
            if endSpace == CraneState.SHIP:
                if self.ship.getCellState(end.x, end.y) != CraneState.OCCUPIED:
                    raise Exception(5)
            elif endSpace == CraneState.BUFFER:
                if self.buffer.getCellState(end.x, end.y) != CraneState.OCCUPIED:
                    raise Exception(5)
            self.cranePosition = end
            self.craneState = endSpace
            self.moveDescription += f"\nMoving crane only from {self.toStringFromState(startSpace)} {start.toString()} to {self.toStringFromState(endSpace)} {end.toString()}"
        # moving the crane and the container
        else:
            self.cranePosition = end
            self.craneState = endSpace
            # add container at end
            if endSpace == CraneState.BUFFER:
                self.buffer.addContainer(end.x, end.y, container)
            elif endSpace == CraneState.SHIP:
                self.ship.addContainer(end.x, end.y, container)
            self.updateContainerCoordinateVectors(container, end, endSpace)
            # remove container at beginning
            if startSpace == CraneState.BUFFER:
                self.buffer.removeContainer(start.x, start.y)
            elif startSpace == CraneState.SHIP:
                self.ship.removeContainer(start.x, start.y)
            self.moveDescription += f"\nMoving container {container.toString()} from {self.toStringFromState(startSpace)} {start.toString()} to {self.toStringFromState(endSpace)} {end.toString()}"

        
    
    def create_derivative(self, container, end, end_space):
        # Create a copy of the current transfer state
        deriv = Transfer(self)
        deriv.parent = self.parent
        deriv.move_description = self.move_description
        
        # Calculate the manhattan distance between the crane's current position and the end position
        translation_move = self.calculate_manhattan_distance(self.crane_position, end, self.crane_state, end_space)
        
        # Move the crane and container to the specified end coordinates and update the transfer state
        deriv.move_container_and_crane(container, self.crane_position, end, self.crane_state, end_space)
        
        # Update the cost to get to this new state and calculate the A* heuristic
        deriv.cost_to_get_here += translation_move
        deriv.calculate_a_star()
        
        # Return the new transfer state
        return deriv

    
    def updateContainerCoordinateVectors(self, container, newPosition, newSpace):
        if container.isToBeOffloaded():
            # search for toOffload
            for i, (coord, c) in enumerate(self.toOffload):
                if c == container:
                    # is the offloaded container now in the trucks?
                    if newSpace == CraneState.TRUCKBAY:
                        self.toOffload.pop(i)
                        return

                    new_coord = ContainerCoordinate(newPosition.x, newPosition.y)
                    new_coord.isInBuffer = (newSpace == CraneState.BUFFER)

                    self.toOffload[i] = (new_coord, container)
                    return
            # did not find the appropriate container, throw exception
            raise Exception("Could not find offloaded container")
        else:
            # search for toStay
            for i, (coord, c) in enumerate(self.toStay):
                if c == container:
                    new_coord = ContainerCoordinate(newPosition.x, newPosition.y)
                    new_coord.isInBuffer = (newSpace == CraneState.BUFFER)

                    self.toStay[i] = (new_coord, container)
                    return
            # did not find the new container, so will add to toStay
            # assuming it was properly pulled from
            new_coord = ContainerCoordinate(newPosition.x, newPosition.y)
            new_coord.isInBuffer = (newSpace == CraneState.BUFFER)
            toAdd = (new_coord, container)
            self.toStay.append(toAdd)







