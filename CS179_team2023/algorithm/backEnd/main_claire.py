from container import Container
from cell import Cell
from enum import Enum
from space import Space
import copy



print (" * message : main.py was compiled")

state_Current= 'nonEmpty'
container_Current = "claire"

cell1= Cell(state_Current,container_Current)
space1 = Space(3,5)
space1.addContainer(2,4,6)

Container.toString()
