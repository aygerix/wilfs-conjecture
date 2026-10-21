# U != T near-tight constructions: T_t = <mu, (t-1)mu+1, [t mu+2, (t+1)mu+1]>, m = (t+1)mu+1, A = gens \ {m} plus a padding
# set of multiples k*mu (2 <= k <= 2t+2, at most 3 of them); keep the covering ones with U != T, report the min ratio
import sys
from itertools import combinations
src = open(sys.argv[1]).read().split('for d in range')[0]; exec(src)   # stats(A, m) from fam.py
for t in range(4, 9):
    for mu in (8, 12, 16, 24):
        base = [mu, (t - 1) * mu + 1] + list(range(t * mu + 2, (t + 1) * mu + 1)); m = (t + 1) * mu + 1
        best = None
        for p in range(0, 4):
            for pad in combinations([k * mu for k in range(2, 2 * t + 3) if k * mu < m and k != t - 1], p):
                A = sorted(set(base) | set(pad)); r = stats(A, m)
                if r is None: continue
                c, l, ne = r
                if not ne or c == 0: continue
                e = len(A) + 1; rt = e * l / c
                if best is None or rt < best[0]: best = (rt, len(A), c, l, e * l - c, pad)
        print(f"t={t} mu={mu} m={m}", "none" if best is None else f"ratio={best[0]:.4f} d={best[1]} c={best[2]} l={best[3]} slack={best[4]} pad={best[5]}")
