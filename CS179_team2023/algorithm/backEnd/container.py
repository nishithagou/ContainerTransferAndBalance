class Container:

    ##added x and y coords, dont't have to use them but they're helpful for animation
    def __init__(self, description, weight, x, y, toOffload=False):
        self.weight = weight
        self.description = description
        self.x = x
        self.y = y
        self.toOffload = toOffload

    def getDescription(self):
        return self.description

    def toString(self):
        return self.description + " (weight: " + str(self.weight) + ")" + " Coords: (" + str(self.x) + "," + str(self.y) + ")"

    def getWeight(self):
        return self.weight

    def isToBeOffloaded(self):
        return self.toOffload
