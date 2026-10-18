# Corner reduction test.  Proven: g <= t(D)*l (corner reflection), so GW holds when t(D) <= d.
# CR: for every residue-complete (D,n) with t(D) > d, is there a single flip D -> D' (remove a corner y, add an
# addable z with the same residue), keeping all d unit vectors, with E(D',n) <= E(D,n) and t(D') < t(D)?
# Also counts instances with t > d at all, and how often an E-nonincreasing flip exists without the t condition.
import sys, numpy as np
from itertools import product
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
def corners(D): return [y for y in D if all(add(y, u) not in D for u in U)]
def E(D, n, m):
    V = [sum(a * b for a, b in zip(x, n)) for x in D]
    return d * max(V) - (d + 1) * sum(v // m for v in V) - d * (m - 1)
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    big = red = anyflip = 0; ex = None
    for D in lev:
        if any(u not in D for u in U): continue
        t = len(corners(D))
        if t <= d: continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            for k in product(range(K + 1), repeat=d):
                n = tuple(int(si + m * ki) for si, ki in zip(s, k)); big += 1; e0 = E(D, n, m)
                res = lambda x: sum(a * b for a, b in zip(x, n)) % m
                found = foundany = False
                for y in corners(D):
                    if not any(y): continue
                    Dm = D - {y}; ry = res(y)
                    cand = {add(x, u) for x in Dm for u in U}
                    for z in cand:
                        if z in Dm or z == y or res(z) != ry: continue
                        if not all(z[a] == 0 or sub(z, U[a]) in Dm for a in range(d)): continue
                        D2 = Dm | {z}
                        if any(u not in D2 for u in U): continue
                        e2 = E(D2, n, m)
                        if e2 <= e0:
                            foundany = True
                            if len(corners(D2)) < t: found = True; break
                    if found: break
                red += found; anyflip += foundany
                if not found and ex is None: ex = (n, e0, t, sorted(D))
    print(f"d={d} m={m} K={K} instances with t>d: {big}; corner-reducing E-nonincreasing flip exists: {red}; "
          f"any E-nonincreasing flip: {anyflip}; first failure: {ex}", flush=True)
