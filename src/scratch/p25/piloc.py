r"""Local high-pair window bound (lead, 2026-10-20). For high u in B (u >= h):
 pi(u) = #{u' in B_h : u + u' in [m+h, m + 3h'), (u+u'-m) notin 3A} (window cells covered by high pairs through u).
Claim LOC: pi(u) <= y0 = |3A n [0,h)| for every u.  Also report max of sum_u pi(u) - b*y0 and of 2*pi' - b*y0.
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
    h = c - 3 * m; hp = (h + 1) // 2
    Bh = [x for x in B if x >= h]
    if not Bh: return None
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A)
    y0 = sum(1 for s in X3 if s < h)
    cells = set()
    piu = {}
    for u in Bh:
        cnt = 0
        for u2 in Bh:
            s = u + u2
            if m + h <= s < m + 3 * hp and (s - m) not in X3: cnt += 1; cells.add(s - m)
        piu[u] = cnt
    mx = max(piu.values())
    return dict(m=m, B=tuple(B), h=h, e=e, y0=y0, b=len(Bh), maxpi=mx, loc=mx - y0, sumpi=sum(piu.values()) - len(Bh) * y0, cells=2 * len(cells) - len(Bh) * y0)
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
print(sys.argv[1:], "S with high elements:", len(recs))
for key in ("loc", "sumpi", "cells"):
    mx = max(recs, key=lambda r: r[key]); print(f"  max {key}: {mx[key]} (count > 0: {sum(1 for r in recs if r[key] > 0)})", mx)
