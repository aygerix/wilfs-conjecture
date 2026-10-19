"""CHAIN-WILF on large interval semigroups <m, 2m+a..2m+b> (lead): min ratio over a with 3e < m, for given m.
usage: python chain_interval_large.py m1,m2,... """
import sys
from chain_interval import chain_stats
for m in [int(x) for x in sys.argv[1].split(',')]:
    best = None; best3 = None
    for width in range(m//6, m//2 + 1, max(1, m//60)):
        for a in range(m//5, m//2 + 1, max(1, m//60)):
            b = a + width - 1
            if b >= m: continue
            r = chain_stats(m, list(range(2*m + a, 2*m + b + 1)))
            if not r or r['q'] < 4: continue
            key = (round(r['ratio'], 4), a, b, r['e'], r['c'], r['q'], r['W'])
            if best is None or key < best: best = key
            if 3*r['e'] < m and (best3 is None or key < best3): best3 = key
    print('m=%d  min CHAIN ratio (any e): %s   with 3e<m: %s' % (m, best, best3), flush=True)
