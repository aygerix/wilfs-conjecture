"""Regime 2h <= m at P18 depth four (lead, 2026-10-20).  PROVED: W >= slB - q + p_hi + 2 d2el + incU + incC and
slB >= OVF := #{(t, b) in (3A n [0,h)) x B : t + b >= h}.  So Wilf <= Z3 := OVF + p_hi + 2 d2el + incU + incC - q >= 0.
Test Z0 = OVF - q, Z1 = OVF + p_hi - q, Z2 = OVFw + p_hi - qres (OVFw: overflow tokens with sum in [h, 2h)),
Z3, Z4 = OVF - qres, Z5 = OVFw - qres, Z6 = OVF + incU + incC - q.  usage like r3.py."""
import sys, itertools, random, jid
def ev(m, B):
    r = jid.info(m, B)
    if not r or 2 * r["h"] > m: return None
    h = r["h"]; A = [0] + sorted(B); e = len(A)
    X2 = set(a + b for i, a in enumerate(A) for b in A[i:]); X3 = set(s + a for s in X2 for a in A)
    S2 = set(v for v in X2 if v < m) | set(A)
    T = set(v for v in X3 if v < m) - S2
    CP = set(v - m for v in X2 if v >= m) - S2 - T
    phi = sum(1 for u in CP if u >= h)
    src = [t for t in X3 if t < h]
    OVF = sum(1 for t in src for b in B if t + b >= h)
    OVFw = sum(1 for t in src for b in B if h <= t + b < 2 * h)
    q, qres = r["q"], r["qres"]
    S3 = set(src); toks = {}
    for t in src:
        for b in B:
            if h <= t + b < 2 * h: toks[t + b] = toks.get(t + b, 0) + 1
    V = set(toks); core = sum(1 for v in X3 if h <= v < 2 * h and v not in V)
    extra = sum(toks.values()) - len(V)
    big = sum(1 for t in src for b in B if t + b >= 2 * h)
    plo = r["plo"]; p2h = sum(1 for u in CP if u >= 2 * h)
    assert r["W"] >= r["slB"] - q + phi + 2 * r["d2el"] + r["incU"] + r["incC"]
    assert r["slB"] >= OVF
    d = dict(Z0=OVF - q, Z1=OVF + phi - q, Z2=OVFw + phi - qres, Z3=OVF + phi + 2 * r["d2el"] + r["incU"] + r["incC"] - q,
             Z4=OVF - qres, Z5=OVFw - qres, Z6=OVF + r["incU"] + r["incC"] - q,
             Z13=OVF + phi + r["Nover"] - q, Z14=OVF + r["Nover"] - q,
             Z10=OVF + len(src) + sum(1 for u in CP if h <= u < 2 * h) - h, Z11=OVF + len(src) + phi - h,
             Z12=OVF + len(src) - sum(1 for v in X3 if h <= v < 2 * h),
             Z7=extra + len(src) + r["H4"] + plo + p2h + big - core, Z8=extra + len(src) - core)
    d.update(W=r["W"], m=m, B=r["B"], h=h, e=e, q=q, qres=qres, p=r["p"], phi=phi, OVF=OVF, OVFw=OVFw, a=r["a"], y0=len(src), core=core, extra=extra, big=big)
    return d
KEYS = ("Z0", "Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7", "Z8", "Z10", "Z11", "Z12", "Z13", "Z14")
if __name__ == "__main__":
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5]); gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        gen = ((m, sorted(random.sample(range(1, m), k))) for m in (random.randint(mlo, mhi) for _ in range(N)))
    n = 0; mins = {}; fails = {}
    for m, B in gen:
        d = ev(m, B)
        if not d: continue
        n += 1
        for key in KEYS:
            if key not in mins or d[key] < mins[key][key]: mins[key] = d
            if d[key] < 0: fails[key] = fails.get(key, 0) + 1
    print(sys.argv[1:], "S with 2h<=m:", n, "failures:", fails)
    for key in KEYS:
        if key in mins: print("  min", key, mins[key][key], {x: mins[key][x] for x in ("W", "m", "B", "h", "q", "qres", "p", "phi", "OVF", "OVFw", "a", "y0", "core", "extra", "big")})
