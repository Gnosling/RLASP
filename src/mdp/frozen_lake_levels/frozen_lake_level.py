class FrozenLakeLevel:

    def __init__(self, start: set[str], width: int, height: int, states: set[str]):
        self.start = start
        self.width = width
        self.height = height
        self.states = states
