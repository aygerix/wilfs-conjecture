# Independent toolkit (referee) for e = 4 semigroups and their factorization tiles.
# Written from the definitions only; does not import project code.
import heapq
from math import gcd
from functools import reduce
from itertools import combinations

def apery(m, gens):
    """Ap(S,m)[i] = least element of S=<m,gens> congruent to i mod m (Dijkstra on Z/m)."""
    INF = float('inf'); dist = [INF]*m; dist[0] = 0; hp = [(0, 0)]
    while hp:
        d, g = heapq.heappop(hp)
        if d > dist[g]: continue
        for p in gens:
            h = (g + p) % m; nd = d + p
            if nd < dist[h]: dist[h] = nd; heapq.heappush(hp, (nd, h))
    return dist

def invariants(m, gens):
    """returns dict with Ap, c, g, ell, minimal gens P' (sorted), e, W (S = <m, gens>, gcd must be 1)."""
    assert reduce(gcd, [m] + list(gens)) == 1
    Ap = apery(m, gens)
    F = max(Ap) - m
    c = F + 1
    g = sum((Ap[i] - i)//m for i in range(m))
    # minimal generators: p in gens minimal iff p not in <m, gens \ {p}>  (also p != m, p > m)
    Pp = []
    for p in sorted(set(gens)):
        if p % m == 0: continue
        others = [q for q in gens if q != p]
        Ao = apery(m, others) if others else [0] + [float('inf')]*(m-1)
        if p < Ao[p % m]: Pp.append(p)
    e = 1 + len(Pp)
    ell = c - g
    return dict(Ap=Ap, c=c, g=g, ell=ell, P=Pp, e=e, W=e*ell - c, M=max(Ap))

def grlex_tile(m, P):
    """grlex-least factorizations over P (list of 3 gens) of the Apery elements: class -> x.
    Order: weight p.x, then degree |x|, then lexicographically smallest tuple."""
    best = {0: (0, 0, (0, 0, 0))}; done = {}
    hp = [((0, 0, (0, 0, 0)), 0)]
    while hp:
        k, g = heapq.heappop(hp)
        if g in done: continue
        done[g] = k
        w, deg, x = k
        for a in range(3):
            y = list(x); y[a] += 1; y = tuple(y)
            h = (g + P[a]) % m
            if h in done: continue
            k2 = (w + P[a], deg + 1, y)
            if h not in best or k2 < best[h]:
                best[h] = k2; heapq.heappush(hp, (k2, h))
    return {g: k[2] for g, k in done.items()}, {g: k[0] for g, k in done.items()}

E = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
def add(x, a, k=1):
    y = list(x); y[a] += k; return tuple(y)

def is_downset(D):
    return all(x[a] == 0 or add(x, a, -1) in D for x in D for a in range(3))

def heights(D):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, a)] + 1 for a in range(3) if add(x, a) in D], default=0)
    return ht

def tops(D):
    T = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        T[x] = tuple(T[add(x, a)][a] if add(x, a) in D else x for a in range(3))
    return T

def H_of(D):
    ht = heights(D); T = tops(D)
    return sum(ht[T[x][a]] for x in D for a in range(3))

def two_face_pairs(D):
    return [(a, b) for a, b in ((0, 1), (0, 2), (1, 2)) if add(add((0, 0, 0), a), b) not in D]

def min_nonelements(D):
    cand = {add(x, a) for x in D for a in range(3)} - D
    return [q for q in cand if all(q[a] == 0 or add(q, a, -1) in D for a in range(3))]

def proj(x, c):
    y = list(x); y[c] = 0; return tuple(y)

def classify(D):
    """returns ('C', None) if D = Cyl, ('cone', q) if D = Cyl \\ (q+N^3) with q >= (1,1,1), else ('other', ...)"""
    G = min_nonelements(D)
    full = [q for q in G if min(q) >= 1]
    # Cyl: x with proj_c(x) in D for all c
    # bounding box
    L = [max(x[a] for x in D) + 1 for a in range(3)]
    Cyl = set()
    for i in range(L[0] + 1):
        for j in range(L[1] + 1):
            for k in range(L[2] + 1):
                x = (i, j, k)
                if all(proj(x, c) in D for c in range(3)): Cyl.add(x)
    if not full:
        return ('C' if Cyl == D else 'other', None, full)
    if len(full) > 1: return ('other', None, full)
    q = full[0]
    D2 = {x for x in Cyl if not all(x[a] >= q[a] for a in range(3))}
    return ('cone' if D2 == D else 'other', q, full)

def face_corners(D, c):
    """number of outer corners (maximal elements) of the face D ∩ {x_c = 0} as a 2-D down-set."""
    F = [x for x in D if x[c] == 0]
    Fs = set(F)
    o = [a for a in range(3) if a != c]
    return sum(1 for x in F if all(add(x, a) not in Fs for a in o))

def counts(D):
    """t, Tri, qU, qO, h(x) table"""
    ht = heights(D); T = tops(D)
    Max = [x for x in D if ht[x] == 0]
    t = len(Max); Tri = qU = qO = 0
    for x in D:
        if ht[x] == 0: continue
        hs = [ht[T[x][a]] for a in range(3)]
        n = sum(1 for v in hs if v == 0); h = sum(hs)
        if n == 3: Tri += 1
        elif h == 1:
            assert n == 2
            c = [a for a in range(3) if hs[a] == 1][0]
            if T[x][c] == x: qU += 1
            else: qO += 1
    return t, Tri, qU, qO

def def_all(D, wmap, M):
    T = tops(D)
    return sum(M - wmap[T[x][a]] for x in D for a in range(3))
