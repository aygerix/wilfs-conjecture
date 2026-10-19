"""Anatomy of chain deficit vs overlap excess (lead, 2026-10-19).
For each Apery element w: layer lam(w), s_w, con(w) = sum_a (s_w - (M - top_a(w))), E(w) = sum_a n_a depth_a(w) - w,
Eu(w) = max(0, sum_{a: w - n_a in S} n_a - w), |U(w)|, least factorization length.  Aggregates by layer and by length.
usage: python anatomy.py m g1,g2,...  (generators other than m)"""
import sys, heapq
sys.path.insert(0, '../p18')
from chain_interval import apery
m = int(sys.argv[1]); g = [int(x) for x in sys.argv[2].split(',')]
w = apery(m, [m] + g); ap = set(w); M = max(w); c = M - m + 1
gens = sorted(x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m))
d = len(gens); C2 = m*(m-1)//2; need = (d-1)*C2
ml = {0: 0}
for x in sorted(w)[1:]: ml[x] = min(1 + ml[x - n] for n in gens if x - n in ml)
rows = []
for x in sorted(w):
    s = (M - x) % m; lam = (M - x) // m
    con = 0
    for n in gens:
        t = x
        while t + n in ap: t += n
        con += s - (M - t)
    dep = 0
    for n in gens:
        y = x
        while y - n in ap: y -= n; dep += n
    E = dep - x
    U = [n for n in gens if x - n in ap]
    Eu = max(0, sum(U) - x)
    rows.append((x, lam, s, con, E, Eu, len(U), ml[x]))
Delta = sum(r[3] for r in rows); E = sum(r[4] for r in rows); Eu = sum(r[5] for r in rows)
print('m=%d d=%d M=%d c=%d need=%d C2=%d Delta=%d (Delta-C2=%d = chain deficit) E=%d Eu=%d' % (m, d, M, c, need, C2, Delta, Delta - C2, E, Eu))
print('by layer: lam, #elts, sum con, sum E, sum Eu, mean |U|')
for L in sorted(set(r[1] for r in rows)):
    R = [r for r in rows if r[1] == L]
    print('  %d %3d %8d %8d %8d %.2f' % (L, len(R), sum(r[3] for r in R), sum(r[4] for r in R), sum(r[5] for r in R), sum(r[6] for r in R)/len(R)))
print('by least length: h, #elts, sum con, sum E, sum Eu')
for h in sorted(set(r[7] for r in rows)):
    R = [r for r in rows if r[7] == h]
    print('  %d %3d %8d %8d %8d' % (h, len(R), sum(r[3] for r in R), sum(r[4] for r in R), sum(r[5] for r in R)))
