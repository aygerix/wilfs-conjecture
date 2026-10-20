r"""Carry Lemma CL (T_c <= U_unc) on exhaustive P18 depth-four semigroups (lead, 2026-10-20). usage: cl4.py k mlo mhi"""
import sys, itertools
from carry import analyse
k, mlo, mhi = map(int, sys.argv[1:4]); n = 0; bad = []; mn = None; mnh = None
for m in range(mlo, mhi + 1):
    for B in itertools.combinations(range(1, m), k):
        r = analyse([m] + [m + b for b in B])
        if r is None or r["q"] != 4: continue
        n += 1
        if r["CL"] < 0: bad.append(r)
        if mn is None or r["CL"] < mn["CL"]: mn = r
        if r["h"] > r["e"] and (mnh is None or r["CL"] < mnh["CL"]): mnh = r
print(sys.argv[1:], "depth-four S", n, "CL fails", len(bad), "min CL", mn and mn["CL"], mn, "\n  min over h>e", mnh)
