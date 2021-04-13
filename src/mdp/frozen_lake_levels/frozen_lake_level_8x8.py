from .frozen_lake_level import FrozenLakeLevel

"""
Fixed 8x8-level for a frozen-lake:
      ________________________
      |S  F  F  F  F  F  F  F|
      |F  F  F  F  F  F  F  F|
      |F  F  F  H  F  F  F  F|
      |F  F  F  F  F  H  F  F|
      |F  F  F  H  F  F  F  F|
      |F  H  H  F  F  F  H  F|
      |F  H  F  F  H  F  H  F|
      |F  F  F  H  F  F  F  G|
      |______________________|
Whereby: 
    S = START
    F = FROZEN
    H = HOLE
    G = GOAL
    (S and G must be frozen)
"""
class FrozenLakeLevel8x8(FrozenLakeLevel):

    def __init__(self):
        # TODO: im .lp ist length = width --> ändern?
        states = {"position(0..63)",
                  "frozen(0..18)", "frozen(20..28)", "frozen(30..34)", "frozen(36..40)",
                  "frozen(43..45)", "frozen(47)", "frozen(48)", "frozen(50)", "frozen(51)",
                  "frozen(53)", "frozen(55)", "frozen(56..58)", "frozen(60..63)",
                  "frozen(4)", "hole(19)", "hole(29)", "hole(35)", "hole(41)", "hole(42)",
                  "hole(46)", "hole(49)", "hole(52)", "hole(54)", "hole(59)",
                  "#const goal = 63", "#const length = 8",
                  "leftEdge(0)", "leftEdge(8)", "leftEdge(16)", "leftEdge(24)",
                  "leftEdge(32)", "leftEdge(40)", "leftEdge(48)", "leftEdge(56)",
                  "rightEdge(7)", "rightEdge(15)", "rightEdge(23)", "rightEdge(31)",
                  "rightEdge(39)", "rightEdge(47)", "rightEdge(55)", "rightEdge(63)",
                  "upperEdge(0..7)", "lowerEdge(56..63)"
                  }
        start = {"currentPosition(0)"}
        width = 8
        height = 8
        super().__init__(start, width, height, states)
