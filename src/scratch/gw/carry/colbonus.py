"""Column-residue identity:  d*ell - g = sum_x r(x)/m + sum_b sum_{b-columns C} Psi_b(C)   (any down-set), where
Psi_b(C) = (J+1)*lambda(t) + #{j<=J : (j n_b mod m) + eps_t >= m} - (1/m) sum_j (j n_b mod m), t = top, M-v(t) = m*lambda(t)+eps_t.
Residue completeness: sum_x r(x)/m = (m-1)/2.
CBH (column bonus Hall): negative columns can be paid by the bonuses r(x)/m of their own cells, each bonus used once.
Checks the identity and CBH (max-flow, integer scaled by m) on residue-complete down-sets and semigroups.  fejer only.
Usage: colbonus.py ds d m0 m1 K | colbonus.py sg G"""
import sys, numpy as np
from itertools import product
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
def flowok(sup, dem, edges):
    need = sum(dem.values())
    if need == 0: return True, 0
    A = list(sup); B = list(dem); ia = {a: i for i, a in enumerate(A)}; ib = {b: i for i, b in enumerate(B)}
    N = 2 + len(A) + len(B); ii = []; jj = []; vv = []
    for a in A:
        if sup[a] > 0: ii.append(0); jj.append(2 + ia[a]); vv.append(sup[a])
    for b in B: ii.append(2 + len(A) + ib[b]); jj.append(1); vv.append(dem[b])
    for a, b in edges: ii.append(2 + ia[a]); jj.append(2 + len(A) + ib[b]); vv.append(10**7)
    G = csr_matrix((np.array(vv, dtype=np.int64).astype(np.int32), (ii, jj)), shape=(N, N))
    f = maximum_flow(G, 0, 1).flow_value
    return f >= need, need - f
def analyze(D, n, m):
    d = len(n); v = {x: sum(a * b for a, b in zip(x, n)) for x in D}; M = max(v.values())
    g = sum(v[x] // m for x in D); ell = sum((M - v[x]) // m for x in D)
    cols = {}; members = {}
    for x in D:
        for b in range(d):
            z = tuple(0 if i == b else x[i] for i in range(d)); key = (b, z)
            members.setdefault(key, []).append(x)
            if key in cols: continue
            J = 0
            while tuple(J + 1 if i == b else z[i] for i in range(d)) in D: J += 1
            t = tuple(J if i == b else z[i] for i in range(d)); lt, et = divmod(M - v[t], m)
            rho = [(j * n[b]) % m for j in range(J + 1)]
            cols[key] = m * (J + 1) * lt + m * sum(1 for p in rho if p + et >= m) - sum(rho)   # = m*Psi
    total = sum(v[x] % m for x in D) + sum(cols.values())
    assert total == m * (d * ell - g), (total, m * (d * ell - g))
    dem = {k: -c for k, c in cols.items() if c < 0}
    sup = {x: v[x] % m for x in D}
    edges = [(x, k) for k in dem for x in members[k]]
    ok, short = flowok(sup, dem, edges)
    return ok, short, d * ell - g
def report(tag, tot, fail, ex): print(f"{tag} inst={tot} CBHfail={fail} ex={ex}", flush=True)
if sys.argv[1] == 'ds':
    d, m0, m1, K = map(int, sys.argv[2:6])
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
    lev = {frozenset([tuple([0] * d)])}
    for m in range(1, m1 + 1):
        if m >= m0:
            tot = fail = 0; ex = None
            for D in lev:
                if any(u not in D for u in U): continue
                Ds = sorted(D); X = np.array(Ds)
                for s in product(range(1, m), repeat=d):
                    if len({int(r) for r in (X @ np.array(s)) % m}) != m: continue
                    for k in product(range(1, K + 1), repeat=d):
                        n = tuple(si + m * ki for si, ki in zip(s, k))
                        ok, short, W = analyze(D, n, m); tot += 1
                        if not ok:
                            fail += 1
                            if ex is None: ex = (n, Ds, 'short/m', short, 'GW', W)
            report(f"d={d} m={m} K={K}", tot, fail, ex)
        nxt = set()
        for D in lev:
            for x in D:
                for u in U:
                    y = add(x, u)
                    if y not in D and all(y[a] == 0 or sub(y, U[a]) in D for a in range(d)): nxt.add(D | {y})
        lev = nxt
else:
    G = int(sys.argv[2]); tot = fail = 0; ex = []
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
            ok, short, W = analyze(D, ng, m); tot += 1
            if not ok:
                fail += 1
                if len(ex) < 4: ex.append((gens, 'short/m', short, 'W', W))
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
    report(f"semigroups genus<={G}", tot, fail, ex)
