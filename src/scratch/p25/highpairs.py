r"""No-small P18 depth four with high elements (lead, 2026-10-20). For each S: a, b, P_hi, pi1, beta1, e', delta_hi, E1,
coll_hh = C(b+1,2) - |2B_h| (high-high pair collisions), F0 = (a+1)(b+1) - P_hi - 2 pi1 - 2 beta1 - 2e' + 3[h odd], V, sigma.
Prints the S with smallest F0 and smallest V (uncovered only), and the min of F0 + 2 coll_hh.  usage: exh k mlo mhi | rnd ..."""
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
    h = c - 3 * m; hp = (h + 1) // 2
    if min(B) < hp: return None
    Bh = [x for x in B if x >= h]
    if not Bh: return None
    g = sum(x // m for x in w); W = e * (c - g) - c
    a = e - 1 - len(Bh); b = len(Bh)
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    E1 = e * (e + 1) - 2 * len(X2); E3f = (e + 2) * len(X2) - 3 * len(X3)
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    tau = sum(1 for s in X3 if s >= m + h); omega = sum(1 for s in X3 if m <= s < m + h and (s - m) in X4)
    Dset = [s for s in X2 if m <= s < m + h and (s - m) in X3]; Phs = [s for s in X2 if m + h <= s < 2 * m]
    dhi = sum(1 for s in Phs if (s - m) in X3); delta = len(Dset); Phi = len(Phs)
    Q = Dset + Phs; QA = set(q + x for q in Q for x in A)
    V = E1 + e * y0 - 3 * N4 - h + 2 * delta - Phi + 3 * dhi + 3 * (tau + omega - len(QA))
    sigma = 3 * len(QA) - (e + 2) * len(Q) + E3f
    W1 = set(range(h, 3 * hp))
    pi1 = len(set(s - m for s in Phs) & W1 - X2); beta1 = len(set(Bh) & W1); ep = len(set(x + m for x in A) & W1)
    hh = set(x + y for x in Bh for y in Bh); coll = b * (b + 1) // 2 - len(hh)
    F0 = (a + 1) * (b + 1) - Phi - 2 * pi1 - 2 * beta1 - 2 * ep + 3 * (h % 2)
    known = h <= e or e * (e + 1) >= 2 * m or (e - 1) ** 2 >= 2 * m or 3 * e >= m
    return dict(m=m, B=tuple(B), h=h, e=e, a=a, b=b, W=W, V=V, sigma=sigma, F0=F0, Phi=Phi, pi1=pi1, beta1=beta1, ep=ep, dhi=dhi, E1=E1, coll=coll, delta=delta, known=known, ok=(W == V + sigma))
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
        lo = (h0 + 1) // 2
        if m - lo <= k: continue
        B = tuple(sorted(random.sample(range(lo, m), k)))
        if gcd(m, *B) == 1:
            r = run(m, B)
            if r: recs.append(r)
U = [r for r in recs if not r["known"]]
print(sys.argv[1:], "no-small with high:", len(recs), "uncovered:", len(U), "W=V+sigma fails:", sum(1 for r in recs if not r["ok"]))
keys = ("m", "B", "h", "e", "a", "b", "W", "V", "sigma", "F0", "Phi", "pi1", "beta1", "ep", "dhi", "E1", "coll", "delta")
for lab, key in (("F0", lambda r: r["F0"]), ("V", lambda r: r["V"]), ("F0+2coll", lambda r: r["F0"] + 2 * r["coll"])):
    if U:
        mn = min(U, key=key); print(f"  uncovered min {lab} = {key(mn)}:", {x: mn[x] for x in keys})
    print(f"  all: {lab} < 0 count {sum(1 for r in recs if key(r) < 0)}; uncovered {sum(1 for r in U if key(r) < 0)}")
