# For fixed p: tiles = chambers of the Groebner fan (all coherent, coherent.py). Moves: for a corner relation
# lam = q - f(q) (q a minimal non-element, f(q) its rep in D), D' = { y + k(y)*(-lam) } ... i.e. flip the binomial:
# cells y >= f(q) - ... We implement the wall crossing for lam = u - v (u = q leading, v = f(q) standard):
# after crossing, v-side becomes larger: each y in D is replaced by y + k*lam with k = max{k >= 0 : y + k lam >= 0}.
# Keep D' if it is a down-set (then it is a tile).  Study local minima of K_s on the move graph.
import sys
import numpy as np
from collections import defaultdict
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = int(sys.argv[1]); m0, m1 = int(sys.argv[2]), int(sys.argv[3])
def isdown(S):
    return all(all(y[b] == 0 or tuple(y[:b] + (y[b]-1,) + y[b+1:]) in S for b in range(d)) for y in S)
def Kvec(Dl, pv, m):
    M = m*(m-1)//2; D = set(Dl); tau = tops(D, d); X = np.zeros(m, dtype=np.int64)
    for a in range(d):
        tp = np.array([int(np.dot(tuple(x[:a]) + (tau[x][a],) + tuple(x[a+1:]), pv) % m) for x in Dl])
        X += ((tp[None, :] - np.arange(m)[:, None]) % m).sum(axis=1)
    return ((d+1)*M - X)//m
for m in range(m0, m1 + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m)
    tiles = defaultdict(list)
    for D in downsets(m, d):
        Dl = sorted(D); C = np.array(Dl)
        pos = (P @ C.T) % m
        for pi in np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]: tiles[pi].append(frozenset(Dl))
    stats = defaultdict(int); bad = []
    for pi, Ts in tiles.items():
        pv = P[pi]; idx = {D: i for i, D in enumerate(Ts)}
        Ks = [Kvec(sorted(D), pv, m) for D in Ts]
        nbrs = [set() for _ in Ts]
        for i, D in enumerate(Ts):
            rep = {int(np.dot(x, pv) % m): x for x in D}
            cors = set()
            for x in D:
                for a in range(d):
                    y = list(x); y[a] += 1; y = tuple(y)
                    if y not in D and all(y[b] == 0 or tuple(y[:b] + (y[b]-1,) + y[b+1:]) in D for b in range(d)): cors.add(y)
            for q in cors:
                lam = np.array(q) - np.array(rep[int(np.dot(q, pv) % m)])
                g = reduce(gcd, [abs(int(v)) for v in lam])
                g = max(h for h in range(1, g + 1) if g % h == 0 and int(np.dot(lam // h, pv)) % m == 0); lam = lam // g
                neg = [a for a in range(d) if lam[a] < 0]
                Dn = set()
                for y in D:
                    k = min(y[a] // (-lam[a]) for a in neg) if neg else 0
                    Dn.add(tuple(int(v) for v in np.array(y) + k*lam))
                Dn = frozenset(Dn)
                if Dn != D and Dn in idx: nbrs[i].add(idx[Dn])
                elif Dn != D and isdown(Dn): stats['move to unlisted tile?!'] += 1
        stats['tiles'] += len(Ts)
        # connectivity
        seen = {0}; st = [0]
        while st:
            u = st.pop()
            for v in nbrs[u]:
                if v not in seen: seen.add(v); st.append(v)
        stats['p disconnected'] += (len(seen) != len(Ts)); stats['p'] += 1
        for s in range(m):
            gmin = min(K[s] for K in Ks)
            for i in range(len(Ts)):
                if all(Ks[j][s] >= Ks[i][s] for j in nbrs[i]):
                    stats['local minima'] += 1
                    if Ks[i][s] > gmin: stats['non-global local minima'] += 1
                    C = np.array(sorted(Ts[i])); isbox = int(np.prod(C.max(axis=0) + 1)) == m
                    stats['local-min boxes'] += isbox
    print(f'd={d} m={m}:', dict(stats), flush=True)
