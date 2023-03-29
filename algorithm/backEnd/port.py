from enum import Enum
import copy
from abc import ABC, abstractmethod
from coordinate import Coordinate, ContainerCoordinate
from cell import Cell, Condition
from space import Space
from container import Container


class CraneState(Enum):
    SHIP = 1
    BUFFER = 2
    TRUCKBAY = 3


class Port(ABC):

    def __init__(self, ship_size: Coordinate, buffer_size: Coordinate):
        # describes the move done; only to be modified in tryAllOperators
        self.move_sequence = list
        self.move_description = ""
        # parent describes how the Port is derived from
        self.parent = None
        self.crane_position = Coordinate(0, 0)
        self.crane_state = CraneState.SHIP
        # the number of minutes it took to reach this Port i.e. g(n)
        self.cost_to_get_here = 0
        # The lower bound number of minutes it has taken and will take for the Port to finish
        self.a_star_cost = 0
        self.solved = False
        self.ship = Space(ship_size.x, ship_size.y)
        self.buffer = Space(buffer_size.x, buffer_size.y)

    def __eq__(self, rhs) -> bool:
        if self.crane_state != rhs.crane_state:
            return False
        if self.crane_position != rhs.crane_position:
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
        return self.a_star_cost < other.a_star_cost

    def __gt__(self, other) -> bool:
        return self.a_star_cost > other.a_star_cost

    def calculate_a_star(self):
        self.a_star_cost = self.cost_to_get_here + self.calculate_heuristic()

    def get_move_description(self) -> str:
        return self.move_description

    def is_solved(self) -> bool:
        return self.solved

    @abstractmethod
    def calculate_heuristic(self):
        pass

    # start and end coordinates are inclusive
    def calculate_manhattan_distance(self, start: Coordinate, end: Coordinate,
                                     start_space: CraneState, end_space: CraneState) -> int:
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
                if not(start_space == CraneState.SHIP and start == Coordinate(0, 0)):
                    # Why are you trying to move within the same column?
                    raise Exception("Trying to move within the same column")
                else:
                    return end.x + end.y
        # This is an "interspace" transfer so like moving between the buffer/ship/truckbay
        # Actually made easier since the crane always has to go up to 0,0 coordinate
        else:
            if start_space == CraneState.TRUCKBAY and end_space == CraneState.TRUCKBAY:
                # Illogical move, throw error
                raise Exception("Trying to move within the same truckbay")
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
            raise Exception(f"Invalid state: {CraneState}")

    @abstractmethod
    def try_all_operators(self) -> []:
        pass
                    
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def move_container_and_crane(self, container: Container, start: Coordinate, end: Coordinate,
                                 start_space: CraneState, end_space: CraneState):
        pass


