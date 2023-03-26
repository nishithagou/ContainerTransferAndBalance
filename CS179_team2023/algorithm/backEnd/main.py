from container import Container
from cell import Cell
from enum import Enum
from space import Space
import copy
#manifest.txt info: [row,col], weightInfo, containerName

print (" * message : main.py was compiled")

state_Current= 'nonEmpty!'
container_Current = "claire"

cell1= Cell('nonEmpty','dog')
space1 = Space(3,5)
space1.addContainer(2,4,6)

Container.toString() 

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