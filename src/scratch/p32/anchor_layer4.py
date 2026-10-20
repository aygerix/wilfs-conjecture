"""Check our reading of the conjectures.io anchor theorem (an_anchor_bound) as a layer-4 inequality at any depth.
Model (m, rho=0, O=B) for P18 S = <m, m+B>, B in [1, m) (no conductor condition):
  ell = N0+N1+N2+N3, d = N4 (N_k = #{r : Kunz coordinate x_r <= k}), W0 = (|B|+1) ell - 4 d, p = m - d,
  h4 = #{u < m : u in 4B' minus 3B'} with B' = {0} u B (sumsets in N, not mod m).
Claim (if some 2b >= m): W0 + p + h4 >= 0, i.e. e*ell - 5*N4 + m + h4 >= 0. Also reports LAYER(4) := e*ell - 4*N4 >= 0.
Usage: python anchor_layer4.py MMAX NRAND SEED"""
import random, sys

def kunz(m, B):
    # Dijkstra-free: levels by BFS over residues (all generators m+b have level 1 + carry)
    INF = 10**9
    w = [INF] * m; w[0] = 0
    gens = [m + b for b in B]
    changed = True
    while changed:
        changed = False
        for r in range(m):
            if w[r] == INF: continue
            for g in gens:
                v = w[r] + g; s = v % m
                if v < w[s]: w[s] = v; changed = True
    if any(x == INF for x in w): return None
    return [(w[r] - r) // m for r in range(m)]

def sums_upto(B, t, bound):
    cur = {0}; allv = [set([0])]
    for _ in range(t):
        cur = {x + b for x in cur for b in [0] + B if x + b < bound}
        allv.append(set(cur))
    return allv  # allv[t] = (t B') n [0,bound)

def check(m, B):
    x = kunz(m, B)
    if x is None: return None
    N = [sum(1 for v in x if v <= k) for k in range(5)]
    e = len(B) + 1
    ell = sum(N[:4])
    Y = sums_upto(B, 4, m)
    h4 = len(Y[4] - Y[3])
    depth = max(x)  # Kunz max ~ depth
    high = any(2 * b >= m for b in B)
    return dict(core=e * ell - 5 * N[4] + m + h4, layer4=e * ell - 4 * N[4], high=high, depth=depth, h4=h4, N=N)

if __name__ == "__main__":
    MMAX, NR, SEED = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rnd = random.Random(SEED)
    stats = dict(n=0, nhigh=0, fail=0, l4fail=0, mincore=None, deep=0)
    worst = None
    for it in range(NR):
        m = rnd.randint(8, MMAX)
        k = rnd.randint(2, min(12, m - 2))
        lo = rnd.choice([1, m // 3, m // 2, (2 * m) // 3])
        pool = list(range(max(1, lo), m))
        if len(pool) < k: continue
        B = sorted(rnd.sample(pool, k))
        r = check(m, B)
        if r is None: continue
        stats['n'] += 1
        if r['depth'] >= 5: stats['deep'] += 1
        if r['layer4'] < 0: stats['l4fail'] += 1
        if not r['high']: continue
        stats['nhigh'] += 1
        if stats['mincore'] is None or r['core'] < stats['mincore']:
            stats['mincore'] = r['core']; worst = (m, B, r)
        if r['core'] < 0:
            stats['fail'] += 1
            print("FAIL", m, B, r, flush=True)
    print(stats); print("worst", worst)