# class SIFT extends Port
class SIFT(Port):
    def __init__(self, ship_size: Coordinate, buffer_size: Coordinate, ship_load: list):
        Port.__init__(self, ship_size, buffer_size)
        self.containers = list
        self.SIFT_solution = Space(ship_size.x, ship_size.y)
        # a weight yields a list of coordinates where the containers can go
        self.unique_weights = dict
        self.container_index = dict
        c_index = 65
        for i in range(len(ship_load)):
            cell = ship_load[i][0]
            co = ship_load[i][1]
            if cell.state == Condition.HULL:
                self.ship.set_as_hull(co.x, co.y)
                self.SIFT_solution.set_as_hull(co.x, co.y)
                # don't need to bother with checking with loads if we know a cell is the hull
                continue
            elif cell.state == Condition.OCCUPIED:
                self.ship.add_container(co.x, co.y, cell.container)
                self.containers.append((ContainerCoordinate(co.x, co.y), cell.container))
                self.container_index[cell.container.id] = chr(c_index)
                c_index = c_index + 1
        self.calculate_solution()

    def calculate_solution(self):
        # sort containers heaviest to lightest
        self.containers.sort(key= lambda x:x[1].weight, reverse=True)
        row: int = self.ship.height - 1
        # integer division
        col: int = self.ship.width // 2 - 1
        for i in range(len(self.containers)):
            while self.ship.get_cell_state(col, row) == Condition.HULL:
                if col == self.ship.width - 1:
                    row = row - 1 # reset column
                    col = self.ship.width // 2 - 1
                else:
                    if col <= self.ship.width // 2 - 1:
                        # flip to other side right side
                        col = self.ship.width - (col + 1)
                    else:
                        # flip to left side
                        col = (self.ship.width - (col + 1)) - 1
            c = self.containers[i][1]
            if self.unique_weights[c.weight] is None:
                self.unique_weights[c.weight] = [Coordinate(col, row)]
            else:
                self.unique_weights[c.weight].append(Coordinate(col, row))

    def calculate_heuristic(self) -> int:
        return 0

    def move_container_and_crane(self, container: Container, start: Coordinate, end: Coordinate,
                                 start_space: CraneState, end_space: CraneState):
        pass

    def try_all_operators(self) -> []:
        return list

    def __str__(self):
        acc = ""
        for col in range(self.buffer.width):
            for row in range(self.buffer.height):
                if self.buffer.get_cell_state(col, row) != Condition.OCCUPIED:
                    acc += "0"
                else:
                    acc += str(self.container_index[self.buffer.cells[col][row].container.id])
        return acc


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
            cell = ship_load[i][0]
            # Fill out the ship
            if cell.state == Condition.HULL:
                self.ship.set_as_hull(co.x, co.y)
                # don't need to bother with checking with loads if we know a cell is the hull
                continue
            elif cell.state == Condition.OCCUPIED:
                self.ship.add_container(co.x, co.y, cell.container)
            else:
                raise Exception("Invalid state. Don't try adding Empty cells to the shipload")
            # Fill out the vectors
            if cell.state == Condition.OCCUPIED and cell.container.to_offload:
                container_to_offload = (ContainerCoordinate(co.x, co.y), cell.container)
                self.to_offload.append(container_to_offload)
            elif cell.state == Condition.OCCUPIED and not cell.container.to_offload:
                container_to_stay = (ContainerCoordinate(co.x, co.y), cell.container)
                self.to_stay.append(container_to_stay)

    # for hashing
    def __str__(self) -> str:
        acc = ""
        for col in range(len(self.buffer.cells)):
            for row in range(len(self.buffer.cells[0])):
                if self.crane_state == CraneState.BUFFER and self.crane_position == Coordinate(col, row):
                    if self.buffer.cells[col][row] != Condition.OCCUPIED:
                        acc += "C"
                    else:
                        if self.buffer.cells[col][row].container.to_offload:
                            acc += "T"
                        else:
                            acc += "K"
                elif self.buffer.cells[col][row] != Condition.OCCUPIED:
                    acc += "0"
                else:
                    if self.buffer.cells[col][row].container.to_offload:
                        acc += "U"
                    else:
                        acc += "S"
            acc += "\n"
        if self.crane_state == CraneState.TRUCKBAY:
            acc += "C\n"
        else:
            acc += "0\n"
        # iterate through ship
        for col in range(len(self.ship.cells)):
            for row in range(len(self.ship.cells[0])):
                if self.crane_state == CraneState.SHIP and self.crane_position == Coordinate(col, row):
                    if self.ship.cells[col][row] != Condition.OCCUPIED:
                        acc += "C"
                    else:
                        if self.ship.cells[col][row].container.to_offload:
                            acc += "T"
                        else:
                            acc += "K"
                elif self.ship.cells[col][row] != Condition.OCCUPIED:
                    acc += "0"
                else:
                    if self.ship.cells[col][row].container.to_offload:
                        acc += "U"
                        # U for unload
                    else:
                        acc += "S"
                        # S for stay
            acc += "\n"
        return acc
    
    def calculate_heuristic(self) -> int:
        # this is just the remaining number of containers that need to load. Will just
        # assume all containers can just phase through one another
        minutes_to_load = len(self.to_load) * 2

        # this is the remaining number of containers that need to offload
        # thanks to how we defined the coordinate system the manhattan distance is
        # calculated the same for both the ship and buffer
        minutes_to_offload = 0
        for p in self.to_offload:
            coord = p[0]
            minutes_to_offload += 2 + coord.x + coord.y

        # for the edge case of having a container in the buffer that needs to be put
        # back onto the ship. If the container that needs to stay on the ship is already
        # on the ship, the heuristic for that will be 0
        minutes_to_move_from_buffer_to_ship = 0
        for p in self.to_stay:
            coord = p[0]
            # do not need to move containers that need to stay in the ship that are already
            # in the ship
            if coord.is_in_buffer:
                minutes_to_move_from_buffer_to_ship += 4 + coord.x + coord.y

        # okay heuristic to be fine-tuned. Can certainly be better
        pos = self.crane_position
        lower_bound_time_left = 0

        # Penalize poor crane placement
        # if self.crane_state == CraneState.TRUCKBAY:
        #     lower_bound_time_left += 2
        # elif self.crane_state == CraneState.SHIP and len(self.to_offload) > 0 and \
        #         not self.ship.cells[pos.x][pos.y].container.to_offload:
        #     lower_bound_time_left += 1
        #     # minimum movement to get to be an offloaded container
        # elif self.crane_state == CraneState.BUFFER and len(self.to_offload) > 0 and \
        #         not self.buffer.cells[pos.x][pos.y].container.to_offload:
        #     lower_bound_time_left += 1
        lower_bound_time_left += minutes_to_load + minutes_to_offload + minutes_to_move_from_buffer_to_ship
        if lower_bound_time_left == 0:
            self.solved = True
        return lower_bound_time_left

    def create_derivative(self, end: Coordinate, end_space: CraneState, container: Container = None):
        # Create a copy of the current transfer state
        deriv = copy.deepcopy(self)
        deriv.parent = self
        
        # Calculate the manhattan distance between the crane's current position and the end position
        translation_move = self.calculate_manhattan_distance(self.crane_position, end, self.crane_state, end_space)
        
        # Move the crane and container to the specified end coordinates and update the transfer state
        deriv.move_container_and_crane(container, self.crane_position, end, self.crane_state, end_space)

        # update the Transfer's internal vectors
        deriv.update_container_coordinate_vectors(container, end, end_space)

        # Update the cost to get to this new state and calculate the A* heuristic
        deriv.cost_to_get_here += translation_move
        deriv.calculate_a_star()
        
        # Return the new transfer state
        return deriv

    def iterate_through_space(self,  end_space: CraneState, container: Container = None) -> list:
        if end_space == CraneState.TRUCKBAY:
            raise Exception("Do not iterate adding containers to trucks. It's a O(1) operation")
        acc = []
        space = self.ship
        if end_space == CraneState.BUFFER:
            space = self.buffer
        # if there is no container move to a spot with a container
        if container is None:
            for col in range(space.width):
                if col == self.crane_position.x and end_space == self.crane_state and \
                        self.crane_position != Coordinate(0, 0):
                    continue
                if space.get_top_physical_cell(col).state == Condition.OCCUPIED:
                    end = Coordinate(col, space.min_clearance[col] + 1)
                    acc.append(self.create_derivative(end, end_space))
                    # do not need to simulate going to all spots in the buffer
                    if end_space == CraneState.BUFFER:
                        break
        else:
            for col in range(space.width):
                if col == self.crane_position.x and end_space == self.crane_state:
                    continue
                # make sure we're not at the UNOCCUPIABLE row
                if space.min_clearance[col] > 0:
                    end = Coordinate(col, space.min_clearance[col])
                    acc.append((self.create_derivative(end, end_space, container)))
                    # just simulate moving the container to the closest possible space in the buffer
                    if end_space == CraneState.BUFFER:
                        break
        return acc

    def try_all_operators(self) -> []:
        acc = []

        if self.crane_state == CraneState.SHIP:
            if self.crane_position == Coordinate(0, 0):
                # go from 0, 0 to all other Coordinates on the ship
                acc += self.iterate_through_space(CraneState.SHIP)

                if len(self.to_load) != 0:
                    acc.append(self.create_derivative(Coordinate(0, 0), CraneState.TRUCKBAY))
            else:
                if self.ship.get_cell_state(self.crane_position.x, self.crane_position.y) != Condition.OCCUPIED:
                    raise ValueError("Why is the crane is an invalid ship position at " + str(self.crane_position))

                # latch container
                to_move = self.ship.cells[self.crane_position.x][self.crane_position.y].container

                # do not bother trying to move the container to bunch of other spots if you could just offload it
                if to_move.to_offload:
                    acc.append(self.create_derivative(Coordinate(0, 0), CraneState.TRUCKBAY, to_move))
                    return acc

                # moving crane in ship to another spot in the ship
                acc += self.iterate_through_space(CraneState.SHIP)

                # moving crane in ship to another spot in the buffer
                acc += self.iterate_through_space(CraneState.BUFFER)

                # move crane itself to the trucks
                if len(self.to_load) != 0:
                    acc.append(self.create_derivative(Coordinate(0, 0), CraneState.TRUCKBAY))

                # moving container in ship to another spots in ship
                acc += self.iterate_through_space(CraneState.SHIP, to_move)

                # moving container in ship to another spots in buffer
                acc += self.iterate_through_space(CraneState.BUFFER, to_move)

        elif self.crane_state == CraneState.BUFFER:

            # did you put the crane to a pointless position
            if self.buffer.get_cell_state(self.crane_position.x, self.crane_position.y) != Condition.OCCUPIED:
                raise Exception("Invalid Buffer position sought at " + str(self.crane_position))
            # latch container
            to_move = self.buffer.cells[self.crane_position.x][self.crane_position.y].container

            # move container to truck bay don't bother with other combinations if to_offload is true
            if to_move.to_offload:
                acc.append(self.create_derivative(Coordinate(0, 0), CraneState.TRUCKBAY, to_move))
                return acc

            # moving container in buffer to another spots in ship
            acc += self.iterate_through_space(CraneState.SHIP, to_move)

            # moving crane in buffer to another spot in the buffer
            # pointless operation
            # acc += self.iterate_through_space(CraneState.BUFFER)

            # moving crane in buffer to another spot in the ship
            acc += self.iterate_through_space(CraneState.SHIP)

            # moving crane in buffer to the Truck bay
            if len(self.to_load) > 0:
                acc.append(self.create_derivative(Coordinate(0, 0), CraneState.TRUCKBAY))

        elif self.crane_state == CraneState.TRUCKBAY:

            # moving from truck bay to buffer with just the crane
            acc += self.iterate_through_space(CraneState.BUFFER)

            # moving from truck bay to ship with just the crane
            acc += self.iterate_through_space(CraneState.SHIP)

            if len(self.to_load) > 0:
                to_move = self.to_load[-1]

                # moving from truck bay to buffer with container
                acc += self.iterate_through_space(CraneState.BUFFER, to_move)

                # moving from truck bay to ship with container
                acc += self.iterate_through_space(CraneState.SHIP, to_move)
        else:
            raise Exception("Error: Crane is in an invalid state")
        return acc

    def update_container_coordinate_vectors(self, container: Container,
                                            new_position: Coordinate, new_space: CraneState):
        if container is None:
            return
        if container.to_offload:
            # search for toOffload
            for i, (coord, c) in enumerate(self.to_offload):
                # need to do a memory comparison and not a pure value one like with
                # Failed memory comparison will need to use some id system
                if c.id == container.id:
                    # is the offloaded container now in the trucks?
                    if new_space == CraneState.TRUCKBAY:
                        self.to_offload.pop(i)
                        return

                    new_coord = ContainerCoordinate(new_position.x, new_position.y)
                    new_coord.is_in_buffer = (new_space == CraneState.BUFFER)

                    self.to_offload[i] = (new_coord, container)
                    return
            # did not find the appropriate container, throw exception
            raise Exception("Could not find offloaded container")
        else:
            # search for to_stay
            for i, (coord, c) in enumerate(self.to_stay):
                if c.id == container.id:
                    new_coord = ContainerCoordinate(new_position.x, new_position.y)
                    new_coord.is_in_buffer = (new_space == CraneState.BUFFER)

                    self.to_stay[i] = (new_coord, container)
                    return
            # did not find the new container, so will add to toStay
            # assuming it was properly pulled from to_load
            new_coord = ContainerCoordinate(new_position.x, new_position.y)
            new_coord.is_in_buffer = (new_space == CraneState.BUFFER)
            to_add = (new_coord, container)
            self.to_load.pop()
            self.to_stay.append(to_add)

    # no longer updates container vectors
    def move_container_and_crane(self, container: Container, start: Coordinate, end: Coordinate,
                                 start_space: CraneState, end_space: CraneState):
        # just moving the crane
        if container is None:
            # another sanity check
            if end_space == CraneState.SHIP:
                if self.ship.get_cell_state(end.x, end.y) != Condition.OCCUPIED:
                    raise Exception("Crane has moved into an non-occupied position in the ship")
            elif end_space == CraneState.BUFFER:
                if self.buffer.get_cell_state(end.x, end.y) != Condition.OCCUPIED:
                    raise Exception("Crane has moved into an non-occupied position in the buffer")
            self.crane_position = Coordinate(end.x, end.y)
            self.crane_state = copy.deepcopy(end_space)
            self.move_description = f"\nMoving crane only from {Port.to_string_from_state(start_space)} {str(start)} " \
                                    f"to {Port.to_string_from_state(end_space)} {str(end)}"
        # moving the crane and the container
        else:
            self.crane_position = Coordinate(end.x, end.y)
            self.crane_state = copy.deepcopy(end_space)
            # add container at end
            if end_space == CraneState.BUFFER:
                self.buffer.add_container(end.x, end.y, container)
            elif end_space == CraneState.SHIP:
                self.ship.add_container(end.x, end.y, container)
            # remove container at beginning
            if start_space == CraneState.BUFFER:
                self.buffer.remove_container(start.x, start.y)
            elif start_space == CraneState.SHIP:
                self.ship.remove_container(start.x, start.y)
            self.move_description = f"\nMoving container {str(container)} from " \
                                    f"{Port.to_string_from_state(start_space)} {str(start)} to " \
                                    f"{Port.to_string_from_state(end_space)} {str(end)}"
