"""Thin a failing interval below 3e = m while keeping B + B (lead): start from the interval [a, b] at level 2 (k = 2)
that minimizes the CHAIN ratio for this m, then greedily delete interior elements whose removal keeps B+B unchanged and
keeps q, choosing each deletion to minimize the CHAIN ratio, until 3e < m.  usage: python chain_thin2.py m a b"""
import sys
from chain_interval import chain_stats
m, a, b = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
B = list(range(a, b + 1)); full2 = {u + v for u in B for v in B}
r = chain_stats(m, [2*m + x for x in B]); print('start', len(B) + 1, round(r['ratio'], 4), r['q'], r['W'], flush=True)
while 3*(len(B) + 1) >= m - 0:
    best = None
    for x in B[1:-1]:
        T = [y for y in B if y != x]
        if {u + v for u in T for v in T} != full2: continue
        rr = chain_stats(m, [2*m + y for y in T])
        if not rr or rr['q'] < 4: continue
        if best is None or rr['ratio'] < best[0]: best = (rr['ratio'], x, rr)
    if best is None: print('stuck at e =', len(B) + 1); break
    B.remove(best[1]); r = best[2]
    print('e=%d 3e<m=%s ratio=%.4f q=%d W=%d removed %d' % (r['e'], 3*r['e'] < m, r['ratio'], r['q'], r['W'], best[1]), flush=True)
print('final B =', B)
