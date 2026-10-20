"""Tightest P18 depth-four cases of SIG = Q4 + sigT (lead, 2026-10-20), with the CARRY-ID breakdown.
SIG = slA + slB - q - 2 Pw.  usage: exh k mlo mhi [top]"""
import sys, itertools
sys.path.insert(0, "../p30")
import payers, jid
k, mlo, mhi = map(int, sys.argv[2:5]); top = int(sys.argv[5]) if len(sys.argv) > 5 else 12
rows = []
for m in range(mlo, mhi + 1):
    for B in itertools.combinations(range(1, m), k):
        d = payers.comps(m, B)
        if not d: continue
        r = jid.info(m, B)
        sig = d["Q4"] + d["sigT"]
        assert sig == r["slA"] + r["slB"] - r["q"] - 2 * d["Pw"], (m, B)
        rows.append((sig, m, B, d, r))
rows.sort(key=lambda t: t[0])
print(sys.argv[1:], "S:", len(rows), "SIG failures:", sum(1 for t in rows if t[0] < 0))
for sig, m, B, d, r in rows[:top]:
    print(" SIG", sig, "m", m, "B", B, "h", d["h"], "W", d["W"], "Q4", d["Q4"], "sigT", d["sigT"], "Pw", d["Pw"], "p", r["p"], "q", r["q"], "qres", r["qres"], "N4", r["H4"], "T", r["T"], "u2", r["d2"], "L3", d["L3"], "incU", r["incU"], "incC", r["incC"], "defU", r["defU"], "slB", r["slB"])
