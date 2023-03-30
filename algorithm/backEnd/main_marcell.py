from container import Container
from cell import Cell, Condition
from port import Transfer
from coordinate import Coordinate


# reads manifest and uploads container vals
# substantially done by Nishitha
def read_manifest(file) -> list:
    containers = []
    manifest = open(file, 'r')
    while True:
        line = manifest.readline()
        if not line:
            break
        line = line.strip()
        # name
        name = (line[18:])
        # x and y coords
        # need to transform coordinate system
        x = int(line[1:3]) + 1
        y = 9 - int(line[4:6])
        # weight
        w = int(line[10:15])
        if name == "NAN":
            containers.append((Cell(Condition.HULL), Coordinate(x, y)))
        elif name != "UNUSED":
            print("Ship has container named <" + name + ">")
            containers.append((Cell(Condition.OCCUPIED, Container(name, w)), Coordinate(x, y)))
    return containers


ship_load = read_manifest(input("Type in the name of the manifest file:\n"))
while int(input("Type 1 to select a container to offload from ship (or 2 to continue to the next step):\n")) == 1:
    container_name = input("Type in precisely the name of the container you wish to offload:\n")
    found: bool = False
    for i in range(len(ship_load)):
        if ship_load[i][0].state == Condition.OCCUPIED:
            if ship_load[i][0].container.description == container_name and not ship_load[i][0].container.to_offload:
                found = True
                ship_load[i][0].container.to_offload = True
                break
    if not found:
        print("Could not find container <" + container_name + "> which has not already been marked to offload")
to_load = []
while int(input("Type 1 to input a container name (or type 2 to begin Transfer calculations:\n")) == 1:
    to_load.append(Container(input("Enter the name of the container:\n"), -1))
t = Transfer(Coordinate(12, 9), Coordinate(24, 5), ship_load, to_load)
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
    if len(stack) % 40 == 0:
        print(str(int(stack[-1].cost_to_get_here / stack[-1].a_star_cost * 100))+"%")
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

steps = []
recurse: Transfer = solution
while recurse is not None:
    steps.append(recurse)
    recurse = recurse.parent
steps.reverse()
for element in steps:
    acc = ""
    sequences = element.move_sequence.generate_animation_sequence()
    for i in sequences:
        acc += str(i) + " "
    print(element.move_description)
    print(acc)
print(str(solution.cost_to_get_here) + " minutes")
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
