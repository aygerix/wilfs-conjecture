"""Near-T family with one low generator (lead): S = <m, g_1..g_k> u [K, oo), K = qm + kappa, low generators g_i = m + beta_i.
Reports min CHAIN ratio over states with Apery height >= 3 (and over all), per m.  usage: python chain_tg.py m1,m2,.. k"""
import sys, random
from chain_interval import chain_stats, apery
def height(m, w, gens):
    ap = set(w); L = {0: 0}
    for x in sorted(w)[1:]:
        L[x] = 1 + min(L[x - g] for g in gens if x - g in ap and x - g in L)
    return max(L.values())
rng = random.Random(11)
for m in [int(x) for x in sys.argv[1].split(',')]:
    k = int(sys.argv[2]); best3 = None; best = None; nf3 = 0; tot = 0
    for _ in range(1500 if m <= 100 else 500):
        q = rng.choice([4, 5, 6]); K = q*m + rng.randint(-m + 1, 0)
        betas = sorted(rng.sample(range(1, m), k))
        base = apery(m, [m] + [m + b for b in betas])
        if any(x is None for x in base): continue
        w = [0] + [min(base[i], K + ((i - K) % m)) for i in range(1, m)]
        M = max(w); c = M - m + 1
        if c <= 3*m: continue
        ap = set(w); gens = sorted(x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m))
        r = chain_stats(m, gens)
        if not r or r['c'] != c: continue
        h = height(m, w, gens); tot += 1
        key = (round(r['ratio'], 4), m, tuple(betas), K, r['e'], r['q'], h)
        if best is None or key < best: best = key
        if h >= 3:
            if best3 is None or key < best3: best3 = key
            if r['ratio'] < 1: nf3 += 1; print('H3FAIL', key, flush=True)
    print('m=%d k=%d tested=%d  min(all)=%s  min(height>=3)=%s  H3 failures=%d' % (m, k, tot, best, best3, nf3), flush=True)
