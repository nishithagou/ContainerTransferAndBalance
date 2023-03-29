class Container:
    # static variable
    static_id: int = 0

    # added x and y coords, don't have to use them but they're helpful for animation
    def __init__(self, description: str, weight: int, to_offload: bool = False):
        self.weight = weight
        self.description = description
        self.id: int = Container.static_id
        Container.static_id = Container.static_id + 1
        self.to_offload = to_offload

    # basically equivalent to toString without having to type out toString
    def __str__(self) -> str:
        return self.description + " (weight: " + str(self.weight) + " kg)"
