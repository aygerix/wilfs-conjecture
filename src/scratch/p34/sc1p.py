r"""SC1' (lead, 2026-10-20): C(|bd|,2) + d C(|A|,2) + m (d|N| - E) >= (d-1) C(m,2), where N = non-maximal cells,
E = sum_x |supp x| (Hasse edges); d|N| - E <= Dep is proved.  Also SC1'' with all levels: sum_{k} C(n_k^A,2) for maximal
weights plus C(|bd|,2) - C(|A|,2) at level 1.  Reports failures in the open regime (3e < m) and overall.
Usage: python sc1p.py NS SEED MMIN MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
C2 = lambda n: n * (n - 1) // 2
cnt = no = f1 = fo1 = f2 = fo2 = 0; w = None
while cnt < NS:
    m = rnd.randint(MMIN, MMAX); k = rnd.randint(2, max(2, m // 2)); c0 = rnd.randint(m + 1, 10 * m)
    G = sorted(rnd.sample(range(m + 1, min(rnd.choice([2 * m, 3 * m, c0 + m]), c0 + m)), min(k, c0 - 1)))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; d = len(gens)
    if d < 2: continue
    cnt += 1; D = list(M); Ds = set(D); op = 3 * (d + 1) < m; no += op
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(d))
    A = [x for x in D if all(up(x, b) not in Ds for b in range(d))]
    I = [x for x in D if all(up(x, b) in Ds for b in range(d))]
    bd = m - len(I); a = len(A); Nn = m - a; E = sum(sum(1 for t in x if t) for x in D)
    rhs = (d - 1) * C2(m)
    s1 = C2(bd) + d * C2(a) + m * (d * Nn - E) - rhs
    ws = [d + sum(y) for y in A]
    s2 = C2(bd) + sum(C2(sum(1 for v in ws if v >= kk)) for kk in range(2, max(ws) + 1)) + m * (d * Nn - E) - rhs
    if s1 < 0: f1 += 1; fo1 += op
    if s2 < 0:
        f2 += 1; fo2 += op
        if op and (w is None or s2 / m / m < w[0]): w = (s2 / m / m, m, gens, a, bd, E)
print("S %d (open %d): SC1' fails %d (open %d); SC1'' fails %d (open %d)  worst open SC1'' %s" % (cnt, no, f1, fo1, f2, fo2, w))
