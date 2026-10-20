r"""Which down-sets fail CR_DEP? (lead, 2026-10-21). For all down-sets D in N^N of size m: CR_DEP slack, the one-step
difference-body condition DB1: |N1| + sum_b |F_b(N1)| <= m (N1 = interior), the two-step DB2: |N2 - Delta_2| <= m
(N2 = {x : x + Delta_2 subset D}), and whether D is a lattice tile (some injective labeling).  Usage: python crdep_db.py N MMIN MMAX"""
import sys, itertools
sys.path.insert(0, '.')
from subadd_lp import downsets
from crdep import crdep
def simplex(N, j):
    out = {(0,) * N}
    for _ in range(j): out |= {tuple(a[t] + (t == i) for t in range(N)) for a in out for i in range(N)}
    return out
def dbj(D, N, j):
    Ds = set(D); S = simplex(N, j)
    Nj = [x for x in D if all(tuple(a + b for a, b in zip(x, s)) in Ds for s in S)]
    diff = {tuple(a - b for a, b in zip(x, s)) for x in Nj for s in S}
    return len(diff)
def is_tile(D, N, m):
    for b in itertools.product(range(1, m), repeat=N):
        if len({sum(x * y for x, y in zip(a, b)) % m for a in D}) == m: return True
    return False
N, MMIN, MMAX = map(int, sys.argv[1:4])
for m in range(MMIN, MMAX + 1):
    tot = fa = fdb1 = fdb2 = ftile = 0; ex = None
    for D in downsets(N, m):
        tot += 1; sl, dep = crdep(D, N)
        if sl >= 0: continue
        fa += 1
        ok1 = dbj(D, N, 1) <= m
        if not ok1: continue
        fdb1 += 1
        ok2 = dbj(D, N, 2) <= m and dbj(D, N, 3) <= m
        if not ok2: continue
        fdb2 += 1
        if is_tile(D, N, m):
            ftile += 1
        elif ex is None: ex = (sl, D)
    print("N=%d m=%d down-sets %d  CR_DEP fails: all %d, with DB1 %d, with DB1-3 %d, tiles %d   DB-passing non-tile failure: %s" % (N, m, tot, fa, fdb1, fdb2, ftile, ex), flush=True)
