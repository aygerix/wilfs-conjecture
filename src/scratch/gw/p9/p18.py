"""Exact P18 arithmetic. Run computations on fejer only."""
from heapq import heappush, heappop
from math import gcd


def apery(m, offsets):
    offsets = tuple(sorted(offsets))
    assert 0 < offsets[0] and offsets[-1] < m
    assert gcd(m, *offsets) == 1
    inf = (m + offsets[-1]) * m + 1
    ap = [inf] * m
    ap[0] = 0
    todo = [(0, 0)]
    while todo:
        w, r = heappop(todo)
        if w != ap[r]:
            continue
        for b in offsets:
            s = (r + b) % m
            z = w + m + b
            if z < ap[s]:
                ap[s] = z
                heappush(todo, (z, s))
    assert max(ap) < inf
    return ap


def profile(m, offsets):
    offsets = tuple(sorted(offsets))
    ap = apery(m, offsets)
    c = max(ap) - m + 1
    q = (c + m - 1) // m
    rho = q * m - c
    x = [w // m for w in ap]
    theta = [sum(z <= t for z in x[1:]) for t in range(q + 1)]
    ell = c - sum(x)
    k = len(offsets)
    B = (0,) + offsets
    sums2 = {a + b for a in B for b in B}
    s2 = sum(z < m for z in sums2)
    offset_gcd = gcd(*offsets)
    return dict(m=m, A=list(offsets), k=k, beta=offsets[-1],
                offset_gcd=offset_gcd, normalized_span=offsets[-1] // offset_gcd, c=c, q=q,
                rho=rho, ell=ell, W=(k + 1) * ell - c, theta=theta,
                s2=s2, s2_integer=len(sums2), s2_cyclic=len({z % m for z in sums2}),
                nowrap_possible=(offsets[0] == 1))


def floor_sum(n, step):
    """sum_{i=0}^{n-1} floor(i/step), with n <= 0 interpreted as zero."""
    if n <= 0:
        return 0
    a, b = divmod(n, step)
    return step * a * (a - 1) // 2 + a * b


def expanded_bound(p, prime=False):
    """Two-layer block growth using C=R2's explicit subset 2B below m."""
    k, q, rho, s = (p[a] for a in ('k', 'q', 'rho', 's2'))
    delta = s - 1 if prime else (s + 1) // 2
    low = [0, k] + [s - 1 + delta * ((t - 2) // 3) for t in range(2, q)]
    krho = sum(b < p['m'] - rho for b in p['A'])
    return q + sum(low[1:q-1]) + max(krho, low[q-1] - rho)


def erdos_turan(p):
    """An integer Sidon set, for an odd prime p; no primality assertion here."""
    return [2 * p * i + (i * i % p) for i in range(p)]


def isprime(n):
    return n >= 2 and all(n % a for a in range(2, __import__('math').isqrt(n) + 1))
