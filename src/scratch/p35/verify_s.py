r"""Independent verification of a semigroup's invariants and its case (lead, 2026-10-20).
(1) Direct: membership by dynamic programming up to a safe bound; conductor c, genus g, ell = c - g, minimal
generators (elements not sums of two smaller nonzero elements), e, W = e*ell - c.  No Apery/tile code.
(2) Tile: ../p34/tile.build (lex factorization tile) and tcldich.stats (Dep, Sigma_supp), height, and the
SUPP-WILF bounds W >= Dep - Sigma_supp.
Usage: python verify_s.py m g1 g2 ..."""
import sys
sys.path.insert(0, '../p34')
from tile import build
from tcldich import stats
G = list(map(int, sys.argv[1:])); m = min(G)
B = sum(G) * 3 + max(G) * max(G)
inS = bytearray(B + 1); inS[0] = 1
for n in range(1, B + 1):
    for g in G:
        if n >= g and inS[n - g]: inS[n] = 1; break
F = max(n for n in range(B + 1) if not inS[n]); assert F < B - max(G) - 1, "bound too small"
c = F + 1; g = sum(1 for n in range(c) if not inS[n]); ell = c - g
S_el = [n for n in range(1, c + max(G) + 1) if inS[n]]
mingens = [s for s in S_el if not any(inS[a] and inS[s - a] for a in range(1, s) if a <= s - a)]
e = len(mingens); W = e * ell - c
print("direct: m=%d c=%d g=%d ell=%d e=%d W=%d  minimal generators %s" % (m, c, g, ell, e, W, mingens))
c2, gens, M = build(m, G); D = list(M)
v, dep, ss = stats(m, D, [x % m for x in gens])
h = max(sum(x) for x in D)
print("tile:   c=%d gens=%s height=%d Dep=%d Sigma_supp=%d mu=%d case=%s  open(c>4m, 3e<m)=%s  minV(TileCL)=%d" % (
    c2, gens, h, dep, ss, ss - dep, 'B' if dep < ss else 'A', 3 * e < m and c > 4 * m, v))
print("checks: conductor agree %s, generators agree %s, W >= Dep - Sigma_supp: %s" % (c == c2, sorted(gens + [m]) == mingens, W >= dep - ss))
cubics = [x for x in D if sum(x) == 3]
print("height-3 cells:", cubics, " their Apery elements:", [sum(a * b for a, b in zip(x, gens)) for x in cubics])
