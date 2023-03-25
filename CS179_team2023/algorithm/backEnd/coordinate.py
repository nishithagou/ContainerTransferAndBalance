class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __ne__(self, other):
        return (self.x != other.x) or (self.y != other.y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def toString(self):
        return "({}, {})".format(self.x, self.y)

class ContainerCoordinate(Coordinate):
    def __init__(self, x, y, isInBuffer=False):
        super().__init__(x, y)
        self.isInBuffer = isInBuffer
