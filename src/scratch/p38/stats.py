# stats: per residual S (from Q5DUMP files) compute candidate counts for D6 (Delta3 >= 6h), and report min ratios.
#   Top3   = #{v in L3 : sigma(v) > Lambda = max sigma}        (necessarily missing)
#   Wrap3  = #{v in L3 : sigma(v) - m in T}                    (U-tile members among them = NE3 reps)
#   PrimM3 = #{v in Miss3 : every lower neighbour in D}        (weight 3)
#   WrapM3 = #{v in Miss3 : sigma(v) >= sigma(rep of class) + m}
import sys
from itertools import combinations_with_replacement as cwr
from fractions import Fraction as F
def analyse(m, A):
    d = len(A); e = d + 1
    mons = {k: [tuple(sum(1 for i in c if i == q) for q in range(d)) for c in cwr(range(d), k)] for k in range(4)}
    sig = lambda v: sum(v[i] * A[i] for i in range(d))
    best = {}
    for k in range(4):
        for v in mons[k]:
            s = sig(v); c = s % m; key = (k * m + s, -k, tuple(-x for x in v))
            if c not in best or key < best[c][0]: best[c] = (key, v)
    assert len(best) == m
    X = {c: best[c][1] for c in best}; D = set(X.values())
    sg = {c: sig(X[c]) for c in X}
    # T Apery set w.r.t. m (Dijkstra over residues)
    tau = [None] * m; tau[0] = 0; done = [False] * m
    import heapq
    pq = [(0, 0)]
    while pq:
        t, c = heapq.heappop(pq)
        if done[c]: continue
        done[c] = True
        for a in A:
            u = t + a; cc = u % m
            if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
    inT = lambda x: x >= 0 and x >= tau[x % m]
    NE = {c for c in X if sg[c] > tau[c]}
    ne3 = sum(1 for c in NE if sum(X[c]) == 3); ne2 = len(NE) - ne3; h = len(NE)
    D3 = 3 * (e - 1) * m - e * sum(sum(X[c]) for c in X)
    Lam = max(sg.values())
    miss2 = [v for v in mons[2] if v not in D]; miss3 = [v for v in mons[3] if v not in D]
    assert D3 == 3 * len(miss3) - (e - 3) * len(miss2)
    low = lambda v: [tuple(v[q] - (q == i) for q in range(d)) for i in range(d) if v[i]]
    top3 = sum(1 for v in mons[3] if sig(v) > Lam)
    wrap3 = sum(1 for v in mons[3] if inT(sig(v) - m))
    prim = sum(1 for v in miss3 if all(u in D for u in low(v)))
    wrapm = sum(1 for v in miss3 if sig(v) >= sg[sig(v) % m] + m)
    shad = len(miss3) - prim
    return dict(m=m, e=e, h=h, ne2=ne2, ne3=ne3, D3=D3, M2=len(miss2), M3=len(miss3), top3=top3, wrap3=wrap3, prim=prim, wrapm=wrapm, shad=shad)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            m = int(t[1]); A = list(map(int, t[15:]))
            r = analyse(m, A); r['A'] = A; rows.append(r)
def rep(name, val):
    w = min(rows, key=lambda r: val(r)); print(f"  min {name} = {float(val(w)):.3f} at m={w['m']} A={w['A']} {dict((k, w[k]) for k in ('h','ne2','ne3','D3','M2','M3','top3','wrap3','prim','wrapm'))}")
print(f"{sys.argv[1]}: {len(rows)} S, e = {rows[0]['e']}")
rep('top3/h', lambda r: F(r['top3'], r['h']))
rep('(wrap3-ne3)/h', lambda r: F(r['wrap3'] - r['ne3'], r['h']))
rep('wrapm/h', lambda r: F(r['wrapm'], r['h']))
rep('prim/h', lambda r: F(r['prim'], r['h']))
rep('(M3-(e-3)M2/3)/h', lambda r: F(3 * r['M3'] - (r['e'] - 3) * r['M2'], 3 * r['h']))
rep('(M3-M2)/h', lambda r: F(r['M3'] - r['M2'], r['h']))
rep('(3prim+4M2)/(6h)', lambda r: F(3 * r['prim'] + 4 * r['M2'], 6 * r['h']))
rep('(3prim+3shad-(e-3)M2)/(6h) [=D3/6h]', lambda r: F(3 * r['prim'] + 3 * r['shad'] - (r['e'] - 3) * r['M2'], 6 * r['h']))
rep('wrapm-h', lambda r: r['wrapm'] - r['h'])
import collections
c = collections.Counter(min(r['wrapm'] - r['h'], 10) for r in rows); print('  hist wrapm-h (capped 10):', sorted(c.items()))
c = collections.Counter(min(3 * r['prim'] + 4 * r['M2'] - 6 * r['h'], 20) for r in rows); print('  hist 3prim+4M2-6h (capped 20):', sorted(c.items())[:12])
