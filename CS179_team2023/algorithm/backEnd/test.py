#going to test all the classes

from container import Container
import cell
from enum import Enum
from space import Space
import coordinate
from cell import Cell
from coordinate import ContainerCoordinate
from coordinate import Coordinate
from cell import Condition

print('test.py is running: testing begins for all classes')


#1. space class
# hardcoding file for testing
#testing Cell
cellTest = Space(3,2)
#print("Height:" , cellTest.height)
#print("width:" , cellTest.width)
count = 0

print('cellTest.cells: ', cellTest.cells[0])