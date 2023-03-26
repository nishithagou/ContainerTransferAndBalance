from container import Container
import cell
from enum import Enum
from space import Space
import copy

print (" * message : main.py was compiled")

state_Current= 'nonEmpty'
container_Current = "claire"

#cell1= Cell(state_Current,container_Current)
#space1 = Space(3,5)
#space1.addContainer(2,4,6)
#Container.toString()
#hardcoding file for testing

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

#testing Cell
cellTest = Space(3,2)
#print("Height:" , cellTest.height)
#print("width:" , cellTest.width)
count = 0

print(cellTest.cells[0])



