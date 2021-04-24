from .frozen_lake_level import FrozenLakeLevel

"""
Fixed 4x4-level for a frozen-lake:
      _____________
      |S  F  F  F |
      |F  H  F  H |
      |F  F  F  H |
      |H  F  F  G |
      |___________|
Whereby: 
    S = START
    F = FROZEN
    H = HOLE
    G = GOAL
    (S and G must be frozen)
"""
class FrozenLakeLevel4x4_A(FrozenLakeLevel):

    def __init__(self):
        # TODO: im .lp ist length = width --> ändern?
        states = {"position(0..15)",
                  "frozen(0)", "frozen(1)", "frozen(2)", "frozen(3)",
                  "frozen(4)", "hole(5)", "frozen(6)", "hole(7)",
                  "frozen(8)", "frozen(9)", "frozen(10)", "hole(11)",
                  "hole(12)", "frozen(13)", "frozen(14)", "frozen(15)",
                  "#const goal = 15", "#const length = 4",
                  "leftEdge(0)", "leftEdge(4)", "leftEdge(8)", "leftEdge(12)",
                  "rightEdge(3)", "rightEdge(7)", "rightEdge(11)", "rightEdge(15)",
                  "upperEdge(0..3)", "lowerEdge(12..15)"
                  }
        start = {"currentPosition(0)"}
        width = 4
        height = 4
        super().__init__(start, width, height, states)
