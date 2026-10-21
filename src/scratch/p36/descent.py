r"""Test of Lemma DESCENT (lead, 2026-10-21).  For S with an additive height h on Ap (h = factorization length, well defined
iff S is graded: hg == hn), lower w'_s = w_s - m t h_s.  Conditions: (a) k_s - t h_s >= 1; (b) w'_i + w'_j >= w'_{i+j} for all
pairs; (c) max w' attained at a cell of maximal h.  Claim: S' = <m, w'> is a numerical semigroup with Ap(S', m) = w' and
    W(S) - W(S') >= t[(e-1) m h* - e H] >= 0     (H = sum h, h* = max h; CH' gives the bracket >= 0),
with equality when e(S') = e(S) and argmax unchanged.  For each random graded S: largest valid t, the check, and the
depth c'/m reached.  W(S') is recomputed from scratch (rtexact.indep_W, Apery-free).
usage: /usr/bin/python3 descent.py NS SEED MMIN MMAX"""
import sys, random
sys.path.insert(0, '.')
from rt2lib import data
from rtexact import indep_W
NS, seed, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
tested = applied = to4 = 0; worst = None
while tested < NS:
    m = rng.randint(mmin, mmax); d = rng.randint(2, min(6, m - 2))
    s = rng.sample(range(1, m), d); K = [rng.randint(1, 5) for _ in s]
    G = [m] + [m * k + x for k, x in zip(K, s)]
    D = data(G); w = D['w']; T = D['tight']; gens = set(D['gens']); e = D['e']
    if D['c'] <= 4 * m: continue
    hg = [0] * m; hn = [0] * m
    for x in sorted(range(1, m), key=lambda t: w[t]):
        if x in gens: hg[x] = hn[x] = 1
        else:
            hg[x] = max(hg[i] + hg[j] for (i, j, t) in T if t == x); hn[x] = min(hn[i] + hn[j] for (i, j, t) in T if t == x)
    if hg != hn: continue
    tested += 1; h = hg; hs = max(h); H = sum(h); X = (e - 1) * m * hs - e * H
    assert X >= 0, ("CH' bracket negative", G, X)
    k = [x // m for x in w]
    def valid(t):
        wp = [w[x] - m * t * h[x] for x in range(m)]
        if any(wp[x] <= m for x in range(1, m)): return None
        for i in range(1, m):
            for j in range(i, m):
                if wp[i] + wp[j] < wp[(i + j) % m]: return None
        mx = max(wp)
        if h[wp.index(mx)] != hs: return None
        return wp
    t = 0
    while valid(t + 1) is not None: t += 1
    if t == 0: continue
    applied += 1; wp = valid(t)
    Wp, info = indep_W([m] + wp[1:])
    lhs = D['W'] - Wp; rhs = t * X
    assert lhs >= rhs, ("DESCENT FAILS", G, t, D['W'], Wp, X)
    if info['c'] <= 4 * m: to4 += 1
    r = (lhs - rhs, sorted(G), t, D['W'], Wp, X, D['c'] / m, info['c'] / m)
    if worst is None or r[0] < worst[0]: worst = r
print("graded S tested %d (c > 4m); descent applicable (t >= 1) %d; landed at c' <= 4m %d" % (tested, applied, to4))
print("min slack (W - W' - tX, G, t, W, W', X, c/m, c'/m):", worst)
