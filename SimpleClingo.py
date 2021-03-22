import clingo


def mop(m: clingo.Model):
    av = set()
    for symbol in m.symbols(shown=True):
        # We expect atoms of the form `currentExecutable(move(X, Y)`
        # but we are only interested in the first argument `move(X, Y)`
        #av.add(str(symbol.arguments[0]))
        sym = str(symbol)
        av.add(sym)
    print(sorted(av))

def mip(m: clingo.Model):
    print(m)

def mep(m: clingo.Model):
    mip(m)
    mop(m)

ctr = clingo.Control()
ctr.load("SimpleClingo.lp")
#ctr.load("frozenLake4x4.lp")
ctr.ground([("base", [])])
ctr.solve(on_model=mep)