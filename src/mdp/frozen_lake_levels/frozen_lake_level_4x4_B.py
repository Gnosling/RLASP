from .frozen_lake_level import FrozenLakeLevel

"""
Fixed 4x4-level for a frozen-lake:
      _____________
      |S  F  F  F |
      |H  F  F  F |
      |H  H  F  F |
      |H  H  H  G |
      |___________|
Whereby: 
    S = START
    F = FROZEN
    H = HOLE
    G = GOAL
    (S and G must be frozen)
"""
class FrozenLakeLevel4x4_B(FrozenLakeLevel):

    def __init__(self):
        # TODO: im .lp ist length = width --> ändern?
        states = {"position(0..15)",
                  "frozen(0..3)",
                  "hole(4)", "frozen(5..7)",
                  "hole(8..9)", "frozen(10..11)",
                  "hole(12..14)", "frozen(15)",
                  "#const goal = 15", "#const length = 4",
                  "leftEdge(0)", "leftEdge(4)", "leftEdge(8)", "leftEdge(12)",
                  "rightEdge(3)", "rightEdge(7)", "rightEdge(11)", "rightEdge(15)",
                  "upperEdge(0..3)", "lowerEdge(12..15)"
                  }
        start = {"currentPosition(0)"}
        width = 4
        height = 4
        super().__init__(start, width, height, states)
