"""CHAIN-WILF(3e<m) on block-union level-2 families (lead): generators 2m + B, B = union of k blocks [x_i, x_i + L_i).
Scans k = 2 (and k = 3 randomly), keeps q >= 4 and 3e < m; reports failures and the minimum ratio.
usage: python chain_blocks.py m step trials3"""
import sys, random
from chain_interval import chain_stats
m, step, T3 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
best = None; nf = 0; tot = 0
def test(B, tag):
    global best, nf, tot
    B = sorted(set(B))
    if not B or B[0] < 1 or B[-1] >= m: return
    r = chain_stats(m, [2*m + x for x in B])
    if not r or r['q'] < 4 or 3*r['e'] >= m: return
    tot += 1
    key = (round(r['ratio'], 4), tag, r['e'], r['c'], r['q'], r['W'])
    if best is None or key < best: best = key + (B,)
    if r['ratio'] < 1:
        nf += 1
        if nf <= 15: print('FAIL', key, B, flush=True)
for L in range(max(2, m//14), m//5 + 1, step):
    for x in range(1, m - L, step):
        for y in range(x + L + 1, m - L + 1, step):
            test(list(range(x, x + L)) + list(range(y, y + L)), ('k2', x, y, L))
rng = random.Random(m)
for _ in range(T3):
    k = rng.choice([3, 4]); L = rng.randint(max(2, m//(k*k + 2)), max(3, m//(k*k - 2)))
    xs = sorted(rng.sample(range(1, m - L), k))
    test([z for x in xs for z in range(x, x + L)], ('k%d' % k, tuple(xs), L))
print('m=%d tested=%d failures=%d min=%s' % (m, tot, nf, best), flush=True)
