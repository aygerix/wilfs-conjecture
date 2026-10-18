# General e = 4 identity (any 3-D tile):  3mW + 3m(m-1) = (m - 4(L1+L2+L3-2)) M + 4 Def_faces + 4 SumAxes + 4 sum_core (2M - 3w)
# Def_faces = sum over 2-D runs of the three coordinate faces (axis runs once) of |R|(M - w(end)); core = cells with all coords >= 1.
import sys, itertools, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def check(s):
    p, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}; D = set(cells); m = s.m; M = max(cells.values())
    def add(x, i): return x[:i] + (x[i] + 1,) + x[i+1:]
    def top(x, i):
        while add(x, i) in D: x = add(x, i)
        return x
    runs = set()
    for x in D:
        for i in range(3):
            # face run: the i-column through x lies in a coordinate face iff some other coordinate of x is 0
            if any(x[j] == 0 for j in range(3) if j != i):
                base = x[:i] + (0,) + x[i+1:]; runs.add((base, i))
    Def_faces = sum((top(b, i)[i] + 1)*(M - cells[top(b, i)]) for b, i in runs)
    L = [max(x[i] for x in D) + 1 for i in range(3)]
    SumAxes = sum(p[i]*L[i]*(L[i] - 1)//2 for i in range(3))
    core = [x for x in D if min(x) >= 1]
    W = s.W if isinstance(s.W, int) else s.W()
    lhs = 3*m*W + 3*m*(m - 1); rhs = (m - 4*(sum(L) - 2))*M + 4*Def_faces + 4*SumAxes + 4*sum(2*M - 3*cells[x] for x in core)
    assert lhs == rhs, (s.P, lhs, rhs)
    return len(core)
n = 0; cores = 0
for m in range(4, 15):
    for g3 in itertools.combinations(range(m + 1, 3*m), 3):
        if reduce(gcd, (m,) + g3) != 1: continue
        s = NS.from_generators([m, *g3])
        if s.e == 4: k = check(s); n += 1; cores += k > 0
print('identity holds on', n, 'e=4 semigroups;', cores, 'with nonempty core')
