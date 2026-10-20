"""Finer necessity audit at P18 depth four (lead, 2026-10-20): sigT = WI + UI, WI = #{(s,b) in U2 x B : s + b >= m}
(wrapped incidences, never used by unwrapped triples), UI = sigT - WI >= 0.  Further WI = WIlo + WIhi by s + b < m + h or
not.  Reports failures of Q4 + WI, Q4 + UI, Q4 + WIlo, Q4 + WIhi, and min ratios.  usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random
sys.path.insert(0, "../p30")
import payers
def ev(m, B):
    d = payers.comps(m, B)
    if not d: return None
    A2 = set(B[i] + B[j] for i in range(len(B)) for j in range(i, len(B)))
    U2 = [s for s in A2 if s < m and s not in B]
    assert len(U2) == sum(1 for _ in U2)
    h = d["h"]
    WIlo = sum(1 for s in U2 for b in B if m <= s + b < m + h); WIhi = sum(1 for s in U2 for b in B if s + b >= m + h)
    WI = WIlo + WIhi; UI = d["sigT"] - WI
    assert UI >= 0, (m, B, d["sigT"], WI)
    return dict(d, WI=WI, UI=UI, WIlo=WIlo, WIhi=WIhi)
if __name__ == "__main__":
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5]); gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        gen = ((m, tuple(sorted(random.sample(range(1, m), k)))) for m in (random.randint(mlo, mhi) for _ in range(N)))
    keys = {"Q4+WI": lambda d: d["Q4"] + d["WI"], "Q4+UI": lambda d: d["Q4"] + d["UI"], "Q4+WIlo": lambda d: d["Q4"] + d["WIlo"], "Q4+WIhi": lambda d: d["Q4"] + d["WIhi"]}
    n = 0; fails = {x: 0 for x in keys}; worst = {}
    for m, B in gen:
        d = ev(m, list(B))
        if not d: continue
        n += 1
        for x, f in keys.items():
            v = f(d)
            if v < 0: fails[x] += 1
            if x not in worst or v < worst[x][0]: worst[x] = (v, d)
    print(sys.argv[1:], "S:", n, "failures:", fails)
    for x in keys: print("  min", x, worst[x][0], {y: worst[x][1][y] for y in ("m", "B", "h", "W", "Q4", "sigT", "WI", "UI", "WIlo", "WIhi", "L3", "d4")})
