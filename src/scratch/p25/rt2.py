r"""RT2 identity for P18 depth four (lead, 2026-10-20).  Q = 2A n [m, 2m) (all carried pairs), L = m + h.
RT2 (condensed Macaulay on k[C]/(x0, Q, I_{>=L})): 3(|(3A\2A)_{<L}| - |K|) <= (e-1)(e + n2), slack MS >= 0, where
  n2 = |(2A\A) n [0,m)|, K = ((Q + A) \ 2A) n [0, L).
Exact: W = R0 + MS,  R0 = E1 + (e-2)P_lo + (e-1)y0 - 4N4 - e*delta - 3|K| - |K'| + 4*omega - P_hi + 3*delta_hi,
  K' = (3A\2A) n [m, m+h).  Checks the identity, RT2, and reports min R0 (and among uncovered S), by a=0 / a>0.
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
    c = max(w) - m + 1
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m; g = sum(x // m for x in w); W = e * (c - g) - c; L = m + h
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    E1 = e * (e + 1) - 2 * len(X2)
    n2 = sum(1 for s in X2 if s < m and s not in set(A))
    Q = [s for s in X2 if s >= m]
    K = set(q + a for q in Q for a in A if q + a < L) - X2
    new3 = sum(1 for s in X3 - X2 if s < L)
    MS = (e - 1) * (e + n2) - 3 * (new3 - len(K))
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    Plo = sum(1 for s in X2 if m <= s < L); Phs = [s for s in X2 if L <= s < 2 * m]; Phi = len(Phs)
    delta = sum(1 for s in X2 if m <= s < L and (s - m) in X3); dhi = sum(1 for s in Phs if (s - m) in X3)
    Kp = sum(1 for s in X3 - X2 if m <= s < L)
    omega = sum(1 for s in X3 if m <= s < L and (s - m) in X4)
    R0 = E1 + (e - 2) * Plo + (e - 1) * y0 - 4 * N4 - e * delta - 3 * len(K) - Kp + 4 * omega - Phi + 3 * dhi
    a = sum(1 for x in B if x < h)
    known = h <= e or e * (e + 1) >= 2 * m or (e - 1) ** 2 >= 2 * m or 3 * e >= m
    return dict(m=m, B=tuple(B), h=h, e=e, a=a, W=W, R0=R0, MS=MS, ok=(W == R0 + MS), K=len(K), Kp=Kp, Plo=Plo, Phi=Phi, E1=E1, y0=y0, known=known)
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
print(sys.argv[1:], "S:", len(recs), "identity fails:", sum(1 for r in recs if not r["ok"]), "RT2 fails (MS<0):", sum(1 for r in recs if r["MS"] < 0))
for lab, sub in (("a=0", [r for r in recs if r["a"] == 0]), ("a>0", [r for r in recs if r["a"] > 0]), ("uncovered", [r for r in recs if not r["known"]])):
    if sub:
        mn = min(sub, key=lambda r: r["R0"]); print(f"  {lab}: n={len(sub)} R0<0: {sum(1 for r in sub if r['R0'] < 0)} min R0 {mn['R0']}", {x: mn[x] for x in ("m", "B", "h", "e", "a", "W", "MS", "K", "Kp", "Plo", "Phi", "E1", "y0")})
