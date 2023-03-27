class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # type hinting with these methods seems to be complaining
    def __ne__(self, other):
        return (self.x != other.x) or (self.y != other.y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def to_string(self):
        return "({}, {})".format(self.x, self.y)


class ContainerCoordinate(Coordinate):
    def __init__(self, x, y, is_in_buffer=False):
        super().__init__(x, y)
        self.is_in_buffer = is_in_buffer

        # print("* msg: ContainerCoordinate() was called")
