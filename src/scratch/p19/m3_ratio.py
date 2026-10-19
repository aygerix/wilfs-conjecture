"""Among CHAIN failures in the interval+1 family, the largest M/n1 and M - 2 n1 (lead, 2026-10-19): how far below
3 n1 can a failing M be?  usage: python m3_ratio.py mlo mhi"""
import sys
from m3_pert import stats
mlo, mhi = int(sys.argv[1]), int(sys.argv[2])
best = None; best2 = None; nf = 0
for m in range(mlo, mhi + 1):
    for k in (1, 2):
        for a in range(1, m):
            for b in range(a + 1, m):
                core = list(range(k*m + a, k*m + b + 1))
                for x in [None] + list(range(m + 1, 4*m)):
                    if x is not None and x in core: continue
                    r = stats(m, core + ([x] if x else []))
                    if not r or r['q'] < 2 or r['ratio'] >= 1: continue
                    nf += 1
                    v = r['M'] / r['n1']
                    if best is None or v > best[0]: best = (round(v, 4), round(r['ratio'], 4), m, k, a, b, x, r['M'], r['n1'], r['e'], r['q'], r['H'])
                    u = (r['M'] - 2*r['n1']) / m
                    if best2 is None or u > best2[0]: best2 = (round(u, 4), round(r['ratio'], 4), m, k, a, b, x, r['M'], r['n1'], r['e'], r['q'], r['H'])
print('failures', nf); print('max M/n1 among failures:', best); print('max (M - 2 n1)/m among failures:', best2)
