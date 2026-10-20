r"""How big is sigma (RTCM slack) in the high-element regime?  (lead, 2026-10-20)
sigma = 3|Q+A| - (e+2)|Q| + E3f, Q = Dset u Pset_hi.  Compare sigma with (2a+1)*P_hi and a*P_hi (free-shadow surplus), and test
W >= F0' := V_free + (2a+1)P_hi, i.e. whether the free-shadow surplus is realized up to E3f.  Reports min of sigma - k*a*P_hi.
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
from math import gcd
def run(m, B):
    A = [0] + sorted(B); e = len(A)
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in B:
            v = d0 + m + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    M = max(w); c = M - m + 1
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m
    g = sum(x // m for x in w); W = e * (c - g) - c
    a = sum(1 for x in B if x < h); b = e - 1 - a
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A)
    E3f = (e + 2) * len(X2) - 3 * len(X3)
    Dset = [s for s in X2 if m <= s < m + h and (s - m) in X3]; Phs = [s for s in X2 if m + h <= s < 2 * m]
    Q = Dset + Phs; QA = set(q + x for q in Q for x in A)
    sigma = 3 * len(QA) - (e + 2) * len(Q) + E3f
    Ac = [0] + [x for x in B if x < h]
    shadow_c = len(set(q + x for q in Phs for x in Ac))
    known = h <= e or e * (e + 1) >= 2 * m or (e - 1) ** 2 >= 2 * m or 3 * e >= m
    return dict(m=m, B=tuple(B), h=h, e=e, a=a, b=b, W=W, sigma=sigma, Phi=len(Phs), delta=len(Dset), E3f=E3f, shc=shadow_c, known=known)
recs = []
if sys.argv[1] == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5])
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k):
            if gcd(m, *B) == 1:
                r = run(m, B)
                if r: recs.append(r)
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    for _ in range(N):
        m = random.randint(mlo, mhi); B = tuple(sorted(random.sample(range(1, m), k)))
        if gcd(m, *B) == 1:
            r = run(m, B)
            if r: recs.append(r)
U = [r for r in recs if r["Phi"] > 0]
print(sys.argv[1:], "S:", len(recs), "with P_hi > 0:", len(U))
for kk in (1, 2):
    mn = min(U, key=lambda r: r["sigma"] - kk * r["a"] * r["Phi"]); print(f"  min sigma - {kk}*a*P_hi:", mn["sigma"] - kk * mn["a"] * mn["Phi"], mn)
mn = min(U, key=lambda r: r["sigma"] - (2 * r["a"] + 1) * r["Phi"]); print("  min sigma - (2a+1)P_hi:", mn["sigma"] - (2 * mn["a"] + 1) * mn["Phi"], mn)
mn = min(U, key=lambda r: r["shc"] - (1 + r["a"]) * r["Phi"] / 2); print("  min shadow_c - (1+a)P_hi/2:", mn["shc"] - (1 + mn["a"]) * mn["Phi"] / 2, mn)
