r"""Height-3 case-B lex tiles with small lifts, ties allowed (lead, 2026-10-20).
For each affine image delta of a cover of Z/m and NR random lift vectors in {KLO..KHI}, build S = <m, m k_a + delta_a>,
its lex tile (../p34/tile.build: lex-least factorizations, ties broken lexicographically), and keep S whose tile has
height >= 3 and Dep < Sigma_supp.  Prints each kept S once (for multin.py).  Usage: python smalllift.py m A KLO KHI NR SEED"""
import sys, math, random
sys.path.insert(0, '../p34')
from tile import build
from tcldich import stats
m = int(sys.argv[1]); A = [int(t) for t in sys.argv[2].split(',')]; KLO, KHI, NR, SEED = map(int, sys.argv[3:7])
rnd = random.Random(SEED); seen = set(); cnt = {}
imgs = sorted({tuple(sorted({(u * (x - a)) % m for x in A} - {0})) for u in range(1, m) if math.gcd(u, m) == 1 for a in A})
for dl in imgs:
    for _ in range(NR):
        G = [m] + [rnd.randint(KLO, KHI) * m + x for x in dl]
        R = build(m, G)
        if R is None: continue
        c, gens, M = R; D = list(M); h = max(sum(x) for x in D)
        v, dep, ss = stats(m, D, [g % m for g in gens])
        key = (h >= 3, dep < ss); cnt[key] = cnt.get(key, 0) + 1
        if h >= 3 and dep < ss and tuple(gens) not in seen:
            seen.add(tuple(gens)); print("KEEP c=%d c/m=%.2f height=%d mu=%d S: %d %s" % (c, c / m, h, ss - dep, m, ' '.join(map(str, gens))), flush=True)
print("counts (height>=3, caseB):", cnt, file=sys.stderr)
