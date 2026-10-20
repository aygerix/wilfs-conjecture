r"""DEAD on S = <m, a..a+d> for larger m: per m, the max of (Lam-O)/W and the min of D = W - (Lam-O) over S with
Lam > O, scanning a in [m+1, 2m], d in [1, m-1] (lead, 2026-10-20).  usage: deadivl2.py m1 m2 step"""
import sys
from dead import info
m1, m2, st = map(int, sys.argv[1:4])
for m in range(m1, m2 + 1, st):
    br = bd = None
    for a in range(m + 1, 2 * m + 1):
        for d in range(1, m):
            r = info([m] + list(range(a, a + d + 1)))
            if r is None or r["W"] <= 0 or r["Lam"] == r["O"]: continue
            r["rat"] = (r["Lam"] - r["O"]) / r["W"]
            if br is None or r["rat"] > br["rat"]: br = r
            if bd is None or r["D"] < bd["D"]: bd = r
            if r["D"] < 0: print("FAIL", r, flush=True)
    for tag, b in (("maxrat", br), ("minD", bd)):
        print(m, tag, round(b["rat"], 4), "D", b["D"], "W", b["W"], "Lam-O", b["Lam"] - b["O"], "e", b["e"], "c", b["c"], "gens", b["gens"][1], "..", b["gens"][-1], flush=True)
