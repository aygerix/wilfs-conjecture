# T1-DOWN-UF test (lead, 2026-10-20): order ideal D in N^d with INJECTIVE residues rho(f) = sum f_a r_a mod m (|D| <= m).
# K_p(f) = P_p(f) - sum_a f_a [p in arc_a(f)],  P_p(f) = floor((R(f) - p)/m) + 1,  R(f) = sum f_a r_a (r_a in [1, m-1]).
# Claim tested: sum_{f in D} K_p(f) <= |D| - |D cap T|, T = {0} u {e_a}, for every p in [1, m].
import itertools, sys
sys.path.insert(0, '.')
from t1uf import partitions, plane_partitions
def ideals(d, n):
    if d == 2:
        for lam in partitions(n): yield [(i, j) for i, row in enumerate(lam) for j in range(row)]
    else:
        yield from plane_partitions(n)
def test(D, r, m):
    d = len(r); R = {f: sum(f[a] * r[a] for a in range(d)) for f in D}
    if len(set(v % m for v in R.values())) != len(D): return None
    T = sum(1 for f in D if sum(f) <= 1)
    worst = None
    for p in range(1, m + 1):
        P = lambda f: (R[f] - p) // m + 1
        tot = 0
        for f in D:
            k = P(f)
            for a in range(d):
                if f[a] >= 1:
                    g = list(f); g[a] -= 1; g = tuple(g)
                    k -= f[a] * (P(f) - P(g))
            tot += k
        sl = len(D) - T - tot
        if worst is None or sl < worst[0]: worst = (sl, p)
    return worst
d = int(sys.argv[1]); M = int(sys.argv[2])
for m in range(3, M + 1):
    tested = fails = 0; ex = None
    for n in range(1, m + 1):
        for D in ideals(d, n):
            for r in itertools.product(range(1, m), repeat=d):
                w = test(D, r, m)
                if w is None: continue
                tested += 1
                if w[0] < 0:
                    fails += 1
                    if ex is None: ex = (sorted(D), r, w)
    print("d=%d m=%d: tested %d (all sizes), fails %d, first %s" % (d, m, tested, fails, ex), flush=True)
