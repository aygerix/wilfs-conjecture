r"""P18 depth four (lead, 2026-10-20). Exact form (star):
  W = E1 + E3f + e*y0 - 3N4 - h + 3(tau + omega + delta_hi) - e*delta - (e+3)*P_hi.
Q = Pset_hi u Dset (carried pairs that cost), Q + A c waste (tau u omega).  Split W = R + G with
  G = 3|Q + A| - e|Q| - 3 P_hi,   R = E1 + E3f + e*y0 - 3N4 - h + 3(tau + omega + delta_hi - |Q+A|).
Reports min G, min R, and min of T = e*y0 - 3N4 - h (top-band part), over uncovered S, by class.
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
    h = c - 3 * m; g = sum(x // m for x in w); W = e * (c - g) - c
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    E1 = e * (e + 1) - 2 * len(X2); E3f = (e + 2) * len(X2) - 3 * len(X3)
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    tau = sum(1 for s in X3 if s >= m + h); omega = sum(1 for s in X3 if m <= s < m + h and (s - m) in X4)
    Dset = [s for s in X2 if m <= s < m + h and (s - m) in X3]; Phs = [s for s in X2 if m + h <= s < 2 * m]
    dhi = sum(1 for s in Phs if (s - m) in X3); delta = len(Dset); Phi = len(Phs)
    lhs = E1 + E3f + e * y0 - 3 * N4 - h + 3 * (tau + omega + dhi) - e * delta - (e + 3) * Phi
    Q = Dset + Phs; QA = set(q + a for q in Q for a in A)
    G = 3 * len(QA) - e * len(Q) - 3 * Phi
    R = W - G
    a = sum(1 for x in B if x < h); hp = (h + 1) // 2
    cl = (sum(1 for x in B if x < hp), a - sum(1 for x in B if x < hp), e - 1 - a)
    known = h <= e or e * (e + 1) >= 2 * m or (e - 1) ** 2 >= 2 * m or 3 * e >= m
    return dict(m=m, B=tuple(B), h=h, e=e, W=W, ok=(lhs == W), G=G, R=R, T=e * y0 - 3 * N4 - h, Q=len(Q), Phi=Phi, delta=delta, cl=cl, known=known, E1=E1, E3f=E3f)
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
print(sys.argv[1:], "S:", len(recs), "identity fails:", sum(1 for r in recs if not r["ok"]))
for name in ("G", "R", "T"):
    neg = [r for r in recs if r[name] < 0]; negu = [r for r in neg if not r["known"]]
    mn = min(recs, key=lambda r: r[name])
    print(f"  {name}: neg {len(neg)} (uncovered {len(negu)}), min {mn[name]}", {x: mn[x] for x in ("m", "B", "h", "e", "W", "G", "R", "T", "Q", "Phi", "delta", "cl", "E1", "E3f")})
    if negu:
        mu = min(negu, key=lambda r: r[name]); print(f"     min among uncovered {mu[name]}", {x: mu[x] for x in ("m", "B", "h", "e", "W", "G", "R", "T", "Q", "Phi", "delta", "cl", "E1", "E3f")})
