# NON-two-face e = 4 with c > 3m, m >= 19: list all where the sharp tau-criterion fails, with shape data.
#   usage: nt_fail.py m0 m1 K   (generators m < a < b < c < K m)
import sys, itertools
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from cl import factorizations_down_set
def shape(s):
    p, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}; D = set(cells)
    m, c = s.m, s.c; M = max(cells.values())
    if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): return None
    X = [x for x in D if c <= cells[x] < c + m]
    P2 = sum(1 for y, z in itertools.combinations(X, 2) if sum(y[a] != z[a] for a in range(3)) == 2)
    L = [max(x[i] for x in D) + 1 for i in range(3)]
    core = [x for x in D if min(x) >= 1]
    xf = sum(1 for x in X if min(x) == 0); xc = len(X) - xf
    return dict(tau=len(X), P2=P2, L=L, core=len(core), xf=xf, xc=xc, M=M, p=p)
m0, m1, K = map(int, sys.argv[1:4])
for m in range(m0, m1 + 1):
    n = nf = 0; worst = None
    for g3 in itertools.combinations(range(m + 1, K*m), 3):
        if reduce(gcd, (m,) + g3) != 1: continue
        s = NS.from_generators([m, *g3])
        if s.e != 4 or s.c <= 3*m: continue
        r = shape(s)
        if r is None: continue
        n += 1; ex = 2*r["tau"] + r["P2"] - m - 1; worst = ex if worst is None else max(worst, ex)
        if ex > 0:
            nf += 1
            print(f'  FAIL m={m} gens={[m,*g3]} ex={ex} tau={r["tau"]} P2={r["P2"]} L={r["L"]} core={r["core"]} xf/xc={r["xf"]}/{r["xc"]} W={s.W if isinstance(s.W,int) else s.W()} c/m={s.c/m:.2f}', flush=True)
    print(f'm={m}: non-two-face e=4, c>3m: {n}; tau-criterion failures {nf}; max excess {worst}', flush=True)
