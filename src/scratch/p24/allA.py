r"""All-A P18 depth four (lead, 2026-10-20): exact identity W = E1 + E2 + E3 - U1 - (e-4)delta + 4nu + 4Omega,
Omega = U1 - P_lo - |H4b| (carried cubes that do not create a new level-4 residue outside 4A).
Checks the identity and the 'free part' F = E2 + 4nu + 4Omega - U1 - (e-4)delta (without the collision slacks E1, E3).
usage: python allA.py exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
from math import gcd
sys.path.insert(0, '.')
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
    h = c - 3 * m
    if max(B) >= h: return None
    g = sum(x // m for x in w); W = e * (c - g) - c
    X2 = set(a + b for a in A for b in A); X3 = set(s + a for s in X2 for a in A); X4 = set(s + a for s in X3 for a in A)
    E1 = e * (e + 1) - 2 * len(X2)
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    E2 = (e - 1) * y0 - 4 * N4
    L = m + h
    E3 = (e + 2) * sum(1 for s in X2 if s < L) - 3 * sum(1 for s in X3 if s < L)
    U1 = sum(1 for s in X3 if m <= s < m + h)
    Plo = sum(1 for s in X2 if m <= s < m + h)
    C2lo = set(s - m for s in X2 if m <= s < m + h) - X3
    delta = Plo - len(C2lo)
    nu = sum(1 for s in X4 if s < h and s not in X3 and s in C2lo)
    level4 = [r for r in range(h) if w[r] // m == 4]
    H4b = [r for r in level4 if r not in X4]
    Omega = U1 - Plo - len(H4b)
    ident = E1 + E2 + E3 - U1 - (e - 4) * delta + 4 * nu + 4 * Omega
    F = E2 + 4 * nu + 4 * Omega - U1 - (e - 4) * delta
    return dict(m=m, B=tuple(B), h=h, e=e, W=W, ident=ident, E1=E1, E2=E2, E3=E3, U1=U1, Plo=Plo, delta=delta, nu=nu, Omega=Omega, F=F)
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
            m = random.randint(mlo, mhi); h0 = random.randint(m // 3, m)
            B = sorted(random.sample(range(1, max(k + 1, h0)), k))
            gg = m
            for b in B: gg = gcd(gg, b)
            if gg != 1: continue
            r = run(m, B)
            if r: recs.append(r)
    bad = [r for r in recs if r["ident"] != r["W"]]
    print(len(recs), "all-A depth-four S; identity mismatches", len(bad))
    if bad: print("  e.g.", bad[0])
    mF = min(recs, key=lambda r: r["F"]); print("min free part F", mF["F"], "neg:", sum(1 for r in recs if r["F"] < 0), mF)
    mW = min(recs, key=lambda r: r["W"]); print("min W", mW["W"], mW)
    # FREE-A and FA2 directly
    def y0f(r): return None
    fa2 = [r["E2"] - r["U1"] - (r["e"] - 4) * r["delta"] for r in recs]
    print("FA2 (E2 - U1 - (e-4)delta >= 0): neg", sum(1 for v in fa2 if v < 0), "min", min(fa2))
    worst = min(recs, key=lambda r: r["E2"] - r["U1"] - (r["e"] - 4) * r["delta"]); print("   worst", worst)
