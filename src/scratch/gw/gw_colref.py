# Column reflections.  R_a(x) reflects x inside its a-column (x_a -> h-1-x_a).  For a gap (x,i) [z = v(x) - i m],
# the image (R_a x, i) [element v(R_a x) + (i-1) m] is an element below c iff i m <= x_a n_a + U(top_a x), and for
# each a the map (x,i) -> (R_a x, i) is INJECTIVE (R_a is a bijection of D).  Questions:
#  (Q1) is every gap in the domain of some column reflection?  (then g <= d l, i.e. GW)
#  (Q2) b* with column-reflection edges + corner-reflection edges.
import sys, numpy as np
from itertools import product
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
d, m0, m1, K = map(int, sys.argv[1:5])
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
def analyse(D, n, m):
    V = {x: sum(a * b for a, b in zip(x, n)) for x in D}; M = max(V.values()); c = M - m + 1
    def top(x, a):
        y = x
        while add(y, U[a]) in D: y = add(y, U[a])
        return y
    def refl(x, a):
        t = top(x, a); h = t[a]; return tuple(h - x[b] if b == a else x[b] for b in range(d))
    gaps = [(x, i) for x in D for i in range(1, V[x] // m + 1)]
    if not gaps: return True, 0, 0
    cor = [y for y in D if all(add(y, u) not in D for u in U)]
    elems = {}; 
    for w in D:
        for h in range(1, (M - V[w]) // m + 1): elems[(w, h)] = len(elems)
    edges = set(); allcov = True
    for gi, (x, i) in enumerate(gaps):
        cov = False
        for a in range(d):
            if i * m <= x[a] * n[a] + (M - V[top(x, a)]):
                e = (refl(x, a), i); assert e in elems; edges.add((gi, elems[e])); cov = True
        allcov &= cov
        for y in cor:
            if all(p >= q for p, q in zip(y, x)): edges.add((gi, elems[(sub(y, x), i)]))
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
    return allcov, lo, G
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    tot = notcov = bad = big = 0; ex1 = ex2 = None
    for D in lev:
        if any(u not in D for u in U): continue
        t = sum(all(add(y, u) not in D for u in U) for y in D)
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            for k in product(range(K + 1), repeat=d):
                n = tuple(int(si + m * ki) for si, ki in zip(s, k))
                cov, b, G = analyse(D, n, m); tot += 1; big += t > d
                if not cov:
                    notcov += 1
                    if ex1 is None: ex1 = (n, sorted(D))
                if b > d:
                    bad += 1
                    if ex2 is None: ex2 = (n, sorted(D), b)
    print(f"d={d} m={m} K={K} instances={tot} (t>d: {big}) gaps not covered by column reflections: {notcov}; b*>d with column+corner edges: {bad}; ex1={ex1} ex2={ex2}", flush=True)
