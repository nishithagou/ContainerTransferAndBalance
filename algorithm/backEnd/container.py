class Container:

    # this class works

    # added x and y coords, don't have to use them but they're helpful for animation
    def __init__(self, description, weight, to_offload=False):
        self.weight = weight
        self.description = description
        # self.x = x
        # self.y = y
        self.to_offload = to_offload

    def to_string(self):
        return self.description + " (weight: " + str(self.weight) + " kg)"
