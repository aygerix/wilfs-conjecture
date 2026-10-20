"""Regime 2h <= m, two-window bound (lead, 2026-10-20).  PROVED: W >= e*y0 - 3N4 - h + p_hi + p_lo + 2 d2el + incU + incC.
Window bounds: Fb = |3A n [h,2h)| + p_[h,2h)  (full first window),  Hb = 2(|3A n W1| + p_W1), W1 = [h, h + ceil(h/2)).
Test R3 = e*y0 - 3N4 + p_hi + p_lo + 2 d2el + incU + incC - min(Fb, Hb) >= 0 and the local R3L (E1 in place of the
slack terms, carried pairs ignored): e*y0 - 3N4 + E1 - min(|3A n [h,2h)|, 2|3A n W1|)."""
import sys, itertools, random, jid
def ev(m, B):
    r = jid.info(m, B)
    if not r or 2 * r["h"] > m: return None
    h = r["h"]; A = [0] + sorted(B); e = len(A); hw = h + (h + 1) // 2
    X2 = set(a + b for i, a in enumerate(A) for b in A[i:]); X3 = set(s + a for s in X2 for a in A)
    S2 = set(v for v in X2 if v < m) | set(A)
    T = set(v for v in X3 if v < m) - S2
    CP = set(v - m for v in X2 if v >= m) - S2 - T
    E1 = e * (e + 1) - 2 * len(X2)
    tF = sum(1 for v in X3 if h <= v < 2 * h); tH = sum(1 for v in X3 if h <= v < hw)
    pF = sum(1 for u in CP if h <= u < 2 * h); pH = sum(1 for u in CP if h <= u < hw); phi = sum(1 for u in CP if u >= h)
    y0 = r["y"] - r["plo"]; N4 = r["H4"]
    base = e * y0 - 3 * N4 + phi + r["plo"] + 2 * r["d2el"] + r["incU"] + r["incC"]
    assert r["W"] >= base - h
    Fb = tF + pF; Hb = 2 * (tH + pH); assert h <= Fb and h <= Hb, (m, B, h, Fb, Hb)
    return dict(R3=base - min(Fb, Hb), R3F=base - Fb, R3H=base - Hb, R3L=e * y0 - 3 * N4 + E1 - min(tF, 2 * tH),
                W=r["W"], m=m, B=r["B"], h=h, e=e, y0=y0, N4=N4, tF=tF, tH=tH, E1=E1, a=r["a"])
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
        for key in ("R3", "R3F", "R3H", "R3L"):
            if key not in mins or d[key] < mins[key][key]: mins[key] = d
            if d[key] < 0: fails[key] = fails.get(key, 0) + 1
    print(sys.argv[1:], "S with 2h<=m:", n, "failures:", fails)
    for key in mins: print("  min", key, {x: mins[key][x] for x in ("R3", "R3F", "R3H", "R3L", "W", "m", "B", "h", "e", "y0", "N4", "tF", "tH", "E1", "a")})
