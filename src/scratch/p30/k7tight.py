"""Tight cases of K7: defU + slB - p - q (<= lim), printed with the carried structure."""
import sys, itertools, jid
k, mlo, mhi, lim = map(int, sys.argv[1:5]); shown = 0; mn = None
for m in range(mlo, mhi + 1):
    for B in itertools.combinations(range(1, m), k):
        r = jid.info(m, B)
        if not r: continue
        v = r["defU"] + r["slB"] - r["p"] - r["q"]
        if mn is None or v < mn: mn = v
        if v <= lim and shown < 12:
            shown += 1; print(v, {x: r[x] for x in ("m", "B", "h", "W", "p", "plo", "q", "qres", "H4", "y", "defU", "slB", "ni", "nii", "d2el", "incU", "incC")})
print("min K7", mn)
