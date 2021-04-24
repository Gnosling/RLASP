from .frozen_lake_level import FrozenLakeLevel

"""
Fixed 5x5-level for a frozen-lake:
      _______________
      |S  F  H  F  G|
      |F  F  F  F  F|
      |F  F  H  F  F|
      |F  F  F  F  F|
      |F  F  F  F  F|
      |_____________|
Whereby: 
    S = START
    F = FROZEN
    H = HOLE
    G = GOAL
    (S and G must be frozen)
"""
class FrozenLakeLevel5x5_A(FrozenLakeLevel):

    def __init__(self):
        # TODO: im .lp ist length = width --> ändern?
        states = {"position(0..24)",
                  "frozen(0..1)", "hole(2)", "frozen(3..4)",
                  "frozen(5..9)",
                  "frozen(10..11)", "hole(12)", "frozen(13..14)",
                  "frozen(15..19)",
                  "frozen(20..24)"
                  "#const goal = 4", "#const length = 5",
                  "leftEdge(0)", "leftEdge(5)", "leftEdge(10)", "leftEdge(15)", "leftEdge(20)"
                  "rightEdge(4)", "rightEdge(9)", "rightEdge(14)", "rightEdge(19)", "rigthEdge(24)"
                  "upperEdge(0..4)", "lowerEdge(20..24)"
                  }
        start = {"currentPosition(0)"}
        width = 5
        height = 5
        super().__init__(start, width, height, states)
