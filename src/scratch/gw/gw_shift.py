# Depth-preserving injections cannot prove GW (per-depth |U_i| <= d|L_i| fails).  Test the graph with DEPTH-LOWERING
# reflections: gap (x,i) -> element (y - x, h) for every maximal y >= x and every 1 <= h <= i
# [the element v(y-x) + (h-1)m, i.e. the reflected gap minus (i-h)m].  Optionally add column reflections
# (x,i) -> (R_a x, h), h <= i, when valid.  b* = least capacity saturating all gaps; GW <=> b* can be <= d?
import sys, numpy as np
from itertools import product
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
d, m0, m1, K = map(int, sys.argv[1:5]); usecol = len(sys.argv) > 5
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
def downsets(M):
    lev = {frozenset([tuple([0] * d)])}
    for m in range(1, M + 1):
        if m >= m0: yield m, lev
        nxt = set()
        for D in lev:
            for x in D:
                for u in U:
                    y = add(x, u)
                    if y not in D and all(y[a] == 0 or sub(y, U[a]) in D for a in range(d)): nxt.add(D | {y})
        lev = nxt
def bstar(D, n, m):
    V = {x: sum(a * b for a, b in zip(x, n)) for x in D}; M = max(V.values())
    gaps = [(x, i) for x in D for i in range(1, V[x] // m + 1)]
    if not gaps: return 0
    elems = {}
    for w in D:
        for h in range(1, (M - V[w]) // m + 1): elems[(w, h)] = len(elems)
    cor = [y for y in D if all(add(y, u) not in D for u in U)]
    def top(x, a):
        y = x
        while add(y, U[a]) in D: y = add(y, U[a])
        return y
    edges = set()
    for gi, (x, i) in enumerate(gaps):
        for y in cor:
            if all(p >= q for p, q in zip(y, x)):
                w = sub(y, x)
                for h in range(1, i + 1): edges.add((gi, elems[(w, h)]))
        if usecol:
            for a in range(d):
                t = top(x, a); w = tuple(t[a] - x[b] if b == a else x[b] for b in range(d))
                for h in range(1, i + 1):
                    if (w, h) in elems: edges.add((gi, elems[(w, h)]))
    G, E = len(gaps), len(elems)
    def flow(b):
        r = [0] * G + [1 + gi for gi, _ in edges] + [1 + G + ei for ei in range(E)]
        cc = [1 + gi for gi in range(G)] + [1 + G + ei for _, ei in edges] + [1 + G + E] * E
        cap = [1] * G + [1] * len(edges) + [b] * E
        A = csr_matrix((np.array(cap, dtype=np.int32), (r, cc)), shape=(G + E + 2, G + E + 2))
        return maximum_flow(A, 0, G + E + 1).flow_value
    lo, hi = 1, G
    while lo < hi:
        mid = (lo + hi) // 2
        if flow(mid) == G: hi = mid
        else: lo = mid + 1
    return lo
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    tot = bad = 0; ex = None
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            for k in product(range(K + 1), repeat=d):
                n = tuple(int(si + m * ki) for si, ki in zip(s, k)); tot += 1
                b = bstar(D, n, m)
                if b > d:
                    bad += 1
                    if ex is None: ex = (n, sorted(D), b)
    print(f"d={d} m={m} K={K} col={usecol} instances={tot} b*>d: {bad} ex={ex}", flush=True)
