# Extended reflection graph.  Gaps (x,i): z = v(x) - i m, 1 <= i <= kappa(x).  Elements below c: (w,h) <-> v(w)+(h-1)m.
#   reflection edges : (x,i) -> (y-x, i)  for maximal y >= x
#   direction edges  : (x,1) -> (x-e_a, 1) for x_a > 0 with v(x) - n_a < c      [z -> z + m - n_a]
# b* = least capacity saturating all gaps.  Reports instances with b* > d, split by multiplicity form (all n_a > m).
import sys, numpy as np
from itertools import product
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
d, m0, m1, K = map(int, sys.argv[1:5]); kmin = int(sys.argv[5]) if len(sys.argv) > 5 else 0
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
def bstar(D, n, m, use_dir):
    V = {x: sum(a * b for a, b in zip(x, n)) for x in D}; M = max(V.values()); c = M - m + 1
    cor = [y for y in D if all(add(y, u) not in D for u in U)]
    gaps = [(x, i) for x in D for i in range(1, V[x] // m + 1)]
    if not gaps: return 0
    elems = {(w, h): None for w in D for h in range(1, (M - V[w]) // m + 1)}
    eid = {e: k for k, e in enumerate(elems)}; G, E = len(gaps), len(eid)
    edges = set()
    for gi, (x, i) in enumerate(gaps):
        for y in cor:
            if all(p >= q for p, q in zip(y, x)): edges.add((gi, eid[(sub(y, x), i)]))
        if use_dir and i == 1:
            for a in range(d):
                if x[a] > 0 and V[x] - n[a] < c: edges.add((gi, eid[(sub(x, U[a]), 1)]))
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
    ks = [k for k in product(range(kmin, K + 1), repeat=d)]
    st = {True: [0, 0, 0], False: [0, 0, 0]}; ex = {}
    for D in lev:
        if any(u not in D for u in U): continue
        t = sum(all(add(y, u) not in D for u in U) for y in D)
        if t <= d: continue                      # covered by GW-8/9
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            for k in ks:
                n = tuple(int(si + m * ki) for si, ki in zip(s, k)); mf = min(k) >= 1
                b0 = bstar(D, n, m, False); b1 = bstar(D, n, m, True)
                st[mf][0] += 1; st[mf][1] += b0 > d; st[mf][2] += b1 > d
                if b1 > d and mf not in ex: ex[mf] = (n, sorted(D), b1)
    print(f"d={d} m={m} [t>d instances, b*>d reflection only, b*>d with direction edges]  mult-form={st[True]}  other={st[False]}  ex={ex}", flush=True)
