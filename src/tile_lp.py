r"""Per-tile certificate for Wilf (e = 4), exact rational arithmetic.

For S = <m, p1, p2, p3> with grlex Apery tile D:  m*W + m(m-1) = Def(p) := sum_{(x,a)} (M(p) - p.t_a(x)),
M(p) = max_{x in D} p.x  (CH').  p lies in the closed Groebner cone C_D of D and p_a >= m+1.  Def is convex and
positively homogeneous, so
        min { Def(p) : p in C_D, p >= m+1 } = (m+1) * kappa_D,   kappa_D := min { Def(q) : q in C_D, q >= 1 }
                                             = min_{p in poly} Def(p) / min_a p_a       (poly = C_D ∩ simplex).
Hence  (m+1) kappa_D >= m(m-1)  ==>  Wilf for EVERY semigroup whose tile is D (all generator values).
On each cell of the arrangement {p.x = p.x' (x, x' maximal)} ∪ {p_a = p_b} ∪ edges(poly), Def(p)/min_a p_a is a
linear-fractional function, so the minimum is attained at a vertex of that arrangement inside poly; we enumerate them.
"""
from fractions import Fraction as Fr
from itertools import combinations

add = lambda x, i: x[:i] + (x[i] + 1,) + x[i+1:]


def tops_sum(D):
    T = [0, 0, 0]; n = 0
    for x in D:
        for a in range(3):
            t = x
            while add(t, a) in D: t = add(t, a)
            for k in range(3): T[k] += t[k]
    return T


def maximal(D):
    return [x for x in D if all(add(x, i) not in D for i in range(3))]


def line_through(P, Q):
    """coefficients v with v.p = 0 on the plane-line through P, Q (points of the simplex plane)."""
    # v = P x Q (cross product): v.P = v.Q = 0
    return (P[1]*Q[2] - P[2]*Q[1], P[2]*Q[0] - P[0]*Q[2], P[0]*Q[1] - P[1]*Q[0])


def intersect(v, w):
    """point on the simplex plane with v.p = w.p = 0 (None if parallel / off-plane)."""
    c = (v[1]*w[2] - v[2]*w[1], v[2]*w[0] - v[0]*w[2], v[0]*w[1] - v[1]*w[0])
    s = c[0] + c[1] + c[2]
    if s == 0: return None
    return tuple(Fr(ci) / s for ci in c)


def inside(poly, p):
    n = len(poly)
    # poly is convex, vertices in order; p inside iff on the same side of every edge as the centroid
    cen = tuple(sum(V[k] for V in poly) / n for k in range(3))
    for i in range(n):
        v = line_through(poly[i], poly[(i + 1) % n])
        sc = sum(a*b for a, b in zip(v, cen)); sp = sum(a*b for a, b in zip(v, p))
        if sc * sp < 0: return False
    return all(c >= 0 for c in p)


def kappa(D, poly):
    m = len(D); A = maximal(D); T = tops_sum(D)
    lines = []
    for x, y in combinations(A, 2):
        v = tuple(xi - yi for xi, yi in zip(x, y))
        if any(v): lines.append(v)
    lines += [(1, -1, 0), (1, 0, -1), (0, 1, -1)]
    n = len(poly)
    lines += [line_through(poly[i], poly[(i + 1) % n]) for i in range(n)]
    cands = list(poly)
    for v, w in combinations(lines, 2):
        p = intersect(v, w)
        if p is not None and inside(poly, p): cands.append(p)
    best = None
    for p in cands:
        mn = min(p)
        if mn <= 0: continue
        Mx = max(sum(a*b for a, b in zip(p, x)) for x in A)
        val = (3*m*Mx - sum(a*b for a, b in zip(p, T))) / mn
        if best is None or val < best[0]: best = (val, p)
    return best


def wilf_certified(D, poly):
    m = len(D); k = kappa(D, poly)
    return (m + 1) * k[0] >= m*(m - 1), k
