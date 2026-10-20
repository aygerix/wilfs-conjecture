r"""P18 depth four (lead, 2026-10-20).  W = V + sigma.  Split test:
 (I)  SIG1: sigma >= P_hi ; SIG: sigma >= (2a+1) P_hi
 (II) TBE: E1 + T + 2 delta + 3 delta_hi + 3 extra >= 0 ;  T = e*y0 - 3N4 - h ; also T >= 0 and T + E1 >= 0.
(I) and (II) together give W >= 0.  usage: exh k mlo mhi | rnd k mlo mhi N seed"""
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
    a = sum(1 for x in B if x < h)
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    E1 = e * (e + 1) - 2 * len(X2); E3f = (e + 2) * len(X2) - 3 * len(X3)
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    tau = sum(1 for s in X3 if s >= m + h); omega = sum(1 for s in X3 if m <= s < m + h and (s - m) in X4)
    Dset = [s for s in X2 if m <= s < m + h and (s - m) in X3]; Phs = [s for s in X2 if m + h <= s < 2 * m]
    dhi = sum(1 for s in Phs if (s - m) in X3); delta = len(Dset); Phi = len(Phs)
    Q = Dset + Phs; QA = set(q + x for q in Q for x in A); extra = tau + omega - len(QA)
    sigma = 3 * len(QA) - (e + 2) * len(Q) + E3f
    T = e * y0 - 3 * N4 - h
    TBE = E1 + T + 2 * delta + 3 * dhi + 3 * extra
    known = h <= e or e * (e + 1) >= 2 * m or (e - 1) ** 2 >= 2 * m or 3 * e >= m
    return dict(m=m, B=tuple(B), h=h, e=e, a=a, W=W, sigma=sigma, Phi=Phi, T=T, E1=E1, TBE=TBE, delta=delta, dhi=dhi, extra=extra, known=known)
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
print(sys.argv[1:], "S:", len(recs))
tests = {"SIG1 sigma-P_hi": lambda r: r["sigma"] - r["Phi"], "SIG sigma-(2a+1)P_hi": lambda r: r["sigma"] - (2 * r["a"] + 1) * r["Phi"],
         "TBE": lambda r: r["TBE"], "T": lambda r: r["T"], "T+E1": lambda r: r["T"] + r["E1"]}
for name, f in tests.items():
    neg = [r for r in recs if f(r) < 0]; mn = min(recs, key=f)
    print(f"  {name}: neg {len(neg)} (uncovered {sum(1 for r in neg if not r['known'])}), min {f(mn)}", {x: mn[x] for x in ("m", "B", "h", "e", "a", "W", "sigma", "Phi", "T", "E1", "TBE", "known")})
