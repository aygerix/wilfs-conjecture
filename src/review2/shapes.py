# Shape-first, fan-free enumeration (referee): every finite down-set D in N^3 with |D| = m that is NON-two-face
# (contains (1,1,0),(1,0,1),(0,1,1)) and has delta = H(D) - (m-1) < 0; then decide whether D is the factorization tile
# of some e = 4 semigroup with multiplicity m: exists r in (Z/m)^3 with x -> r.x injective on D, and the open
# Groebner cone {p > 0 : p.(q - rep_r(q)) > 0 for all minimal non-elements q} is nonempty (exact polygon clipping).
import sys, time
import numpy as np
from fractions import Fraction as Fr
from itertools import product
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from tk import H_of, min_nonelements, two_face_pairs

def parts_in(lam, s, i=0, prev=None):
    """partitions mu (tuples, no trailing zeros) with mu_i <= lam_i, mu nonincreasing, |mu| = s."""
    if s == 0: yield (); return
    if i >= len(lam): return
    hi = min(lam[i], s if prev is None else min(prev, s))
    # remaining capacity check
    for v in range(hi, 0, -1):
        cap = sum(min(lam[k], v) for k in range(i + 1, len(lam)))
        if v + cap < s: break
        for rest in parts_in(lam, s - v, i + 1, v): yield (v,) + rest

def plane_partitions_nt(n):
    """plane partitions as layer lists [lam0, lam1, ...], non-two-face constraint on lam0, lam1."""
    big = (n,)*n
    for k0 in range(4, n - 2):
        for lam0 in parts_in(big, k0):
            if len(lam0) < 2 or lam0[1] < 2: continue
            for k1 in range(3, min(k0, n - k0) + 1):
                for lam1 in parts_in(lam0, k1):
                    if lam1[0] < 2 or len(lam1) < 2: continue
                    yield from extend([lam0, lam1], n - k0 - k1)

def extend(layers, rem):
    if rem == 0: yield layers; return
    last = layers[-1]
    for k in range(min(rem, sum(last)), 0, -1):
        for lam in parts_in(last, k):
            yield from extend(layers + [lam], rem - k)

def cells(layers):
    return {(i, j, k) for k, lam in enumerate(layers) for i, L in enumerate(lam) for j in range(L)}

def injective_rs(D, m):
    X = np.array(sorted(D), dtype=np.int64)              # (m,3)
    R = np.array(list(product(range(m), repeat=3)), dtype=np.int64)
    V = (R @ X.T) % m
    V.sort(axis=1)
    ok = np.all(V[:, 1:] != V[:, :-1], axis=1)
    return [tuple(int(c) for c in r) for r in R[ok]]

def clip(poly, v):
    dot = lambda p: sum(pi*vi for pi, vi in zip(p, v))
    out = []; n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        dp, dq = dot(P), dot(Q)
        if dp >= 0: out.append(P)
        if (dp > 0 and dq < 0) or (dp < 0 and dq > 0):
            t = dp/(dp - dq); out.append(tuple(a + t*(b - a) for a, b in zip(P, Q)))
    res = []
    for P in out:
        if P not in res: res.append(P)
    return res

def area2(poly):
    # twice the area of the polygon projected to (p1, p2)
    s = 0
    for i in range(len(poly)):
        (x1, y1, _), (x2, y2, _) = poly[i], poly[(i + 1) % len(poly)]
        s += x1*y2 - x2*y1
    return abs(s)

def open_cone(D, m, r):
    cls = {sum(a*b for a, b in zip(r, x)) % m: x for x in D}
    poly = [(Fr(1), Fr(0), Fr(0)), (Fr(0), Fr(1), Fr(0)), (Fr(0), Fr(0), Fr(1))]
    cons = []
    for q in min_nonelements(D):
        rep = cls[sum(a*b for a, b in zip(r, q)) % m]
        v = tuple(a - b for a, b in zip(q, rep)); cons.append(v)
        poly = clip(poly, v)
        if len(poly) < 3: return None, cons
    return (poly if area2(poly) > 0 else None), cons

def canon_shape(D):
    from itertools import permutations
    return min(tuple(sorted(tuple(x[s[i]] for i in range(3)) for x in D)) for s in permutations(range(3)))

if __name__ == '__main__':
    m0, m1 = int(sys.argv[1]), int(sys.argv[2])
    for m in range(m0, m1 + 1):
        t0 = time.time(); npp = 0; neg = []
        for layers in plane_partitions_nt(m):
            npp += 1
            D = cells(layers)
            d = H_of(D) - (m - 1)
            if d < 0: neg.append((d, D))
        t1 = time.time()
        # dedupe by symmetry
        seen = {}
        for d, D in neg:
            c = canon_shape(D)
            if c not in seen: seen[c] = (d, D)
        real = []
        for c, (d, D) in seen.items():
            rs = injective_rs(D, m)
            good = []
            for r in rs:
                poly, cons = open_cone(D, m, r)
                if poly is not None: good.append(r)
            if good: real.append((d, sorted(D), good))
        print(f'm={m}: non-two-face down-sets {npp}, delta<0 {len(neg)} ({len(seen)} up to S3); '
              f'realizable as e=4 tiles: {len(real)} shapes  [{t1-t0:.0f}s + {time.time()-t1:.0f}s]', flush=True)
        for d, D, good in real:
            print('   REAL delta', d, 'D', D, '#r', len(good), 'r e.g.', good[:4], flush=True)
