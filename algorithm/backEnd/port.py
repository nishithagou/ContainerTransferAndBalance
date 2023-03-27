from enum import Enum
from abc import ABC, abstractmethod
from coordinate import Coordinate, ContainerCoordinate
from cell import Cell, Condition
from space import Space


class CraneState(Enum):
    SHIP = 1
    BUFFER = 2
    TRUCKBAY = 3


class Port(ABC):

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

    def __eq__(self, rhs) -> bool:
        if self.craneState != rhs.craneState:
            return False
        if self.cranePosition != rhs.cranePosition:
            return False
        # find the first thing that is unequal
        # go through the ship's space
        for row in range(self.ship.height):
            for col in range(self.ship.width):
                if rhs.ship.cells[col][row] != self.ship.cells[col][row]:
                    return False
        # then the buffer's space room for optimization
        for row in range(self.buffer.height):
            for col in range(self.buffer.width):
                if rhs.buffer.cells[col][row] != self.buffer.cells[col][row]:
                    return False
        return True

    def __lt__(self, other) -> bool:
        return self.aStarCost < other.aStarCost

    def __gt__(self, other) -> bool:
        return self.aStarCost > other.aStarCost

    def calculate_a_star(self):
        self.aStarCost = self.costToGetHere + self.calculate_heuristic()

    def get_move_description(self) -> str:
        return self.moveDescription

    def is_solved(self) -> bool:
        return self.solved

    @abstractmethod
    def calculate_heuristic(self):
        pass

    # start and end coordinates are inclusive
    def calculate_manhattan_distance(self, start: Coordinate, end: Coordinate,
                                     start_space: Condition, end_space: Condition):
        if start_space == end_space:
            # Are we in the buffer or ship?

            curr_space = self.ship
            if start_space == CraneState.BUFFER:
                curr_space = self.buffer

            # Actually the most complicated to calculate
            to_move_x = start.x - end.x

            if to_move_x > 0:
                # Need to decrement x

                # Find the smallest value of min_clearance
                min_depth = curr_space.min_clearance[start.x - 1]
                for x in range(start.x-1, end.x-1, -1):
                    if min_depth <= curr_space.min_clearance[x]:
                        min_depth = curr_space.min_clearance[x]
                return (start.y - min_depth) + to_move_x + (end.y - min_depth)
            elif to_move_x < 0:
                # Need to increment x
                min_depth = start.y
                for x in range(start.x - 1, end.x - 1, -1):
                    if min_depth <= curr_space.min_clearance[x]:
                        min_depth = curr_space.min_clearance[x]
                return (start.y - min_depth) + (-to_move_x) + (end.y - min_depth)
            else:
                # Why are you trying to move within the same column?
                raise ValueError("Trying to move within the same column")
        # This is an "interspace" transfer so like moving between the buffer/ship/truckbay
        # Actually made easier since the crane always has to go up to 0,0 coordinate
        else:
            if start_space == CraneState.TRUCKBAY and end_space == CraneState.TRUCKBAY:
                # Illogical move, throw error
                raise ValueError("Trying to move within the same truckbay")
            # Quite trivial
            if start_space == CraneState.TRUCKBAY:
                return end.x + end.y + 2
            if end_space == CraneState.TRUCKBAY:
                return start.x + start.y + 2
            # Only dealing with distance between ship and buffer also pretty trivial
            return start.x + start.y + end.x + end.y + 4

    @staticmethod
    def to_string_from_state(state: CraneState) -> str:
        if state == CraneState.SHIP:
            return "Ship"
        elif state == CraneState.BUFFER:
            return "Buffer"
        elif state == CraneState.TRUCKBAY:
            return "Truck Bay"
        else:
            raise ValueError("Invalid state")

    @abstractmethod
    def try_all_operators(self) -> []:
        pass
                    
    @abstractmethod
    def __str__(self):
        pass


# class Transfer extends Port
class Transfer(Port):
    # shipload is a list of pairs that contain (Cell, Coordinate)
    def __init__(self, ship_size: Coordinate, buffer_size: Coordinate, ship_load: list, to_load: list):
        Port.__init__(self, ship_size, buffer_size)
        self.to_offload = []
        self.to_load = to_load
        self.to_stay = []
        for i in range(len(ship_load)):
            # apparently Python struggles
            co = ship_load[i][1]
            cell = Cell(ship_load[i][0])
            if cell.state == Condition.HULL:
                self.ship.set_as_hull(co.x, co.y)
            elif cell.state == Condition.OCCUPIED:
                self.ship.add_container(co.x, co.y, cell.container)
            else:
                raise Exception("Invalid state. Don't try adding Empty cells to the shipload")
            if cell.state == Condition.OCCUPIED and cell.container.to_offload:
                container_to_offload = (co, cell.container)
                self.toOffload.append(containerToOffload)
            elif CELL.getState().name == "OCCUPIED" and not CELL.getContainer().isToBeOffloaded():
                containerToStay = (ContainerCoordinate(CO.x, CO.y), CELL.getContainer())
                self.toStay.append(containerToStay)
    
    
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

    def try_all_operators(self) -> []:
        CRANE_COLUMN = self.cranePosition.x
        acc = []

        if self.craneState == CraneState.SHIP:
            if self.cranePosition == Coordinate(0, 0):
                for i in range(self.ship.getWidth()):
                    if self.ship.getStackHeight(i) > 0 and self.ship.getTopPhysicalCell(
                            i).getState() != Condition.Hull and i != CRANE_COLUMN:
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
                    if self.ship.getStackHeight(i) > 0 and self.ship.getTopPhysicalCell(
                            i).getState() != Condition.Hull and i != CRANE_COLUMN:
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
                    NEW_COORD = Coordinate(i, self.buffer.getHeight() - self.buffer.getStackHeight(i) - 1)
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
                if self.ship.get_stack_height(i) > 0 and self.ship.get_top_physical_cell(
                        i).get_state() != Condition.HULL:
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
            raise Exception("Error: Crane is in an invalid state")
        return acc





