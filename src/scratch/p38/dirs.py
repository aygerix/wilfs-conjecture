# dirs: per-direction split Delta3 = sum_i D3_i, D3_i = 3m - sum_s (h_s + (x_s)_i) = sum over i-columns (t_i+1)(3-|t|).
# Test DIR_i: D3_i >= h for directions i with a_i != mu (and report the mu direction separately).
import sys, collections
from itertools import combinations_with_replacement as cwr
from fractions import Fraction as F
import heapq
def analyse(m, A):
    d = len(A); e = d + 1
    best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            v = tuple(sum(1 for i in c if i == q) for q in range(d)); s = sum(A[i] for i in c); cl = s % m
            key = (k * m + s, -k, tuple(-x for x in v))
            if cl not in best or key < best[cl][0]: best[cl] = (key, v)
    X = {c: best[c][1] for c in best}
    tau = [None] * m; tau[0] = 0; pq = [(0, 0)]; done = [False] * m
    while pq:
        t, c = heapq.heappop(pq)
        if done[c]: continue
        done[c] = True
        for a in A:
            u = t + a; cc = u % m
            if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
    sg = {c: sum(X[c][i] * A[i] for i in range(d)) for c in X}
    h = sum(1 for c in X if sg[c] > tau[c]); H = sum(sum(X[c]) for c in X)
    Di = [3 * m - H - sum(X[c][i] for c in X) for i in range(d)]
    D3 = 3 * (e - 1) * m - e * H; assert sum(Di) == D3
    return dict(m=m, e=e, h=h, D3=D3, Di=Di)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:]))); r['A'] = list(map(int, t[15:])); rows.append(r)
e = rows[0]['e']; print(f"{sys.argv[1]}: {len(rows)} S, e = {e}")
w = min(rows, key=lambda r: F(min(r['Di'][1:]), r['h'])); print(f"  min_{{i>=2}} D3_i/h = {float(F(min(w['Di'][1:]), w['h'])):.3f} at m={w['m']} A={w['A']} h={w['h']} Di={w['Di']}")
w = min(rows, key=lambda r: F(r['Di'][0], r['h'])); print(f"  min D3_1/h (mu direction) = {float(F(w['Di'][0], w['h'])):.3f} at m={w['m']} A={w['A']} h={w['h']} Di={w['Di']}")
w = min(rows, key=lambda r: F(sum(r['Di'][1:]), (e - 2) * r['h'])); print(f"  min sum_{{i>=2}} D3_i/((e-2)h) = {float(F(sum(w['Di'][1:]), (e-2) * w['h'])):.3f} at m={w['m']} A={w['A']} h={w['h']} Di={w['Di']}")
fails = sum(1 for r in rows if min(r['Di'][1:]) < r['h']); print(f"  DIR (D3_i >= h for all i >= 2) failures: {fails}")
c = collections.Counter(min(F(min(r['Di'][1:]), r['h']), 3) for r in rows)
print('  quantiles of min_{i>=2} D3_i/h:', [float(x) for x in sorted(F(min(r['Di'][1:]), r['h']) for r in rows)[:8]])
