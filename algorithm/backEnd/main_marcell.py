from space import Space
from container import Container
from cell import Cell, Condition
from port import Transfer
from coordinate import Coordinate


ship_load = [(Cell(Condition.OCCUPIED, Container("Meow", 5, True)), Coordinate(0, 8)),
             (Cell(Condition.OCCUPIED, Container("Puff", 8, True)), Coordinate(1, 8)),
             (Cell(Condition.OCCUPIED, Container("Ruff", 10, True)), Coordinate(2, 8)),
             (Cell(Condition.OCCUPIED, Container("Beep", 7, True)), Coordinate(3, 8))]
to_load = [Container("Truck Load 1", -1), Container("Truck Load 2", -1)]
t = Transfer(Coordinate(4, 9), Coordinate(1, 2), ship_load, to_load)
print(str(t))
history = {str(t)}
stack = [t]
solution: Transfer = t
while len(stack) > 0:
    if stack[-1].solved:
        print("Found solution")
        solution = stack[-1]
        break
    derivs = stack[-1].try_all_operators()
    stack.pop()
    for deriv in derivs:
        if str(deriv) in history:
            derivs.remove(deriv)
        else:
            stack.append(deriv)
            history.add(str(deriv))
    stack.sort(reverse=True)
    # if len(stack) % 100 == 0:
    #     print(str(stack[-1]))
    #     print(str(len(stack)))

recurse: Transfer = solution
while recurse is not None:
    print(str(recurse))
    print(str(recurse.move_description))
    recurse = recurse.parent
print(str(solution.cost_to_get_here))
print(str(len(stack)) + " " + str(len(history)))
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
