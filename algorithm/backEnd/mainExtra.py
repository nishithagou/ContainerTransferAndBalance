from container import Container

from enum import Enum
from space import *
import copy
from coordinate import *
from cell import *
from typing import List, Tuple, Deque, Set
from collections import deque
from port import *


print (" * message : main.py was compiled")



#cell1= Cell(state_Current,container_Current)
#space1 = Space(3,5)
#space1.addContainer(2,4,6)
#Container.toString()
#hardcoding file for testing
'''
def read_manifest():
    containers = []
    manifest = open('ShipCase3.txt', 'r')
    while True:
        line = manifest.readline()
        if not line:
            break
        line = line.strip()
        #name
        name=(line[18:])
        #x and y coords
        x=int(line[1:3])
        y=int(line[4:6])
        #weight
        w=int(line[10:15])
        containers.append(Container(name,w,x,y))
    return containers

x = read_manifest()
#for cont in x:
#   print(cont.weight)
'''

'''
if __name__ == '__main__':
    # some hardcoded values to be added
    shipLoad = []
    allContainers = []
    hull = Cell('HULL')
    for i in range(4):
        hullSpot = (hull, Coordinate(0, 8-i))
        shipLoad.append(hullSpot)
        hullSpot2 = (hull, Coordinate(11, 8-i))
        shipLoad.append(hullSpot2)
        allContainers.append(Container("Container Ld " + str(i), 100+i))
        containerSpot = (Cell(allContainers[-1]), Coordinate(1, 8-i))
        shipLoad.append(containerSpot)
    allContainers.append(Container("Container to Offload", 420, True))
    toAdd = (Cell(allContainers[-1]), Coordinate(2, 8))
    shipLoad.append(toAdd)
    toLoad = [Container("From truck 1", 100), Container("From truck 2", 200)]
    

    stack = deque()
    base = Transfer(Coordinate(12,9), Coordinate(24, 5), shipLoad, toLoad)
    history = set()
    history.add(base.toStringBasic())
    stack.append(base)
    solution = None
    while stack:
        if stack[-1].isSolved():
            solution = stack[-1]
            break

        # expand cheapest node
        derivs = stack[-1].tryAllOperators()
        print("Best Node so Far: ")
        print(stack[-1].toStringBasic())
        stack.pop()

        # look through derivs
        for port in derivs:
            if port.toStringBasic() in history:
                if port == derivs[0]:
                    derivs.popleft()
                elif port == derivs[-1]:
                    derivs.pop()
                else:
                    derivs.remove(port)
            else:
                stack.append(port)

        # sort
        stack.sort(reverse=True, key=lambda x: x.greaterThan())
    
    print(solution.getMoveDescription())


'''


#testing Cell
cellTest = Space(3,2)
print("Height:" , cellTest.height)
print("width:" , cellTest.width)
count = 0

print(cellTest.cells[0][1])
