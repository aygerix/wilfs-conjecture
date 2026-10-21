r"""Exhaustive case-B search over S = <m, m + delta> (lead, 2026-10-21): all d-subsets delta of [1, m) (or NS random
ones when NS > 0), true factorization tile via build(); records case B (Dep < Sigma_supp) by height, the largest margin
Sigma_supp - Dep per height, and Tile-CL min V on case-B hits of height >= 3.  Usage: python cbexh.py d MMIN MMAX NS SEED"""
import sys, itertools, random
sys.path.insert(0, '.')
from tile import build
from tcldich import stats
d, MMIN, MMAX, NS, SEED = map(int, sys.argv[1:6]); rnd = random.Random(SEED)
for m in range(MMIN, MMAX + 1):
    it = itertools.combinations(range(1, m), d) if NS == 0 else (tuple(sorted(rnd.sample(range(1, m), d))) for _ in range(NS))
    tot = 0; byh = {}; best = {}
    for dl in it:
        R = build(m, [m + x for x in dl])
        if R is None: continue
        c, gens, M = R
        if len(gens) != d: continue
        D = list(M); Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(d))
        om = {x: 0 for x in D}
        for b in range(d):
            for x in D:
                if up(x, b) not in Ds: om[x] += x[b] + 1
        mx = {x for x in D if all(up(x, b) not in Ds for b in range(d))}
        dep = sum(v for x, v in om.items() if x not in mx)
        ss = sum(max(0, sum(1 for t in x if t) - 1) for x in D)
        tot += 1
        if dep >= ss: continue
        h = max(sum(x) for x in D); byh[h] = byh.get(h, 0) + 1
        if h not in best or ss - dep > best[h][0]:
            v = stats(m, D, [g % m for g in gens])[0] if h >= 3 else None
            best[h] = (ss - dep, gens, c, v)
    print("d=%d m=%d S %d  case-B by height %s  max margin per height %s" % (d, m, tot, byh, best), flush=True)
