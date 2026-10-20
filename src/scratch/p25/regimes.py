r"""P18 depth four: where is Wilf tight? (lead, 2026-10-20). Classifies S = <m, m+B> (3m < c <= 4m, h = c - 3m) by
(s, k, b) = #B below h/2, #B in [h/2, h), #B >= h, restricted to S NOT covered by known criteria
(h <= e; e(e+1) >= 2m; (e-1)^2 >= 2m; 3e >= m), and reports per class: count, min W, min W/e, argmin.
Also checks the general exact identity W = E1 + E2 + E3f + b*y0 + 3tau + 4omega - U1 - e*delta - (e+3)P_hi + 3delta_hi.
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
    a = sum(1 for x in B if x < h); bb = e - 1 - a
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3); E2 = a * y0 - 4 * N4
    U1 = sum(1 for s in X3 if m <= s < m + h); tau = sum(1 for s in X3 if s >= m + h)
    omega = sum(1 for s in X3 if m <= s < m + h and (s - m) in X4)
    delta = sum(1 for s in X2 if m <= s < m + h and (s - m) in X3)
    Phi = sum(1 for s in X2 if m + h <= s < 2 * m); dhi = sum(1 for s in X2 if m + h <= s < 2 * m and (s - m) in X3)
    ok = W == E1 + E2 + E3f + bb * y0 + 3 * tau + 4 * omega - U1 - e * delta - (e + 3) * Phi + 3 * dhi
    hp = (h + 1) // 2
    cl = (sum(1 for x in B if x < hp), sum(1 for x in B if hp <= x < h), bb)
    known = h <= e or e * (e + 1) >= 2 * m or (e - 1) ** 2 >= 2 * m or 3 * e >= m
    return dict(m=m, B=tuple(B), h=h, e=e, W=W, ok=ok, cl=cl, known=known)
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
print(sys.argv[1:], "depth-four S:", len(recs), "identity fails:", sum(1 for r in recs if not r["ok"]), "uncovered:", sum(1 for r in recs if not r["known"]))
agg = {}
for r in recs:
    if r["known"]: continue
    s, kc, b = r["cl"]; key = ("s>0" if s else "s=0") + "," + ("k>0" if kc else "k=0") + "," + ("b>0" if b else "b=0")
    d = agg.setdefault(key, [0, None, None])
    d[0] += 1
    if d[1] is None or r["W"] < d[1]["W"]: d[1] = r
    if d[2] is None or r["W"] / r["e"] < d[2]["W"] / d[2]["e"]: d[2] = r
for key in sorted(agg):
    n, r1, r2 = agg[key]
    print(f"  {key}: n={n}  minW {r1['W']} (e={r1['e']}, m={r1['m']}, h={r1['h']}, B={r1['B']})  min W/e {r2['W']/r2['e']:.2f} (e={r2['e']}, m={r2['m']}, h={r2['h']}, cl={r2['cl']}, B={r2['B']})")
