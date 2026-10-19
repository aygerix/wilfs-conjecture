"""Column payment CPC: carry(x) = kappa(x) - sum_a floor(x_a n_a/m); column slack s(b,z) = sum_j [lambda(R_b(z+j e_b))
- floor(j n_b/m)] >= 0.  GW <=> sum carry <= sum s.  CPC: carries can be routed from cell x to columns through x in
directions b in supp(x) [rule 'own'], or to any column through x [rule 'thru'], or columns through x or its lower covers
['near'].  Exhaustive residue-complete down-sets (d, m0..m1, lifts 1..K) and semigroups (genus <= G).  fejer only.
Usage: colpay.py ds d m0 m1 K | colpay.py sg G"""
import sys, numpy as np
from itertools import product
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
def flowok(dem, cap, edges):
    need = sum(dem.values())
    if need == 0: return True
    A = list(dem); B = list(cap); ia = {a: i for i, a in enumerate(A)}; ib = {b: i for i, b in enumerate(B)}
    N = 2 + len(A) + len(B); ii = []; jj = []; vv = []
    for a in A: ii.append(0); jj.append(2 + ia[a]); vv.append(dem[a])
    for b in B:
        if cap[b] > 0: ii.append(2 + len(A) + ib[b]); jj.append(1); vv.append(cap[b])
    for a, b in edges: ii.append(2 + ia[a]); jj.append(2 + len(A) + ib[b]); vv.append(10**6)
    G = csr_matrix((np.array(vv, dtype=np.int32), (ii, jj)), shape=(N, N))
    return maximum_flow(G, 0, 1).flow_value >= need
def analyze(D, n, m):
    """D: set of tuples, n: weights. returns dict of rule -> ok, plus totals"""
    d = len(n); v = {x: sum(a * b for a, b in zip(x, n)) for x in D}; M = max(v.values())
    lam = lambda y: (M - v[y]) // m
    carry = {x: v[x] // m - sum((x[a] * n[a]) // m for a in range(d)) for x in D}
    col = {}; colof = {}
    for x in D:
        for b in range(d):
            z = tuple(0 if i == b else x[i] for i in range(d)); key = (b, z)
            colof[(x, b)] = key
            if key in col: continue
            J = 0
            while tuple(J + 1 if i == b else z[i] for i in range(d)) in D: J += 1
            s = 0
            for j in range(J + 1):
                y = tuple(J - j if i == b else z[i] for i in range(d))   # R_b(z + j e_b)
                s += lam(y) - (j * n[b]) // m
            col[key] = s
    dem = {x: c for x, c in carry.items() if c > 0}
    res = {}
    for rule in ('own', 'thru', 'near'):
        edges = set()
        for x in dem:
            if rule == 'own': bs = [b for b in range(d) if x[b]]; cells = [x]
            elif rule == 'thru': bs = range(d); cells = [x]
            else:
                bs = range(d); cells = [x] + [tuple(x[i] - (i == a) for i in range(d)) for a in range(d) if x[a]]
            for y in cells:
                for b in bs: edges.add((x, colof[(y, b)]))
        res[rule] = flowok(dem, col, edges)
    return res, sum(carry.values()), sum(col.values())
if sys.argv[1] == 'ds':
    d, m0, m1, K = map(int, sys.argv[2:6]); nores = len(sys.argv) > 6
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
    lev = {frozenset([tuple([0] * d)])}
    for m in range(1, m1 + 1):
        if m >= m0:
            tot = 0; fail = {'own': 0, 'thru': 0, 'near': 0}; ex = {}
            for D in lev:
                if any(u not in D for u in U): continue
                Ds = sorted(D); X = np.array(Ds)
                for s in product(range(1, m), repeat=d):
                    if not nores and len({int(r) for r in (X @ np.array(s)) % m}) != m: continue
                    for k in product(range(1, K + 1), repeat=d):
                        n = tuple(si + m * ki for si, ki in zip(s, k))
                        res, tc, ts = analyze(D, n, m); tot += 1
                        gwbad = tc > ts
                        fail.setdefault('GWfail', 0); fail['GWfail'] += gwbad
                        for r, ok in res.items():
                            if not ok:
                                fail[r] += 1
                                if r == 'near' and not gwbad: fail.setdefault('near_but_GW_ok', 0); fail['near_but_GW_ok'] += 1; ex.setdefault('nearGWok', (n, Ds, tc, ts))
                                if r not in ex: ex[r] = (n, Ds, tc, ts)
            print(f"d={d} m={m} K={K} inst={tot} fails={fail} ex={ex}", flush=True)
        nxt = set()
        for D in lev:
            for x in D:
                for u in U:
                    y = add(x, u)
                    if y not in D and all(y[a] == 0 or sub(y, U[a]) in D for a in range(d)): nxt.add(D | {y})
        lev = nxt
else:
    G = int(sys.argv[2]); tot = 0; fail = {'own': 0, 'thru': 0, 'near': 0}; ex = {}
    stack = [(0, -1, 1, [1], 0)]
    while stack:
        gm, F, m, gens, g = stack.pop()
        if F + 1 > 0 and m > 1:
            isS = lambda z: z >= 0 and not ((gm >> z) & 1)
            ap = []
            for r in range(m):
                w = r
                while not isS(w): w += m
                ap.append(w)
            M = max(ap); ng = sorted(x for x in gens if x != m); d = len(ng)
            rep = [None] * (d + 1); rep[d] = {0}
            for kk in range(d - 1, -1, -1):
                st = set()
                for val in rep[kk + 1]:
                    t = val
                    while t <= M: st.add(t); t += ng[kk]
                rep[kk] = st
            D = set()
            for w in ap:
                x = []; rem = w
                for kk in range(d):
                    t = 0
                    while rem - t * ng[kk] not in rep[kk + 1]: t += 1
                    x.append(t); rem -= t * ng[kk]
                D.add(tuple(x))
            res, tc, ts = analyze(D, ng, m); tot += 1
            for r, ok in res.items():
                if not ok:
                    fail[r] += 1
                    if r not in ex: ex[r] = (gens, tc, ts)
        if g < G:
            for nn in gens:
                if nn <= F: continue
                gm2 = gm | (1 << nn)
                if nn == m: m2 = m + 1; ng2 = list(range(m2, 2 * m2))
                else:
                    m2 = m; ng2 = [k for k in gens if k != nn]; y = nn + m
                    dec = any(a != nn and not ((gm2 >> a) & 1) and (y - a) != nn and not ((gm2 >> (y - a)) & 1) for a in range(m, y // 2 + 1))
                    if not dec: ng2.append(y)
                stack.append((gm2, nn, m2, ng2, g + 1))
    print(f"semigroups genus<={G}: {tot} fails={fail} ex={ex}")
