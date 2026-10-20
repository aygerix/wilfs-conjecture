r"""Depth four: W = D1 + D2 with D1 = e*l2 - 3m (l2 = |S n [0,3m)|) and D2 = e*x - h (x = |S n [3m, c)|).
Is D2 >= 0 (e*|S n [3m,c)| >= c - 3m) always?  P18 exhaustive and general S via generator lists. (lead, 2026-10-20)"""
import sys, itertools, heapq
from math import gcd
def apery(m, gens):
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for n in gens:
            v = d0 + n; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    return w
def pieces(m, B):
    w = apery(m, [m + b for b in B])
    if any(x is None for x in w): return None
    M = max(w); c = M - m + 1
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m; e = len(B) + 1
    l2 = sum(max(0, (3 * m - x + m - 1) // m) for x in w)   # #{x + jm < 3m}
    x_ = sum(1 for r in range(m) if w[r] <= 3 * m + r and r < h)
    D1 = e * l2 - 3 * m; D2 = e * x_ - h
    return D1, D2, h, e, x_, l2
k = int(sys.argv[1]); mlo, mhi = int(sys.argv[2]), int(sys.argv[3])
cnt = 0; neg2 = 0; mn2 = None; mn1 = None
for m in range(mlo, mhi + 1):
    for B in itertools.combinations(range(1, m), k):
        g = m
        for b in B: g = gcd(g, b)
        if g != 1: continue
        r = pieces(m, B)
        if not r: continue
        cnt += 1; D1, D2, h, e, x_, l2 = r
        if D2 < 0: neg2 += 1
        if mn2 is None or D2 < mn2[0]: mn2 = (D2, D1, m, B, h, x_)
        if mn1 is None or D1 < mn1[0]: mn1 = (D1, D2, m, B, h, x_)
print("k", k, "S", cnt, "D2<0:", neg2, "min D2", mn2, "min D1", mn1)
