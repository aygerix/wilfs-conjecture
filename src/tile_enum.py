r"""Complete enumeration of 3-D Apery tiles (e = 4) for a given multiplicity m.

For S = <m, p1, p2, p3> the grlex Apery factorization tile D depends only on
  * the lattice  Lam_r = {x in Z^3 : r.x = 0 mod m},  r = (p1, p2, p3) mod m,  and
  * the Groebner cone of the weight vector p: D(p) = {min-weight representative of each class of Z^3/Lam_r},
    ties broken by grlex (a tie-break is the limit of an open neighbouring cone, so only open cones matter).
For fixed r the positive weight space (the simplex p1 + p2 + p3 = 1, p > 0) is partitioned into finitely many open
Groebner cones; the cone of D is {p : p.(q - rep(q)) > 0 for every minimal non-element q of D} (reduced Groebner basis
binomials x^q - x^rep(q)).  We traverse this fan by flipping across facets, starting from p = (1,1,1).  Every tile of
every e = 4 semigroup with multiplicity m (and residues r) is found (assuming the standard facts above).

D(p) is computed by Dijkstra on Z/m with edge weights p_a (exact Fractions), tie-break by grlex on exponent vectors.

usage:  python3 src/tile_enum.py m            -> prints counts; use enumerate_tiles(m) from other scripts.
"""
import sys, heapq
from fractions import Fraction as Fr
from math import gcd
from itertools import permutations


def tile_for_weight(m, r, p):
    """grlex-tie-broken min-weight representatives of Z^3 / Lam_r, weight p (Fractions/ints). Returns dict cls -> x."""
    best = {0: (0, (0, 0, 0))}
    key = lambda w, x: (w, sum(x), x)                       # weight, then grlex (degree, then lex)
    heap = [(key(0, (0, 0, 0)), 0)]
    done = {}
    while heap:
        k, g = heapq.heappop(heap)
        if g in done: continue
        w, _, x = k
        done[g] = x
        for a in range(3):
            y = x[:a] + (x[a] + 1,) + x[a+1:]
            h = (g + r[a]) % m
            if h in done: continue
            k2 = key(w + p[a], y)
            if h not in best or k2 < key(*best[h]):
                best[h] = (w + p[a], y)
                heapq.heappush(heap, (k2, h))
    return done


def min_nonelements(D):
    cand = {x[:a] + (x[a] + 1,) + x[a+1:] for x in D for a in range(3)} - D
    return [q for q in cand if all(q[a] == 0 or q[:a] + (q[a] - 1,) + q[a+1:] in D for a in range(3))]


def cone_constraints(m, r, D):
    """vectors v with cone = {p : p.v > 0}."""
    cls = {sum(ri*xi for ri, xi in zip(r, x)) % m: x for x in D}
    out = []
    for q in min_nonelements(D):
        rep = cls[sum(ri*qi for ri, qi in zip(r, q)) % m]
        out.append(tuple(qi - ri for qi, ri in zip(q, rep)))
    return out


def clip(poly, v):
    """clip convex polygon (list of 3-vectors of Fractions on the plane sum=1) by p.v >= 0."""
    dot = lambda p: sum(pi*vi for pi, vi in zip(p, v))
    out = []
    n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        dp, dq = dot(P), dot(Q)
        if dp >= 0: out.append(P)
        if (dp > 0 and dq < 0) or (dp < 0 and dq > 0):
            t = dp / (dp - dq)
            out.append(tuple(Pi + t*(Qi - Pi) for Pi, Qi in zip(P, Q)))
    # remove duplicates
    res = []
    for P in out:
        if not res or res[-1] != P: res.append(P)
    if len(res) > 1 and res[0] == res[-1]: res.pop()
    return res


SIMPLEX = [(Fr(1), Fr(0), Fr(0)), (Fr(0), Fr(1), Fr(0)), (Fr(0), Fr(0), Fr(1))]


def cone_polygon(cons):
    poly = list(SIMPLEX)
    for v in cons:
        poly = clip(poly, v)
        if len(poly) < 3: return poly
    return poly


def on_closure(poly, cons, pt):
    """pt in the closed cone {p.v >= 0}."""
    return all(sum(a*b for a, b in zip(pt, v)) >= 0 for v in cons)


def enumerate_lattice(m, r, eps=Fr(1, 10**6), maxcones=100000):
    """all tiles (as frozensets) of Lam_r arising from positive weights.  Flip traversal; each flip is verified to land
    in a cone whose closure contains the facet midpoint (eps is halved until it does)."""
    start = (Fr(1, 3) + Fr(1, 997), Fr(1, 3) + Fr(1, 1999), Fr(1, 3) - Fr(1, 997) - Fr(1, 1999))
    seen = {}
    D0 = frozenset(tile_for_weight(m, r, start).values())
    todo = [D0]
    cache = {}
    while todo:
        D = todo.pop()
        if D in seen: continue
        cons = cone_constraints(m, r, D)
        poly = cone_polygon(cons)
        assert len(poly) >= 3, (m, r, sorted(D))
        seen[D] = poly
        if len(seen) > maxcones: raise RuntimeError('too many cones')
        n = len(poly)
        cen = tuple(sum(V[k] for V in poly) / n for k in range(3))
        for i in range(n):
            P, Q = poly[i], poly[(i + 1) % n]
            mid = tuple((Pi + Qi) / 2 for Pi, Qi in zip(P, Q))
            if any(c == 0 for c in mid): continue                # boundary of the positive simplex
            e = eps
            while True:
                out = tuple(mi + e*(mi - ci) for mi, ci in zip(mid, cen))
                if any(c <= 0 for c in out): break
                D2 = frozenset(tile_for_weight(m, r, out).values())
                if D2 == D: e *= 2; continue                      # still inside (should not happen)
                cons2 = cache.get(D2) or cone_constraints(m, r, D2); cache[D2] = cons2
                if on_closure(None, cons2, mid):
                    todo.append(D2); break
                e /= 2
                if e < Fr(1, 10**40): raise RuntimeError('flip failed')
    return seen


def canonical_residues(m):
    """one residue vector per lattice up to units and coordinate permutations; residues nonzero and distinct."""
    units = [u for u in range(1, m) if gcd(u, m) == 1]
    reps = set()
    for r1 in range(1, m):
        for r2 in range(1, m):
            for r3 in range(1, m):
                if len({r1, r2, r3}) < 3 or gcd(gcd(gcd(r1, r2), r3), m) != 1: continue
                r = (r1, r2, r3)
                c = min(tuple(sorted((u*x) % m for x in r)) for u in units)
                reps.add(c)
    return sorted(reps)


def enumerate_tiles(m, verbose=False):
    """yield (r, D, poly) for all lattices (canonical up to units and coordinate permutation) and all their tiles."""
    for r in canonical_residues(m):
        tiles = enumerate_lattice(m, r)
        if verbose: print(r, len(tiles), flush=True)
        for D, poly in tiles.items():
            yield r, D, poly


if __name__ == '__main__':
    m = int(sys.argv[1])
    nl = 0; nt = 0
    for r in canonical_residues(m):
        T = enumerate_lattice(m, r); nl += 1; nt += len(T)
    print(f'm={m}: lattices {nl}, tiles {nt}')
