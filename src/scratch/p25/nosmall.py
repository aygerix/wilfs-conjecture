r"""P18 depth four, no-small regime B c [h', m) (h' = ceil(h/2)), lead 2026-10-20.  Checks the exact identity
  W = E1 + E3f + e(1+a) - h - e*delta + 3*kappa_c + 3*tau' + 3*delta_hi - (e+3)*P_hi,
a = |B n [h', h)|, delta = |2A n [m,m+h) n (m+A)|, kappa_c = |3A n [m,m+h) n (m+A)|, tau' = |3A n [m+h, oo)|,
P_hi = |2A n [m+h, 2m)|, delta_hi = |{s in 2A n [m+h,2m): s-m in 3A}|; reports min W - (e-2) and min W/e by class (a, b).
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
from math import gcd
def c2(h): return (h + 1) // 2
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
    if min(B) < c2(h): return None
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A)
    E1 = e * (e + 1) - 2 * len(X2); E3f = (e + 2) * len(X2) - 3 * len(X3)
    a = sum(1 for x in B if x < h); Am = set(x + m for x in A)
    delta = sum(1 for s in X2 if m <= s < m + h and s in Am)
    kc = sum(1 for s in X3 if m <= s < m + h and s in Am)
    taup = sum(1 for s in X3 if s >= m + h)
    Phi = sum(1 for s in X2 if m + h <= s < 2 * m); dhi = sum(1 for s in X2 if m + h <= s < 2 * m and (s - m) in X3)
    rhs = E1 + E3f + e * (1 + a) - h - e * delta + 3 * kc + 3 * taup + 3 * dhi - (e + 3) * Phi
    return dict(m=m, B=tuple(B), h=h, e=e, a=a, W=W, ok=(rhs == W), E1=E1, E3f=E3f, delta=delta, kc=kc, taup=taup, Phi=Phi, dhi=dhi)
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
        m = random.randint(mlo, mhi); h0 = random.randint(4, m)
        lo = c2(h0)
        if m - lo <= k: continue
        B = tuple(sorted(random.sample(range(lo, m), k)))
        if gcd(m, *B) == 1:
            r = run(m, B)
            if r: recs.append(r)
print(sys.argv[1:], "no-small S:", len(recs), "identity fails:", sum(1 for r in recs if not r["ok"]))
cls = {}
for r in recs:
    key = ("core" if r["a"] == r["e"] - 1 else ("allhigh" if r["a"] == 0 else "mixed"))
    if key not in cls or r["W"] - (r["e"] - 2) < cls[key]["W"] - (cls[key]["e"] - 2): cls[key] = r
    cls[key + "_n"] = cls.get(key + "_n", 0) + 1 if isinstance(cls.get(key + "_n", 0), int) else 1
for kk, v in cls.items(): print("  ", kk, v)
print("  W < e-2:", sum(1 for r in recs if r["W"] < r["e"] - 2), " W < 0:", sum(1 for r in recs if r["W"] < 0))
