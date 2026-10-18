# Dichotomy test for NON-two-face e = 4, c > 3m:
#  (I)  N >= m-1  (T(X) <= 2m+1)                       [TOP-type; => Wilf]
#  (II) crude faces bound: (m+8-2 sum L) M + 4 Def'_faces(crude) + 4 sum_core (2M - 3 w_hat) >= 3m(m-1)
#       Def'_faces(crude) = sum over non-axis face runs R of |R| * (m if end not in X else m - pi(end)),
#       w_hat(core x) = M - m if x not in X else w(x).                                         [=> Wilf]
import sys, itertools
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def analyse(s):
    p, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}; D = set(cells)
    if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): return None
    m, c = s.m, s.c; M = max(cells.values())
    add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
    def top(x, i):
        while add(x, i) in D: x = add(x, i)
        return x
    X = {x for x in D if cells[x] >= c}
    TX = sum(sum(x) + 3 for x in X); I = TX <= 2*m + 1
    L = [max(x[i] for x in D) + 1 for i in range(3)]
    runs = set()
    for x in D:
        for i in range(3):
            others = [j for j in range(3) if j != i]
            if any(x[j] == 0 for j in others) and not all(x[j] == 0 for j in others):
                runs.add((x[:i] + (0,) + x[i+1:], i))
    defc = 0
    for b, i in runs:
        t = top(b, i); ln = t[i] + 1
        defc += ln*(m if t not in X else M - cells[t])
    core = [x for x in D if min(x) >= 1]
    corec = sum(2*M - 3*(cells[x] if x in X else M - m) for x in core)
    II = (m + 8 - 2*sum(L))*M + 4*defc + 4*corec >= 3*m*(m - 1)
    return I, II, dict(TX=TX - 2*m - 1, L=L, core=len(core), cm=round(c/m, 2), W=s.W if isinstance(s.W, int) else s.W(),
                       IIval=(m + 8 - 2*sum(L))*M + 4*defc + 4*corec - 3*m*(m - 1))
m0, m1, K = map(int, sys.argv[1:4])
for m in range(m0, m1 + 1):
    n = nI = nII = nb = 0
    for g3 in itertools.combinations(range(m + 1, K*m), 3):
        if reduce(gcd, (m,) + g3) != 1: continue
        s = NS.from_generators([m, *g3])
        if s.e != 4 or s.c <= 3*m: continue
        r = analyse(s)
        if r is None: continue
        n += 1; nI += r[0]; nII += r[1]
        if not r[0] and not r[1]:
            nb += 1; print('   NEITHER', [m, *g3], r[2], flush=True)
    print(f'm={m}: {n} non-two-face c>3m; (I) holds {nI}; (II) holds {nII}; neither {nb}', flush=True)
