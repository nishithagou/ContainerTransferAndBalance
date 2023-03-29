# space is representaive of the entire ship + buffer
# basically the whole frame
from cell import Cell
from cell import Condition
from container import Container

# did not add the assignment and noteq functions at end. are they necessary?


class Space:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = [[Cell(Condition.EMPTY) for _ in range(height)] for _ in range(width)]
        # instead of stack heights we are going to be using min_clearance
        # which stands for minimum clearance in other words what is the index which points to
        # the "top"
        self.min_clearance = [height - 1] * width

        for i in range(width):
            self.cells[i][0] = Cell(Condition.UNOCCUPIABLE)

    def get_cell_state(self, col: int, row: int) -> Condition:
        return self.cells[col][row].state

    def set_as_hull(self, col: int, row: int):
        if row <= self.min_clearance[col]:
            self.min_clearance[col] = row - 1
        self.cells[col][row].state = Condition.HULL

    def add_container(self, col: int, row: int, container: Container):
        if self.cells[col][row].state is not Condition.EMPTY:
            raise Exception("Error: adding a container to a nonempty cell")
        
        else:
            self.cells[col][row].state = Condition.OCCUPIED
            self.cells[col][row].container = container
            if row <= self.min_clearance[col]:
                # presume row 7 occupied and adding row 8
                self.min_clearance[col] = row - 1

    def remove_container(self, col: int, row: int):
        if self.cells[col][row].state is not Condition.OCCUPIED:
            raise Exception("Error: Trying to remove a container from a cell which has no container")
        self.cells[col][row].state = Condition.EMPTY
        self.min_clearance[col] = self.min_clearance[col] + 1

    # way nicer logic with min_clearance than with stack heights
    def get_top_physical_cell(self, col: int) -> Cell:
        if self.min_clearance[col] == self.height - 1:
            # no physical cell so return the empty cell
            return Cell()
        return self.cells[col][self.min_clearance[col] + 1]
