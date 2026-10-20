r"""P18 depth four (lead, 2026-10-20).  Relative TCM: for Q c 2A \ A,  3|(3A\2A) \ (Q+A)| <= (e-1)(|2A| - |Q|)
(Eliahou's condensed Macaulay for k[C]/(x0, (2,q): q in Q)). Hence 3|Q+A| >= (e+2)|Q| - E3f.
With Q = Dset u Pset_hi (wasted carried pairs), W >= V := E1 + T + 2 delta - P_hi + 3 delta_hi + 3 extra,
T = e*y0 - 3N4 - h, extra = tau + omega - |Q+A| >= 0.  Checks relative TCM (also for random Q), reports min V by class.
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
from math import gcd
def run(m, B, rng):
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
    h = c - 3 * m; g = sum(x // m for x in w); W = e * (c - g) - c
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    E1 = e * (e + 1) - 2 * len(X2); E3f = (e - 1) * len(X2) - 3 * len(X3 - X2)
    def rel(Q):
        QA = set(q + a for q in Q for a in A)
        return 3 * len((X3 - X2) - QA) <= (e - 1) * (len(X2) - len(Q))
    pool = sorted(X2 - set(A)); Qr = [q for q in pool if rng.random() < 0.5]
    relok = rel(Qr)
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    tau = sum(1 for s in X3 if s >= m + h); omega = sum(1 for s in X3 if m <= s < m + h and (s - m) in X4)
    Dset = [s for s in X2 if m <= s < m + h and (s - m) in X3]; Phs = [s for s in X2 if m + h <= s < 2 * m]
    dhi = sum(1 for s in Phs if (s - m) in X3); delta = len(Dset); Phi = len(Phs)
    Q = Dset + Phs; relok = relok and rel(Q)
    QA = set(q + a for q in Q for a in A); extra = tau + omega - len(QA)
    T = e * y0 - 3 * N4 - h
    V = E1 + T + 2 * delta - Phi + 3 * dhi + 3 * extra
    a = sum(1 for x in B if x < h); hp = (h + 1) // 2
    cl = (sum(1 for x in B if x < hp), a - sum(1 for x in B if x < hp), e - 1 - a)
    known = h <= e or e * (e + 1) >= 2 * m or (e - 1) ** 2 >= 2 * m or 3 * e >= m
    return dict(m=m, B=tuple(B), h=h, e=e, W=W, V=V, relok=relok, bound=(W >= V), T=T, Phi=Phi, delta=delta, dhi=dhi, extra=extra, E1=E1, E3f=E3f, cl=cl, known=known)
rng = random.Random(1)
recs = []
if sys.argv[1] == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5])
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k):
            if gcd(m, *B) == 1:
                r = run(m, B, rng)
                if r: recs.append(r)
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    for _ in range(N):
        m = random.randint(mlo, mhi); B = tuple(sorted(random.sample(range(1, m), k)))
        if gcd(m, *B) == 1:
            r = run(m, B, rng)
            if r: recs.append(r)
print(sys.argv[1:], "S:", len(recs), "relTCM fails:", sum(1 for r in recs if not r["relok"]), "W>=V fails:", sum(1 for r in recs if not r["bound"]))
neg = [r for r in recs if r["V"] < 0]; negu = [r for r in neg if not r["known"]]
keys = ("m", "B", "h", "e", "W", "V", "T", "Phi", "delta", "dhi", "extra", "E1", "E3f", "cl")
mn = min(recs, key=lambda r: r["V"]); print("  V<0:", len(neg), "uncovered:", len(negu), "min V", {x: mn[x] for x in keys})
if negu: mu = min(negu, key=lambda r: r["V"]); print("  min V uncovered", {x: mu[x] for x in keys})
by = {}
for r in neg: by[r["cl"][1] > 0, r["cl"][2] > 0, r["cl"][0] > 0] = by.get((r["cl"][1] > 0, r["cl"][2] > 0, r["cl"][0] > 0), 0) + 1
print("  V<0 by (core>0, high>0, small>0):", by)
