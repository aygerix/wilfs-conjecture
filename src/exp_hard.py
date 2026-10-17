"""Experiment E2: hardest semigroups for Wilf at depth q>=4 (smallest e*ell/c),
excluding the equality families e=2 and S = mN u [qm,oo)."""
import sys, heapq
sys.path.insert(0, 'src')
from ns import all_by_genus
G = int(sys.argv[1]) if len(sys.argv) > 1 else 20
best = []
byq = {}
for g, s in all_by_genus(G):
    if s.m == 1 or s.e == 2:
        continue
    if s.ell == s.q and s.rho == 0 and s.e == s.m:
        continue
    r = s.e * s.ell / s.c
    q = min(s.q, 6)
    key = (q,)
    if key not in byq or r < byq[key][0]:
        byq[key] = (r, s.summary(), s.W0())
    if s.q >= 4:
        heapq.heappush(best, (-r, s.c, tuple(s.P)))
        if len(best) > 25:
            heapq.heappop(best)
for k in sorted(byq):
    print('q', k, 'min ratio', round(byq[k][0], 4), byq[k][1], 'W0=', byq[k][2])
print('--- 25 smallest ratios with q>=4 ---')
for r, c, P in sorted(best, reverse=True):
    print(round(-r, 4), 'c', c, 'P', P)
