"""Largest-generator modulus certificates. Exact integer arithmetic, fejer only."""
def by_modulus(m, A):
    from heapq import heappop, heappush
    beta = max(A)
    n = m + beta
    generators = [m] + [m + b for b in A if b != beta]
    inf = n * n + 1
    ap = [inf] * n
    ap[0] = 0
    todo = [(0, 0)]
    while todo:
        w, r = heappop(todo)
        if ap[r] != w:
            continue
        for a in generators:
            s = (r + a) % n
            z = w + a
            if z < ap[s]:
                ap[s] = z
                heappush(todo, (z, s))
    assert max(ap) < inf
    c = max(ap) - n + 1
    D = (c + n - 1) // n
    rho = D * n - c
    ell = c - sum(w // n for w in ap)
    R = [sum(w // n <= H for w in ap) for H in range(D + 1)]
    s = len({a + b for a in [0] + list(A) for b in [0] + list(A)})
    delta = s - 1 if m > 3 * beta else (s + 1) // 2
    low = [len(A) + 1] + [s + delta * ((H - 1) // 2) for H in range(1, D)]
    lower = sum(low[:D-1]) + max(0, low[D-1] - rho) if D >= 2 else 0
    return dict(N=n, D=D, rhoN=rho, ell=ell, R=R, s=s,
                delta=delta, lower=lower, c=c)


def certificate(m, A):
    """The exact quadratic sufficient criterion, requiring m > 3 beta."""
    from math import gcd
    beta = max(A)
    span = beta // gcd(*A)
    e = len(A) + 1
    s = len({a + b for a in [0] + list(A) for b in [0] + list(A)})
    T = e * (s - 1)
    n = m + beta
    return m > 3 * beta and T * (m * (m - 1) - 2 * span * n) >= 4 * span * n * n


def sumset(B, j):
    C = {0}
    for _ in range(j):
        C = {a + b for a in C for b in B}
    return C


def higher_certificate(m, A, j):
    from math import gcd
    beta = max(A)
    span = beta // gcd(*A)
    e = len(A) + 1
    s = len(sumset([0] + list(A), j))
    T = e * (s - 1)
    n = m + beta
    quadratic = m > (2 * j - 1) * beta and T * (m * (m - 1) - j * span * n) >= 2 * j * span * n * n
    linear = T > 2 * j * span and m * (T - 2 * j * span) >= 2 * j * beta * (T + 3 * span)
    assert not linear or quadratic
    return s, quadratic, linear
