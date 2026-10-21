r"""Case B from near-maximal cyclic sum covers (lead, 2026-10-21). Literature (Haanpaa, JIS 7 (2004), Table): the largest
cyclic group with a k-element sum cover (A + A = Z_n) is n'(k) = 3,5,9,13,19,21,30,35,43,51,63,67 for k = 2..13.  A
height-2 tile is such a cover A = {0} U delta (k = d+1), with case-B margin C(d,2) - 3 k_mixed - 2 k_loop.  This script
enumerates delta (d = k-1 elements with 1 in delta; this is WLOG only for delta containing a unit mod m, after scaling)
for Z_m, keeps those where {0} U delta covers all but at most MISS residues with <= 2 summands, builds the factorization
tile of S = <m, m + delta> (lift 1: all generators in (m,2m)) and of S with residues < m/2 lifted to (2m, 2.5m) (lift 2),
and reports case B (Dep < Sigma_supp) by height with Tile-CL min V.  Usage: python sumcover.py d m MISS"""
import sys, itertools
sys.path.insert(0, '.')
from tile import build
from tcldich import stats
d, m, MISS = map(int, sys.argv[1:4])
cnt = hit = 0; byh = {}; ex = {}
for rest in itertools.combinations(range(2, m), d - 1):
    dl = (1,) + rest; A = (0,) + dl
    cov = {(a + b) % m for a in A for b in A}
    if m - len(cov) > MISS: continue
    cnt += 1
    for lift in (1, 2):
        G = [x + lift * m if lift == 2 and x < m // 2 else x + m for x in dl] if lift == 2 else [x + m for x in dl]
        R = build(m, sorted(G))
        if R is None: continue
        c, gens, M = R
        if len(gens) != d: continue
        D = list(M); v, dep, ss = stats(m, D, [g % m for g in gens])
        if dep < ss:
            h = max(sum(x) for x in D); byh[h] = byh.get(h, 0) + 1; hit += 1
            if h not in ex or ss - dep > ex[h][0]: ex[h] = (ss - dep, gens, c, v, int(3 * (d + 1) < m and c > 4 * m))
print("d=%d m=%d covers(miss<=%d) %d  case-B tiles %d by height %s  best per height (margin, gens, c, minV, open) %s" % (d, m, MISS, cnt, hit, byh, ex), flush=True)
