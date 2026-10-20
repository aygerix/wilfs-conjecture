r"""Brute force over ALL B c [1, m-1] (lead, 2026-10-20): per h, min W and min TB4 over P18 depth-four S with c = 3m + h.
Cross-check for cpsat_p18.py minW / minTB4.  usage: python brute_p18.py m"""
import sys, itertools
sys.path.insert(0, '.')
from cpsat_p18 import verify
m = int(sys.argv[1]); best = {}
for k in range(1, m):
    for B in itertools.combinations(range(1, m), k):
        r = verify(m, B)
        if r is None or not (3 * m < r["c"] <= 4 * m): continue
        b = best.setdefault(r["h"], [10**9, 10**9, 0])
        b[0] = min(b[0], r["W"]); b[1] = min(b[1], r["TB4"]); b[2] += 1
for h in sorted(best): print(f"m={m} h={h}: count {best[h][2]} minW {best[h][0]} minTB4 {best[h][1]}")
