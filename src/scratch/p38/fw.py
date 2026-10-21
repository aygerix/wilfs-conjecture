# fw: D6 <=> F + Wv >= 2h + (e/3) M2, where F = C(e+2,3) - |L3| (monomial coincidences: monomials of degree <= 3
# sharing a value), Wv = |L3| - m (distinct values of <=3-sums that are not class minima), L3 = 3A' as an integer set.
import sys, heapq, collections
from itertools import combinations_with_replacement as cwr
from fractions import Fraction as F
from math import comb
def analyse(m, A):
    d = len(A); e = d + 1
    vals = collections.Counter(); minv = {}; lev = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); vals[s] += 1
    L3 = set(vals)
    for s in sorted(L3):
        if s % m not in minv: minv[s % m] = s
    assert len(minv) == m
    tau = [None] * m; tau[0] = 0; pq = [(0, 0)]; done = [False] * m
    while pq:
        t, c = heapq.heappop(pq)
        if done[c]: continue
        done[c] = True
        for a in A:
            u = t + a; cc = u % m
            if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
    h = sum(1 for c in range(m) if minv[c] > tau[c])
    Fc = comb(e + 2, 3) - len(L3); Wv = len(L3) - m
    # M2 = level-2 monomials not in the U-tile
    best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            v = tuple(sum(1 for i in c if i == q) for q in range(d)); s = sum(A[i] for i in c); cl = s % m
            key = (k * m + s, -k, tuple(-x for x in v))
            if cl not in best or key < best[cl][0]: best[cl] = (key, v)
    D = set(b[1] for b in best.values())
    M2 = sum(1 for c in cwr(range(d), 2) if tuple(sum(1 for i in c if i == q) for q in range(d)) not in D)
    D3 = 3 * (e - 1) * m - e * sum(sum(b[1]) for b in best.values())
    assert 3 * D3 == 9 * (Fc + Wv) - 3 * e * M2, (D3, Fc, Wv, M2)
    return dict(m=m, e=e, h=h, F=Fc, Wv=Wv, M2=M2, D3=D3)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:]))); r['A'] = list(map(int, t[15:])); rows.append(r)
print(f"{sys.argv[1]}: {len(rows)} S, e = {rows[0]['e']}")
def rep(name, val):
    w = min(rows, key=val); print(f"  min {name} = {float(val(w)):.3f} at m={w['m']} A={w['A']} h={w['h']} F={w['F']} Wv={w['Wv']} M2={w['M2']} D3={w['D3']}")
rep('Wv - h', lambda r: r['Wv'] - r['h'])
rep('Wv/h', lambda r: F(r['Wv'], r['h']))
rep('(F - (e/3)M2)/h', lambda r: F(3 * r['F'] - r['e'] * r['M2'], 3 * r['h']))
rep('F/h', lambda r: F(r['F'], r['h']))
rep('(F + Wv - (e/3)M2)/(2h) [D6 iff >= 1]', lambda r: F(3 * (r['F'] + r['Wv']) - r['e'] * r['M2'], 6 * r['h']))
