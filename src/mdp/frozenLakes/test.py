import clingo


def mop(m: clingo.Model):
    av = set()
    for symbol in m.symbols(shown=True):
        # We expect atoms of the form `currentExecutable(move(X, Y)`
        # but we are only interested in the first argument `move(X, Y)`
        #av.add(str(symbol.arguments[0]))
        sym = str(symbol)
        if sym.startswith("down") or sym.startswith("right") or sym.startswith("left") or sym.startswith("up"):
            av.add(sym)
    print(sorted(av))
    # print(av.__contains__("red"))

def mip(m: clingo.Model):
    print(m)

def mep(m: clingo.Model):
    #mip(m)
    mop(m)

ctr = clingo.Control()
#ctr.load("SimpleClingo.lp")
ctr.load("frozenLake4x4.lp")
state = 6
ctr.add('base', [], "currentState(" + str(state) + ").")
ctr.ground([("base", [])])
ctr.solve(on_model=mep)