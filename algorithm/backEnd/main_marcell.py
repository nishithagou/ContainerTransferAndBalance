from space import Space
from container import Container
from cell import Cell, Condition
from port import Transfer
from coordinate import Coordinate


ship_load = [(Cell(Condition.HULL), Coordinate(0, 8)), (Cell(Condition.HULL), Coordinate(11, 8)),
             (Cell(Condition.OCCUPIED, Container("Meow", 5, True)), Coordinate(1, 8)),
             (Cell(Condition.OCCUPIED, Container("Ruff", 10, False)), Coordinate(1, 7)),
             (Cell(Condition.OCCUPIED, Container("Beep", 7, True)), Coordinate(10, 8))]
to_load = []  # = [Container("Truck Load 1", -1), Container("Truck Load 2", -1)]
t = Transfer(Coordinate(12, 9), Coordinate(1, 5), ship_load, to_load)
history = {str(t)}
stack = [t]
solution: Transfer
while len(stack) > 0:
    if stack[-1].solved:
        print("Found solution")
        solution = stack[-1]
    derivs = stack[-1].try_all_operators()
    for deriv in derivs:
        print(str(deriv.a_star_cost))
        print(str(deriv))
    stack.pop()
    for deriv in derivs:
        if str(deriv) in history:
            if deriv is derivs[0]:
                derivs.popleft()
                continue
            elif deriv is derivs[-1]:
                derivs.pop()
                break
            derivs.remove(deriv)
        else:
            stack.append(deriv)
    stack.sort(reverse=True)

# for i in range(cells.__len__()):
#     acc = ""
#     for j in range(cells[0].__len__()):
#         acc += str(cells[i][j]) + " "
#     print(acc)
#
# for i in range(cells.__len__()):
#     acc = ""
#     for j in range(cells[0].__len__()):
#         acc += str(cells[i][j]) + " "
#     print(acc)
