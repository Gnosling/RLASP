class FrozenLakeLevel:

    """
    Super-class of all frozen lake-levels. Syntax of start and states is analog to .mdp.frozenlake.lp
    """
    def __init__(self, start: set[str], width: int, height: int, states: set[str]):
        self.start = start
        self.width = width
        self.height = height
        self.states = states
