from port import SIFT
from cell import Cell, Container, Condition
from coordinate import Coordinate, ContainerCoordinate

ship_load = [(Cell(Condition.OCCUPIED, Container("Meow", 10)), Coordinate(0, 8)),
             (Cell(Condition.OCCUPIED, Container("Puff", 84)), Coordinate(1, 8)),
             (Cell(Condition.OCCUPIED, Container("Ruff", 10)), Coordinate(2, 8)),
             (Cell(Condition.OCCUPIED, Container("Beep", 10)), Coordinate(3, 8))]
s = SIFT(Coordinate(12, 9), Coordinate(24, 5), ship_load)
solution_state: dict = s.unique_weights
coords = solution_state[10]
for element in coords:
    print(str(element))
