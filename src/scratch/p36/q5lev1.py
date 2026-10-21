r"""q = 5, height <= 3, all generators of level 1 (lead, 2026-10-21).  Exact count
    l = 5 + sum_g (4 - [g>r]) + sum_P (3 - carry_p - [p>r]) + sum_C (2 - carries_z - [z>r]),  every term >= 0,
so l >= 5 + 3d + |P| and Wilf holds whenever e(3d + |P| + 5) >= c = 4m + r + 1.  Check on all unit rescalings of the
dense covers with all levels 1 (plus random residue sets): assert the identity and the bound, report how often the
sufficient condition fails, and for those the number Z of cubic cells with mu_z = 0.
usage: /usr/bin/python3 q5lev1.py NRAND SEED FILE [FILE ..]"""
import sys, re, math, random
sys.path.insert(0, '.')
from kunz_face import apery
def check(G, stats):
    m = min(G); w = apery(m, G); Ws = set(w)
    gens = [s for s in range(1, m) if not any(w[s] - w[i] in Ws and 0 < w[s] - w[i] for i in range(1, m) if w[i] < w[s])]
    if any(w[g] // m != 1 for g in gens): return
    e = len(gens) + 1; d = e - 1; c = max(w) - m + 1; q = -(-c // m)
    if q != 5: return
    r = w.index(max(w)); g = sum(x // m for x in w); l = c - g; W = e * l - c
    mu = [max(0, -((w[s] - c) // m)) for s in range(m)]; mu[0] = q
    k = [x // m for x in w]   # level = length + carries for level-1 generators
    if max(k) > 5: return
    # height via shortest factorization length h = k - carries; classify by k and residue sums is implicit: compute lengths by DP
    INF = 99; h = [INF] * m; h[0] = 0
    for s in sorted(range(1, m), key=lambda x: w[x]):
        if s in gens: h[s] = 1
        else: h[s] = min(h[(s - i) % m] + 1 for i in gens if w[s] - w[i] in Ws and w[s] > w[i] and h[(s - i) % m] < INF and w[(s - i) % m] == w[s] - w[i])
    if max(h) > 3: return
    P = [s for s in range(1, m) if h[s] == 2]; C = [s for s in range(1, m) if h[s] == 3]
    terms = 5 + sum(4 - (1 if s > r else 0) for s in gens) + sum(3 - (k[s] - 2) - (1 if s > r else 0) for s in P) + sum(2 - (k[s] - 3) - (1 if s > r else 0) for s in C)
    assert terms == l, (G, terms, l)
    bad = [(s, 'P', k[s], s > r) for s in P if 3 - (k[s] - 2) - (s > r) < 1] + [(s, 'C', k[s], s > r) for s in C if 2 - (k[s] - 3) - (s > r) < 0]
    assert not bad, (sorted(G), r, bad, [(x, h[x], k[x]) for x in range(m)])
    assert l >= 5 + 3 * d + len(P) and c == 4 * m + r + 1
    stats['n'] += 1
    cond = e * (3 * d + len(P) + 5) >= c
    if not cond:
        stats['fail'] += 1; Z = sum(1 for s in C if mu[s] == 0)
        rec = (W, sorted(G), m, d, len(P), len(C), Z, r)
        if stats['worst'] is None or W < stats['worst'][0]: stats['worst'] = rec
    stats['minW'] = min(stats['minW'], (W, sorted(G)))
stats = dict(n=0, fail=0, worst=None, minW=(10**9, None))
NR, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
for fn in sys.argv[3:]:
    for line in open(fn):
        mm = re.match(r'm=(\d+) d=(\d+) s=([0-9,]+)', line)
        if not mm: continue
        m = int(mm.group(1)); s0 = [int(t) for t in mm.group(3).split(',')]
        for u in range(1, m):
            if math.gcd(u, m) == 1: check([m] + [m + (u * x % m) for x in s0], stats)
for _ in range(NR):
    m = rng.randint(12, 60); d = rng.randint(3, 8)
    if d >= m - 1: continue
    check([m] + [m + x for x in rng.sample(range(1, m), d)], stats)
print("q=5, height<=3, level-1 generators: %d S; sufficient condition e(3d+|P|+5) >= c fails on %d" % (stats['n'], stats['fail']))
print("worst W among failures (W, G, m, d, |P|, |C|, #cubic cells with mu=0, r):", stats['worst'])
print("min W overall:", stats['minW'])
