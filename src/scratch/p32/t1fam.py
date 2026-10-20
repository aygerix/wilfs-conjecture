"""Conjecture T1 (lead, 2026-10-20): sum_y (j_y - c_y) <= rho + r, i.e. E + r >= P (ID-q pool), on P18 truncation
families (window model (m, rho, B), q, via idq.canon). Families: Fromentin-type examples, <30,44,48,49>_118,
EF B3 family (random B3 offsets in ((m+1)/2, (2m-1)/3), c = 4m), Delgado <mu, gamma, gamma+1>_{p mu} with E < 0.
Usage: python t1fam.py MUMAX PMAX NEF SEED"""
import sys, random, itertools
sys.path.insert(0, __import__('os').path.dirname(__file__))
from idq import canon
def t1(m, rho, B, q):
    K = len(B); best = canon(m, rho, B, q, q + 3)
    reach = {x: v for x, v in best.items() if v[0] <= q}
    if (m - 1) not in reach or reach[m - 1][0] < q:
        if not ((m - 1) in best and best[m - 1][0] >= q): return None   # c(T) = qm - rho needs lam(m-1) >= q
    d = len(reach); r = m - d; ell = sum(q - v[0] for v in reach.values()); E = (K + 1) * ell - q * d + rho
    JC = 0; P = 0
    for x, (lx, tx, cx, ax) in reach.items():
        JC += (lx - tx) - sum(ax[i] for i, b in enumerate(B) if ax[i] > 0 and b > x)
        for i, b in enumerate(B):
            y = (x + b) % m; ay = tuple(ax[k] + (k == i) for k in range(K))
            if not (y in reach and reach[y][3] == ay): P += (q - lx) * (ax[i] + 1)
    assert E == rho + P - JC
    return dict(E=E, r=r, P=P, JC=JC, T1=rho + r - JC, CORE1=E + r)
MUMAX, PMAX, NEF, SEED = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
def model(A, c):
    m = min(A); q = -(-c // m); rho = q * m - c; return m, rho, sorted(a - m for a in A if a != m), q
for A, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68), ((18, 28, 29), 72), ((30, 44, 48, 49), 118)]:
    m, rho, B, q = model(A, c); print("known", A, c, t1(m, rho, B, q))
# EF B3 family
worst = None; cnt = 0
for it in range(NEF):
    m = rnd.randint(20, 160); lo, hi = (m + 2) // 2, (2 * m - 2) // 3
    if hi - lo < 4: continue
    K = rnd.randint(3, 8); B = []
    for b in rnd.sample(range(lo, hi + 1), hi - lo + 1):
        Bt = sorted(B + [b])
        sums = set()
        ok = True
        for t in range(1, 4):
            for comb in itertools.combinations_with_replacement(Bt, t):
                s = sum(comb)
                if s in sums: ok = False; break
                sums.add(s)
            if not ok: break
        if ok: B = Bt
        if len(B) == K: break
    s = t1(m, 0, B, 4)
    if s is None: continue
    cnt += 1
    if worst is None or s['T1'] < worst[0]: worst = (s['T1'], m, B, s)
print("EF B3:", cnt, "models; worst T1", worst)
# Delgado-type with E < 0
worst = None; cnt = 0; neg = 0
for p in range(3, PMAX + 1):
    for mu in range(5, MUMAX + 1):
        for g in range(mu + 1, 2 * mu - 1):
            s = t1(mu, 0, [g - mu, g + 1 - mu], p)
            if s is None: continue
            cnt += 1
            if s['E'] < 0:
                neg += 1
                if worst is None or s['T1'] < worst[0]: worst = (s['T1'], mu, g, p, s)
print("Delgado:", cnt, "truncations,", neg, "with E < 0; worst T1 among them", worst)
