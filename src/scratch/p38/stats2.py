# stats2: T-ideal quantities for D6.  J = T-nonstandard monomials (sigma(v) - m in T, or T-Apery value but not the
# T-rep).  D6 <=> |J3| >= 3 b3 + (e/3 - 1)(|J2| - b2) + 2 b2   (b2 = |NE2|, b3 = |NE3|).
# Sufficient (crude shadow): T3: 3|G3| + 4(|J2| - b2) >= 9 b3, G3 = minimal cubic generators of J.
import sys, heapq, collections
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
    X = {c: best[c][1] for c in best}; sg = {c: sig(X[c]) for c in X}
    T = {0: (0, 0, tuple([0] * d))}; pq = [(0, 0, tuple([0] * d), 0)]; done = set()
    while pq:
        val, ln, negv, c = heapq.heappop(pq)
        if c in done: continue
        done.add(c); v = tuple(-x for x in negv)
        for i in range(d):
            w = list(v); w[i] += 1; w = tuple(w); nv = val + A[i]; nc = nv % m; key = (nv, ln + 1, tuple(-x for x in w))
            if nc not in done and (nc not in T or key < T[nc]): T[nc] = key; heapq.heappush(pq, (nv, ln + 1, tuple(-x for x in w), nc))
    tau = {c: T[c][0] for c in T}; Trep = {c: tuple(-x for x in T[c][2]) for c in T}
    DT = set(Trep.values())
    NE = [c for c in X if sg[c] > tau[c]]; b3 = sum(1 for c in NE if sum(X[c]) == 3); b2 = len(NE) - b3
    J2 = [v for v in mons[2] if v not in DT]; J3 = [v for v in mons[3] if v not in DT]
    low = lambda v: [tuple(v[q] - (q == i) for q in range(d)) for i in range(d) if v[i]]
    G3 = [v for v in J3 if all(u in DT for u in low(v))]
    D = set(X.values()); M2 = sum(1 for v in mons[2] if v not in D); M3 = sum(1 for v in mons[3] if v not in D)
    D3 = 3 * M3 - (e - 3) * M2
    assert D3 == 3 * (e - 1) * m - e * sum(sum(X[c]) for c in X)
    assert len(J2) == M2 + b2 and len(J3) == M3 + b3
    pi0 = sum(1 for c in NE if sum(X[c]) == 3 and all(u in DT for u in low(X[c])))
    return dict(m=m, e=e, b2=b2, b3=b3, h=b2 + b3, D3=D3, J2=len(J2), J3=len(J3), G3=len(G3), pi0=pi0)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:]))); r['A'] = list(map(int, t[15:])); rows.append(r)
keys = ('b2', 'b3', 'D3', 'J2', 'J3', 'G3', 'pi0')
def rep(name, val, filt=lambda r: True):
    R = [r for r in rows if filt(r)]
    if not R: print('  (none)', name); return
    w = min(R, key=val); print(f"  min {name} = {float(val(w)):.3f} at m={w['m']} A={w['A']} {dict((k, w[k]) for k in keys)}")
print(f"{sys.argv[1]}: {len(rows)} S, e = {rows[0]['e']}")
has3 = lambda r: r['b3'] > 0
rep('T3: (3G3 + 4(J2-b2))/(9 b3)', lambda r: F(3 * r['G3'] + 4 * (r['J2'] - r['b2']), 9 * r['b3']), has3)
rep('G3/b3', lambda r: F(r['G3'], r['b3']), has3)
rep('(G3 - pi0)/b3', lambda r: F(r['G3'] - r['pi0'], r['b3']), has3)
rep('(J3 - b3)/b3', lambda r: F(r['J3'] - r['b3'], r['b3']), has3)
rep('D6 slack D3-6h', lambda r: r['D3'] - 6 * r['h'])
c = collections.Counter(min(3 * r['G3'] + 4 * (r['J2'] - r['b2']) - 9 * r['b3'], 30) for r in rows if has3(r)); print('  hist T3 slack (capped 30):', sorted(c.items())[:15])
