"""Check of Theorem DEG2-WILF (lead, 2026-10-20). For S with every Apery element a sum of <= 2 minimal generators:
build the GRADED (degree, then lex) standard tile D (degree <= 2), verify: D is a down-set, injective; Lemma T2
identity; TM2 bound RHS - LHS >= lambda (n - |I|) >= 0 with lambda = (-c) mod m; W >= Phat; W >= 0.
Generators: random large-second-generator S and random S filtered by the degree condition.
Usage: python deg2check.py NS SEED MMAX"""
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from tile import apery
def check(m, G):
    w = apery(m, G)
    if w is None: return None
    c = max(w) - m + 1
    gens = sorted(x for i, x in enumerate(w) if i and not any(w[a] + w[(i - a) % m] == x for a in range(1, m) if (i - a) % m))
    n = len(gens); gi = {g: i for i, g in enumerate(gens)}
    D = {}
    for x in w:
        if x == 0: D[(0,) * n] = 0; continue
        if x in gi: a = [0] * n; a[gi[x]] = 1; D[tuple(a)] = x; continue
        best = None
        for i in range(n):
            for j in range(i, n):
                if gens[i] + gens[j] == x:
                    a = [0] * n; a[i] += 1; a[j] += 1; a = tuple(a)
                    if best is None or a[::-1] < best[::-1]: best = a
        if best is None: return 'deg3'
        D[best] = x
    assert len(D) == m
    for a in D:   # down-set
        for i in range(n):
            if a[i]:
                b = list(a); b[i] -= 1
                assert tuple(b) in D, (m, G, a)
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(n))
    lam = (-c) % m
    eps = {a: (x - c) % m for a, x in D.items()}
    mx = [a for a in D if all(up(a, i) not in D for i in range(n))]
    lhs = sum((sum(a) + n) * eps[a] for a in mx); rhs = (n + 1) * m * (m - 1) // 2
    I = sum(1 for a in D if sum(a) == 1)
    assert rhs - lhs >= lam * (n - I), (m, G)
    g = sum(x // m for x in w); W = (n + 1) * (c - g) - c
    P = Fr(0); top = Fr(0)
    for a, x in D.items():
        if x < c:
            for i in range(n):
                if up(a, i) not in D: P += Fr((a[i] + 1) * (c - x), m)
        else: top += Fr((sum(a) + n) * (x - c), m)
    assert W == Fr((n + 1) * (m - 1), 2) + P - top, (m, G)
    assert W >= P and W >= 0, (m, G)
    return W, float(P), c, m, n
NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED); ok = d3 = 0; deep = 0; minr = None
for _ in range(NS):
    m = rnd.randint(4, MMAX); k = rnd.randint(2, 12)
    lo = rnd.choice([m + 1, m + m // 2, 2 * m]); hi = lo + rnd.choice([m, 2 * m, 4 * m])
    G = [rnd.randint(lo, hi) for _ in range(k)]
    v = check(m, G)
    if v is None: continue
    if v == 'deg3': d3 += 1; continue
    ok += 1; deep += v[2] > 3 * m
    r = (v[0] - v[1]) / v[3]
    if minr is None or r < minr[0]: minr = (r, v)
print("degree<=2 S checked", ok, "(c > 3m:", deep, ") skipped deg>=3", d3, "min (W-Phat)/m", minr)
