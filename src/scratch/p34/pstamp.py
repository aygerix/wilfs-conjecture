r"""Mirrors of postage-stamp tiles (lead, 2026-10-21). S = <m, m+delta_1, .., m+delta_d> with small delta: the tile is
no-wrap at phase 0 when m <= postage-stamp range + 1.  DEP-ALL on the mirror (D, -delta) <=> max_sigma V_delta(sigma)
<= m - 1 + Dep.  Scans all delta with 1 = delta_1 < .. < delta_d <= AMAX and m in [M0, range+1]; reports the minimum of
the mirror slack (m - 1 + Dep - max V) and of the direct slack (min V + Dep), and whether the mirror is a factorization tile.
Usage: python pstamp.py d AMAX"""
import sys, itertools
sys.path.insert(0, '.')
from tile import build
d, AMAX = map(int, sys.argv[1:3])
def Vs(m, D, delta):
    N = len(delta); Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    om = {x: 0 for x in D}
    for b in range(N):
        for x in D:
            if up(x, b) not in Ds: om[x] += x[b] + 1
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    dep = sum(v for x, v in om.items() if x not in mx)
    wt = [0] * m
    for x in D: wt[sum(p * q for p, q in zip(x, delta)) % m] += om[x]
    Mp = m * (m - 1) // 2
    V = [(Mp - (sum(wt[l] * ((l + rho) % m) for l in range(m)) - N * Mp)) // m for rho in range(m)]
    return V, dep
best = None; bestd = None; cnt = 0
for rest in itertools.combinations(range(2, AMAX + 1), d - 1):
    dl = (1,) + rest
    for m in range(2 * d + 2, 200):
        R = build(m, [m + x for x in dl])
        if R is None: continue
        c, gens, M = R
        if len(gens) != d: continue
        D = list(M); delta = [g % m for g in gens]
        if any(sum(p * q for p, q in zip(x, delta)) >= m for x in D):   # stop once the tile wraps
            break
        cnt += 1
        V, dep = Vs(m, D, delta)
        ms = m - 1 + dep - max(V); ds = min(V) + dep
        if best is None or ms < best[0]: best = (ms, m, gens, dep, max(V), max(sum(x) for x in D))
        if bestd is None or ds < bestd[0]: bestd = (ds, m, gens, dep)
print("d=%d AMAX=%d no-wrap tiles %d" % (d, AMAX, cnt))
print("  min mirror slack (m-1+Dep-maxV), m, gens, Dep, maxV, height:", best)
print("  min direct slack (minV+Dep):", bestd)
