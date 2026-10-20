"""SUBADD-TOP via LP (lead, 2026-10-21). For a finite down-set D in N^n with maximal elements Z, maximize
    sum_{y in Z} (|y|-1) eps(y) - (n+1) sum_{b in D \\ Z} eps(b)
over eps >= 0, eps(0) = 0, eps(b+g) <= eps(b) + eps(g) (b, g, b+g in D, b, g != 0), sum eps = 1.
Optimum > 0 refutes SUBADD-TOP for D. Usage: python subadd_lp.py N SIZEMIN SIZEMAX [NRANDOM SEED]"""
import sys, random, itertools
import numpy as np
from scipy.optimize import linprog
def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p): yield (p,) + rest
def downsets(N, size):
    if N == 2:
        for lam in partitions(size): yield [(i, j) for i, row in enumerate(lam) for j in range(row)]
    elif N == 3:
        def layers(k, prev):
            if k == 0: yield []; return
            for s in range(k, 0, -1):
                for lam in partitions(s):
                    if len(lam) <= len(prev) and all(lam[i] <= prev[i] for i in range(len(lam))):
                        for rest in layers(k - s, lam): yield [lam] + rest
        for L in layers(size, (size,) * size):
            yield [(k, i, j) for k, lam in enumerate(L) for i, row in enumerate(lam) for j in range(row)]
def random_downset(N, size, rnd):
    D = {(0,) * N}
    while len(D) < size:
        a = rnd.choice(sorted(D)); i = rnd.randrange(N); b = tuple(a[t] + (t == i) for t in range(N))
        if b in D: continue
        if all(b[t] == 0 or tuple(b[s] - (s == t) for s in range(N)) in D for t in range(N)): D.add(b)
    return sorted(D)
def lp(D, N):
    Ds = set(D); idx = {a: i for i, a in enumerate(D)}; K = len(D)
    Z = [a for a in D if all(tuple(a[s] + (s == t) for s in range(N)) not in Ds for t in range(N))]
    Zs = set(Z)
    c = np.zeros(K)
    for a in D:
        if a in Zs: c[idx[a]] -= (sum(a) - 1)
        elif any(a): c[idx[a]] += (N + 1)
    rows = []
    nz = [a for a in D if any(a)]
    for i, b in enumerate(nz):
        for g in nz[i:]:
            s = tuple(x + y for x, y in zip(b, g))
            if s in Ds:
                r = np.zeros(K); r[idx[s]] += 1; r[idx[b]] -= 1; r[idx[g]] -= 1; rows.append(r)
    A_ub = np.array(rows) if rows else None; b_ub = np.zeros(len(rows)) if rows else None
    A_eq = np.ones((1, K)); A_eq[0, idx[(0,) * N]] = 0
    A_eq = np.vstack([A_eq, np.eye(K)[idx[(0,) * N]]]); b_eq = np.array([1.0, 0.0])
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * K, method='highs')
    return -res.fun, res.x, Z
if __name__ == '__main__':
    N, SMIN, SMAX = map(int, sys.argv[1:4]); NR = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    rnd = random.Random(int(sys.argv[5]) if len(sys.argv) > 5 else 1)
    ZMAX = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    zhist = {}
    tot = fail = 0; best = None
    for size in range(SMIN, SMAX + 1):
        it = (random_downset(N, size, rnd) for _ in range(NR)) if NR else downsets(N, size)
        for D in it:
            if len(D) < 2: continue
            v, x, Z = lp(D, N)
            if ZMAX and len(Z) > ZMAX: continue
            tot += 1
            if best is None or v > best[0]: best = (v, D, Z, [round(t, 4) for t in x])
            if v > 1e-9:
                zhist[len(Z)] = zhist.get(len(Z), 0) + 1
                fail += 1
                if fail <= 3: print("SUBADD-TOP FAIL value %.5f D=%s Z=%s eps=%s" % (v, D, Z, [round(t, 4) for t in x]), flush=True)
        print("size %d done: tested %d, failures %d, best value %.6f, failures by #maximal %s" % (size, tot, fail, best[0] if best else 0, zhist), flush=True)
