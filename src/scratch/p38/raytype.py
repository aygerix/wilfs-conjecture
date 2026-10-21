# raytype: on ray-case residual S (T\U = {4mu,...,K mu}), split the missing monomials of D by (level, #mu in v, wrap/flat)
# and compare the weighted Delta3 contributions (4 per missing square, wt(v) per missing cube) to mu*(K-3).
# Report, over the S with the largest mu*(K-3)/Delta3, the average share of each type.
import sys, heapq, collections
from itertools import combinations_with_replacement as cwr
from fractions import Fraction as F
def analyse(m, A):
    d = len(A); e = d + 1; mu = A[0]
    mons = {k: [tuple(sum(1 for i in c if i == q) for q in range(d)) for c in cwr(range(d), k)] for k in range(4)}
    sig = lambda v: sum(v[i] * A[i] for i in range(d))
    best = {}
    for k in range(4):
        for v in mons[k]:
            s = sig(v); c = s % m; key = (k * m + s, -k, tuple(-x for x in v))
            if c not in best or key < best[c][0]: best[c] = (key, v)
    X = {c: best[c][1] for c in best}; sg = {c: sig(X[c]) for c in X}; D = set(X.values())
    tau = [None] * m; tau[0] = 0; pq = [(0, 0)]; done = [False] * m
    while pq:
        t, c = heapq.heappop(pq)
        if done[c]: continue
        done[c] = True
        for a in A:
            u = t + a; cc = u % m
            if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
    NE = sorted(tau[c] for c in range(m) if sg[c] > tau[c])
    K = len(NE) + 3
    if NE != [k * mu for k in range(4, K + 1)]: return None
    low = lambda v: [(i, tuple(v[q] - (q == i) for q in range(d))) for i in range(d) if v[i]]
    D3 = 3 * (e - 1) * m - e * sum(sum(X[c]) for c in X)
    contrib = collections.Counter()
    for k in (2, 3):
        for v in mons[k]:
            if v in D: continue
            s = sig(v); typ = 'W' if s >= sg[s % m] + m else 'F'
            wt = 4 if k == 2 else sum(v[i] for i, u in low(v) if u in D)
            contrib[(k, v[0], typ)] += wt
    assert sum(contrib.values()) == D3
    return dict(m=m, e=e, mu=mu, K=K, D3=D3, c=contrib)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:])))
            if r: r['A'] = list(map(int, t[15:])); rows.append(r)
print(f"{sys.argv[1]}: {len(rows)} ray-case S")
rows.sort(key=lambda r: -F(r['mu'] * (r['K'] - 3), r['D3']))
top = rows[:max(1, len(rows) // 50)]
tot = collections.Counter(); 
for r in top:
    for k, v in r['c'].items(): tot[k] += F(v, r['D3'])
print(f"  top {len(top)} by mu(K-3)/D3 (max {float(F(rows[0]['mu'] * (rows[0]['K'] - 3), rows[0]['D3'])):.3f}): mean share of Delta3 by (level, #mu, Wrap/Flat):")
for k, v in sorted(tot.items(), key=lambda x: -x[1])[:10]: print(f"    {k}: {float(v / len(top)):.3f}")
for r in rows[:3]: print(f"  ex: m={r['m']} A={r['A']} mu={r['mu']} K={r['K']} D3={r['D3']} {dict(sorted(r['c'].items()))}")
