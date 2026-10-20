"""Regime 2h <= m at P18 depth four (lead, 2026-10-20).  PROVED: W >= R2 := e*y0 - 3*N4 - |3A n [h,2h)| + 2*d2el + incU
+ incC + p_lo.  Test R2 >= 0 and the local versions R2L := e*y0 + E1 - 3*N4 - min(h, |3A n [h,2h)|), R2T := e*y0 + E1 -
3*N4 - |3A n [h,2h)|.  usage like jid.py (exh / rnd)."""
import sys, itertools, random, jid
def ev(m, B):
    r = jid.info(m, B)
    if not r or 2 * r["h"] > m: return None
    h = r["h"]; A = [0] + sorted(B); e = len(A)
    X2 = set(a + b for i, a in enumerate(A) for b in A[i:]); X3 = set(s + a for s in X2 for a in A)
    E1 = e * (e + 1) - 2 * len(X2); t = sum(1 for v in X3 if h <= v < 2 * h)
    y0 = r["y"] - r["plo"]; N4 = r["H4"]
    R2 = e * y0 - 3 * N4 - t + 2 * r["d2el"] + r["incU"] + r["incC"] + r["plo"]
    assert r["W"] >= R2, (m, B, r["W"], R2)
    return dict(R2=R2, R2L=e * y0 + E1 - 3 * N4 - min(h, t), R2T=e * y0 + E1 - 3 * N4 - t, W=r["W"], m=m, B=r["B"], h=h,
                e=e, y0=y0, N4=N4, t=t, E1=E1, a=r["a"])
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
        for key in ("R2", "R2L", "R2T"):
            if key not in mins or d[key] < mins[key][key]: mins[key] = d
            if d[key] < 0: fails[key] = fails.get(key, 0) + 1
    print(sys.argv[1:], "S with 2h<=m:", n, "(W >= R2 asserted)", "failures:", fails)
    for key in mins: print("  min", key, mins[key])
