from port import SIFT
from cell import Cell, Container, Condition
from coordinate import Coordinate, ContainerCoordinate

ship_load = [(Cell(Condition.OCCUPIED, Container("Meow", 5, True)), Coordinate(0, 8)),
             (Cell(Condition.OCCUPIED, Container("Puff", 8, True)), Coordinate(1, 8)),
             (Cell(Condition.OCCUPIED, Container("Ruff", 10, True)), Coordinate(2, 8)),
             (Cell(Condition.OCCUPIED, Container("Beep", 7, True)), Coordinate(3, 8))]
s = SIFT(Coordinate(12, 9), Coordinate(24, 5), ship_load)
solution_state = s.unique_weights
