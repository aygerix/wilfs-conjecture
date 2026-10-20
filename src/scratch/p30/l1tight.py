"""List tight cases of L1 (incU + incC - qres small, qres > 0) at P18 depth four, with the unused incidences."""
import sys, itertools, jid
k, mlo, mhi, lim = map(int, sys.argv[1:5]); shown = 0
for m in range(mlo, mhi + 1):
    for B in itertools.combinations(range(1, m), k):
        r = jid.info(m, B)
        if not r or r["qres"] == 0: continue
        sl = r["incU"] + r["incC"] - r["qres"]
        if sl <= lim and shown < 25:
            shown += 1; print(sl, {x: r[x] for x in ("m", "B", "h", "W", "p", "plo", "q", "qres", "incU", "incC", "d2el", "defU", "slB", "ni", "nii")})
