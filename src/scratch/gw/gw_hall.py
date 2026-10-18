# Reflection graph for GW.  Gap z = v(x) - i*m (x in D, 1 <= i <= kappa(x)).  For every y in D with y >= x,
# delta = v(y - x) + (i-1)*m is an element of Delta below c (reflection z -> v(y) - m - z).  Variants:
#   'all'    : y ranges over all cells >= x;   'corner' : y ranges over maximal cells >= x.
# For each instance compute b* = least capacity b such that a b-matching saturates all gaps (max-flow), and compare
# with d and with ceil(g / l).  GW <=> g <= d*l; "reflection Hall" <=> b* <= d.
import sys, numpy as np
from itertools import product
from math import ceil
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
d, m0, m1, K = map(int, sys.argv[1:5])
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
def downsets(M):
    lev = {frozenset([tuple([0] * d)])}
    for m in range(1, M + 1):
        if m >= m0: yield m, lev
        nxt = set()
        for D in lev:
            for x in D:
                for u in U:
                    y = tuple(p + q for p, q in zip(x, u))
                    if y not in D and all(y[a] == 0 or tuple(y[b] - (b == a) for b in range(d)) in D for a in range(d)):
                        nxt.add(D | {y})
        lev = nxt
def bstar(D, n, m, mode):
    V = {x: sum(a * b for a, b in zip(x, n)) for x in D}; M = max(V.values()); c = M - m + 1
    corners = [y for y in D if all(tuple(p + q for p, q in zip(y, u)) not in D for u in U)]
    gaps = [(x, i) for x in D for i in range(1, V[x] // m + 1)]
    elems = sorted({V[x] + j * m for x in D for j in range(0, (M - V[x]) // m) if V[x] + j * m < c})
    if not gaps: return 0, 0, len(elems)
    eid = {e: k for k, e in enumerate(elems)}
    ys = corners if mode == 'corner' else list(D)
    edges = set()
    for gi, (x, i) in enumerate(gaps):
        for y in ys:
            if all(p >= q for p, q in zip(y, x)):
                dl = V[y] - V[x] + (i - 1) * m
                assert dl in eid, (dl, c)
                edges.add((gi, eid[dl]))
    G, E = len(gaps), len(elems)
    def flow(b):   # source 0, gaps 1..G, elems G+1..G+E, sink G+E+1
        rows, cols, caps = [], [], []
        for gi in range(G): rows.append(0); cols.append(1 + gi); caps.append(1)
        for gi, ei in edges: rows.append(1 + gi); cols.append(1 + G + ei); caps.append(1)
        for ei in range(E): rows.append(1 + G + ei); cols.append(1 + G + E); caps.append(b)
        A = csr_matrix((np.array(caps, dtype=np.int32), (rows, cols)), shape=(G + E + 2, G + E + 2))
        return maximum_flow(A, 0, G + E + 1).flow_value
    lo, hi = 1, G
    while lo < hi:
        mid = (lo + hi) // 2
        if flow(mid) == G: hi = mid
        else: lo = mid + 1
    return lo, G, E
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    ks = list(product(range(K + 1), repeat=d))
    st = {'all': [0, 0, 0], 'corner': [0, 0, 0]}; tested = 0; worst = {}
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            for k in ks:
                n = tuple(int(si + m * ki) for si, ki in zip(s, k)); tested += 1
                for mode in ('all', 'corner'):
                    b, g, l = bstar(D, n, m, mode)
                    if g == 0: continue
                    lb = ceil(g / l)
                    st[mode][0] += 1; st[mode][1] += b > d; st[mode][2] += b > lb
                    if b > d and (mode not in worst or b - d > worst[mode][0]): worst[mode] = (b - d, n, sorted(D), g, l, b)
    print(f"d={d} m={m} K={K} instances={tested}  [with gaps, b*>d, b*>ceil(g/l)]: all={st['all']} corner={st['corner']}", flush=True)
    for mode, w in worst.items(): print('    worst', mode, w, flush=True)
