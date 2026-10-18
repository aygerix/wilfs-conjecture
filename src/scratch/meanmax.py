# e = 4: theta = mean(Ap)/max(Ap).  Wilf <=> theta <= 3/4 - (m-1)/(4M).  Report max theta (two-face vs not), c > 3m.
import sys, itertools, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def info(s):
    ap = s.apery(); m = s.m; M = max(ap); th = sum(ap)/(m*M)
    _, best = factorizations_down_set(s, 'grlex'); D = set(best.values())
    two = any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a + 1, 3))
    need = 0.75 - (m - 1)/(4*M)
    return th, need, two, M/m
res = {True: [], False: []}
if sys.argv[1] == 'exh':
    for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        for g3 in itertools.combinations(range(m + 1, int(sys.argv[4])*m), 3):
            if reduce(gcd, (m,) + g3) != 1: continue
            s = NS.from_generators([m, *g3])
            if s.e != 4 or s.c <= 3*m: continue
            th, need, two, Mm = info(s); res[two].append((th, need, s.P, round(Mm, 1)))
for two in (False, True):
    L = res[two]
    if not L: continue
    print('two-face' if two else 'NON-two-face', len(L), 'max theta', max(L)[0:1], max(L)[2:], ' min (need - theta)', min((n - t, P, Mm) for t, n, P, Mm in L))
    print('   count theta > 2/3:', sum(t > 2/3 for t, n, P, Mm in L), '  theta > 0.6875:', sum(t > 0.6875 for t, n, P, Mm in L))
