r"""General P18 depth four (lead, 2026-10-20). Exact identity
   W = E1 + E2 + E3 + b*y0 - U1 - P_hi + 3*delta_hi - (e-4)*delta + 4*nu + 4*Omega,
and the collision-free part F_gen = (e+3)*y0 + 3*U1 + 3*delta_hi - 4h - e*delta - P_hi = W - E1 - E3 (FREE-GEN: F_gen >= 0).
usage: python p18free.py exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
from math import gcd
def run(m, B):
    A = [0] + sorted(B); e = len(A)
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for b in B:
            v = d0 + m + b; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    M = max(w); c = M - m + 1
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m; g = sum(x // m for x in w); W = e * (c - g) - c
    a = sum(1 for x in B if x < h); bb = e - 1 - a
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    E1 = e * (e + 1) - 2 * len(X2)
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    E2 = a * y0 - 4 * N4
    E3 = (e + 2) * sum(1 for s in X2 if s < m + h) - 3 * sum(1 for s in X3 if s < m + h)
    U1 = sum(1 for s in X3 if m <= s < m + h)
    Plo = sum(1 for s in X2 if m <= s < m + h); Phi = sum(1 for s in X2 if m + h <= s < 2 * m)
    delta = sum(1 for s in X2 if m <= s < m + h and (s - m) in X3)
    dhi = sum(1 for s in X2 if m + h <= s < 2 * m and (s - m) in X3)
    C2lo = set(s - m for s in X2 if m <= s < m + h) - X3
    nu = sum(1 for s in X4 if s < h and s not in X3 and s in C2lo)
    level4 = [r for r in range(h) if w[r] // m == 4]
    H4b = [r for r in level4 if r not in X4]
    Omega = U1 - Plo - len(H4b)
    ident = E1 + E2 + E3 + bb * y0 - U1 - Phi + 3 * dhi - (e - 4) * delta + 4 * nu + 4 * Omega
    F = (e + 3) * y0 + 3 * U1 + 3 * dhi - 4 * h - e * delta - Phi
    E3f = (e - 1) * len(X2) - 3 * len(X3 - X2)
    Ffull = W - E1 - E3f
    return dict(m=m, B=tuple(B), h=h, e=e, a=a, W=W, ident=ident, F=F, Ffull=Ffull, E3f=E3f, E1=E1, E2=E2, E3=E3, y0=y0, U1=U1, Plo=Plo, Phi=Phi, delta=delta, dhi=dhi, nu=nu, Omega=Omega)
if __name__ == "__main__":
    recs = []
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                gg = m
                for b in B: gg = gcd(gg, b)
                if gg != 1: continue
                r = run(m, B)
                if r: recs.append(r)
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k))
            gg = m
            for b in B: gg = gcd(gg, b)
            if gg != 1: continue
            r = run(m, B)
            if r: recs.append(r)
    bad = [r for r in recs if r["ident"] != r["W"] or r["W"] - r["E1"] - r["E3"] != r["F"]]
    print(len(recs), "P18 depth-four S; identity mismatches", len(bad), bad[:1])
    mF = min(recs, key=lambda r: r["F"]); print("FREE-GEN: neg", sum(1 for r in recs if r["F"] < 0), "min F", mF["F"], mF)
    for r in [r for r in recs if r["F"] < 0][:6]: print("  FAIL", r)
    big = [r for r in recs if r["h"] > r["e"]]
    print("restricted to h > e:", len(big), "S; FREE-GEN neg", sum(1 for r in big if r["F"] < 0), "min F", min(r["F"] for r in big) if big else None)
    if big:
        mb = min(big, key=lambda r: r["F"]); print("   worst", mb)
        print("   h<=e failures:", sum(1 for r in recs if r["F"] < 0 and r["h"] <= r["e"]))
    print("FREE-FULL (W - E1 - E3full >= 0): neg", sum(1 for r in recs if r["Ffull"] < 0), "; with h > e:", sum(1 for r in big if r["Ffull"] < 0))
    mf = min(recs, key=lambda r: r["Ffull"]); print("   min Ffull", mf["Ffull"], mf)
    mfb = min(big, key=lambda r: r["Ffull"]); print("   min Ffull (h>e)", mfb["Ffull"], mfb)
