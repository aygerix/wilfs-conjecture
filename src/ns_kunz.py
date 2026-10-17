"""Implementation B (independent of ns.py): everything from the Apery set computed by
Dijkstra on residues mod m, invariants via Selmer/Kunz formulas, minimal generators via the
Apery poset.  Used to cross-check implementation A.

  g = sum_i (w_i - i)/m            (Selmer)
  F = max_i w_i - m,  c = F + 1    (Brauer-Shockley)
  P = {m} U {w_i != 0 minimal in (Ap, <=_S)}
"""
import heapq
from math import gcd
from functools import reduce


def apery_dijkstra(gens):
    gens = sorted(set(gens))
    assert reduce(gcd, gens) == 1
    m = gens[0]
    dist = [None] * m
    dist[0] = 0
    pq = [(0, 0)]
    done = [False] * m
    while pq:
        d, r = heapq.heappop(pq)
        if done[r]:
            continue
        done[r] = True
        for a in gens[1:]:
            r2 = (r + a) % m
            nd = d + a
            if dist[r2] is None or nd < dist[r2]:
                dist[r2] = nd
                heapq.heappush(pq, (nd, r2))
    return dist


def invariants_from_apery(ap):
    m = len(ap)
    if m == 1:
        return dict(m=1, e=1, c=0, g=0, ell=0, W=0, P=[1])
    g = sum((w - i) // m for i, w in enumerate(ap))
    c = max(ap) - m + 1
    ell = c - g
    apset = set(ap)
    nz = sorted(w for w in ap if w)
    # w is decomposable in the Apery poset iff w = u + v with u, v nonzero in Ap
    minimal = []
    for w in nz:
        if not any((w - u) in apset and (w - u) > 0 for u in nz if u < w):
            minimal.append(w)
    e = 1 + len(minimal)
    return dict(m=m, e=e, c=c, g=g, ell=ell, W=e * ell - c, P=[m] + minimal)


def invariants(gens):
    return invariants_from_apery(apery_dijkstra(gens))


def apery_from_kunz(x):
    m = len(x) + 1
    return [0] + [m * x[i - 1] + i for i in range(1, m)]


def is_kunz(x):
    """Kunz inequalities (integer, all x_i >= 1)."""
    m = len(x) + 1
    X = [0] + list(x)
    for i in range(1, m):
        if X[i] < 1:
            return False
        for j in range(i, m):
            k = i + j
            if k < m:
                if X[i] + X[j] < X[k]:
                    return False
            elif k > m:
                if X[i] + X[j] + 1 < X[k - m]:
                    return False
    return True
