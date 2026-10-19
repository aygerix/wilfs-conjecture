"""CHAIN-WILF(3e<m) stress test on thin-basis level-2 families (lead): generators 2m + a + B,
B = {0..k-1} u {k, 2k, ..., j*k} (B + B covers an interval of length ~ 2jk with |B| = k + j), plus random thinnings
of intervals that keep B + B an interval.  usage: python chain_thin.py m1,m2,..."""
import sys, random
from chain_interval import chain_stats
rng = random.Random(7)
for m in [int(x) for x in sys.argv[1].split(',')]:
    best = None; nf = 0; tot = 0
    for k in range(2, m//3):
        for j in range(1, m//3):
            B = sorted(set(list(range(k)) + [k*i for i in range(1, j + 1)]))
            span = B[-1]
            if span >= m//2: break
            for a in range(max(1, m//6), m//2, max(1, m//25)):
                if a + span >= m: continue
                g = [2*m + a + x for x in B]
                r = chain_stats(m, g)
                if not r or r['q'] < 4 or 3*r['e'] >= m: continue
                tot += 1
                key = (round(r['ratio'], 4), m, a, k, j, r['e'], r['c'], r['q'], r['W'])
                if best is None or key < best: best = key
                if r['ratio'] < 1: nf += 1; print('FAIL', key, flush=True)
    # random thinnings of an interval of length ~ m/3 that keep 2B = interval
    for _ in range(300):
        L = rng.randint(m//4, m//3 + 2); a = rng.randint(m//6, m//2)
        B = list(range(L)); rng.shuffle(B)
        Bs = set(range(L))
        for x in B:
            if x in (0, L - 1): continue
            T = Bs - {x}
            if len({u + v for u in T for v in T}) == 2*L - 1: Bs = T
            if 3*(len(Bs) + 1) < m and rng.random() < 0.15: break
        g = [2*m + a + x for x in sorted(Bs)]
        if a + L >= m: continue
        r = chain_stats(m, g)
        if not r or r['q'] < 4 or 3*r['e'] >= m: continue
        tot += 1
        key = (round(r['ratio'], 4), m, a, 'thin', len(Bs), r['e'], r['c'], r['q'], r['W'])
        if best is None or key < best: best = key
        if r['ratio'] < 1: nf += 1; print('FAIL', key, sorted(Bs), flush=True)
    print('m=%d tested(3e<m, q>=4)=%d failures=%d min=%s' % (m, tot, nf, best), flush=True)
