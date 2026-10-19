"""Cover-payment CP on residue-complete (or arbitrary, with --nores) multiplicity-form down-sets.
Delta(x) = sum_b lambda(R_b x) - kappa(x).  CP: deficits (Delta<0) can be routed to lower covers with surplus.
Exhaustive: all down-sets of size m in N^d with all units, residues s in {1..m-1}^d bijective, lifts k in {1..K}^d.
Usage: cp_downsets.py d m0 m1 K [nores]   (fejer)"""
import sys, numpy as np
from itertools import product
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
d, m0, m1, K = map(int, sys.argv[1:5]); nores = len(sys.argv) > 5
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
def flow(defs, surp, edges):
    need = int(sum(defs.values()))
    X = list(surp); Y = list(defs); ix = {x: i for i, x in enumerate(X)}; iy = {y: k for k, y in enumerate(Y)}
    N = 2 + len(X) + len(Y); ii = []; jj = []; vv = []
    for x in X: ii.append(0); jj.append(2 + ix[x]); vv.append(int(surp[x]))
    for y in Y: ii.append(2 + len(X) + iy[y]); jj.append(1); vv.append(int(defs[y]))
    for (x, y) in edges:
        if x in ix: ii.append(2 + ix[x]); jj.append(2 + len(X) + iy[y]); vv.append(10**6)
    G = csr_matrix((np.array(vv, dtype=np.int32), (ii, jj)), shape=(N, N))
    return maximum_flow(G, 0, 1).flow_value >= need
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    ks = np.array(list(product(range(1, K + 1), repeat=d)), dtype=np.int64)
    tot = gwfail = withdef = cpfail = eqfail = 0; ex = None; ex2 = None
    for D in lev:
        if any(u not in D for u in U): continue
        Ds = sorted(D); X = np.array(Ds, dtype=np.int64); idx = {x: i for i, x in enumerate(Ds)}
        R = np.zeros((d, len(Ds)), dtype=np.int64)
        for i, x in enumerate(Ds):
            for a in range(d):
                t = x
                while add(t, U[a]) in D: t = add(t, U[a])
                y = tuple(t[a] - x[a] if b == a else x[b] for b in range(d)); R[a, i] = idx[y]
        covers = [(i, idx[sub(x, U[a])]) for i, x in enumerate(Ds) for a in range(d) if x[a]]  # (y, x=y-e_a)
        if nores: Ss = S
        else:
            ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0); Ss = S[ok]
        for s in Ss:
            N = s[None, :] + m * ks; V = X @ N.T; Mx = V.max(0)
            kap = V // m; lam = (Mx[None, :] - V) // m
            Dl = sum(lam[R[a]] for a in range(d)) - kap      # (m, nk)
            tot += V.shape[1]
            gwfail += int((Dl.sum(0) < 0).sum())
            for j in np.nonzero((Dl < 0).any(0))[0]:
                withdef += 1
                col = Dl[:, j]
                defs = {i: -col[i] for i in range(len(Ds)) if col[i] < 0}
                surp = {i: col[i] for i in range(len(Ds)) if col[i] > 0}
                edges = [(x, y) for (y, x) in covers if y in defs]
                deg = {}
                for (y, x) in covers:
                    if y in defs: deg[y] = deg.get(y, 0) + 1
                load = {}
                for (y, x) in covers:
                    if y in defs: load[x] = load.get(x, 0) + defs[y] / deg[y]
                if any(load[x] > max(0, col[x]) + 1e-9 for x in load):
                    eqfail += 1
                    if ex2 is None: ex2 = (tuple(int(t) for t in N[j]), Ds, {Ds[i]: int(col[i]) for i in range(len(Ds)) if col[i]})
                if not flow(defs, surp, edges):
                    cpfail += 1
                    if ex is None: ex = (tuple(int(t) for t in N[j]), Ds, {Ds[i]: int(col[i]) for i in range(len(Ds)) if col[i]}, 'GWslack', int(col.sum()))
    print(f"d={d} m={m} K={K} nores={nores} inst={tot} GWfail={gwfail} withdeficit={withdef} CPfail={cpfail} EQSPLITfail={eqfail} ex={ex} ex2={ex2}", flush=True)
