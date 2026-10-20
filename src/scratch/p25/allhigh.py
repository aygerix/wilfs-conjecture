r"""P18 depth four with a = 0 (all B >= h) and h > e (lead, 2026-10-20): which known criterion covers them?
Reports counts and min of e(e+1) - 2m, (e-1)^2 - 2m, 3e - m, and max h - e, max m/e.  usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
from math import gcd
def run(m, B):
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
    h = c - 3 * m; e = len(B) + 1
    if min(B) < h or h <= e: return None
    g = sum(x // m for x in w)
    return dict(m=m, B=tuple(B), h=h, e=e, W=e * (c - g) - c, yz=e * (e + 1) - 2 * m, dkm=(e - 1) ** 2 - 2 * m, el=3 * e - m)
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
        m = random.randint(mlo, mhi); lo = random.randint(2, m // 2)
        if m - lo <= k: continue
        B = tuple(sorted(random.sample(range(lo, m), k)))
        if gcd(m, *B) == 1:
            r = run(m, B)
            if r: recs.append(r)
print(sys.argv[1:], "a=0, h>e S:", len(recs))
if recs:
    for key in ("yz", "dkm", "el"):
        mn = min(recs, key=lambda r: r[key]); print(f"  min {key}: {mn[key]}", mn)
    print("  uncovered:", sum(1 for r in recs if r["yz"] < 0 and r["dkm"] < 0 and r["el"] < 0))
    mx = max(recs, key=lambda r: r["h"] - r["e"]); print("  max h-e:", mx["h"] - mx["e"], mx)
