r"""All-A P18 depth four (lead, 2026-10-20): how big can the window 3-sums t3w = |(3A\2A) n [h,3h')| be relative to
h2 = |2A_<h| - e and h3 = |3A_<h| - |2A_<h|?  Reports max of ratio 2 t3w / ((e+2)h2 + e h3) and the worst examples;
also max of e'' = |W1 n (m+4A_<h) \ 3A| and N4.  usage: exh k mlo mhi | rnd k mlo mhi N seed"""
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
    if max(B) >= h: return None
    hp = (h + 1) // 2
    if min(B) >= hp: return None
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    x2h = sum(1 for s in X2 if s < h); y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    W1 = range(h, 3 * hp); t3w = sum(1 for v in W1 if v in X3 and v not in X2)
    A4h = set(s for s in X4 if s < h); epp = sum(1 for v in W1 if v >= m and (v - m) in A4h and v not in X3)
    h2 = x2h - e; h3 = y0 - x2h; den = (e + 2) * h2 + e * h3
    return dict(m=m, B=tuple(B), h=h, e=e, t3w=t3w, h2=h2, h3=h3, N4=N4, epp=epp, ratio=(2 * t3w / den if den else (0 if t3w == 0 else 99)),
                Z=den + e + 3 * (h % 2) - 2 * t3w - 3 * N4 - 2 * epp)
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
        m = random.randint(mlo, mhi); h0 = random.randint(max(4, m // 2), m)
        B = tuple(sorted(random.sample(range(1, h0), min(k, h0 - 1))))
        if len(B) == k and gcd(m, *B) == 1:
            r = run(m, B)
            if r: recs.append(r)
print(sys.argv[1:], "noncore all-A S:", len(recs), " Z<0:", sum(1 for r in recs if r["Z"] < 0))
for r in sorted(recs, key=lambda r: -r["ratio"])[:4]: print("  ratio", round(r["ratio"], 3), r)
print("  max epp", max(r["epp"] for r in recs), " max N4", max(r["N4"] for r in recs), " max t3w", max(r["t3w"] for r in recs))
for r in sorted(recs, key=lambda r: r["Z"])[:3]: print("  minZ", r)
