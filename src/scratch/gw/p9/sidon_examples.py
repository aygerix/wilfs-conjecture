"""Exact witnesses for the span/doubling theorem. Fejer only."""
import json
from math import gcd
from p18 import erdos_turan, profile, isprime


def old_lkyz(p):
    k, q, rho, m = (p[a] for a in ('k', 'q', 'rho', 'm'))
    delta = k if isprime(m) else (k + 2) // 2
    krho = sum(b < m - rho for b in p['A'])
    return q + (q - 2) * k + delta * ((q - 3) ** 2 // 4) + max(
        krho, k + delta * ((q - 2) // 2) - rho)


def main():
    for p in [31, 47, 53, 67]:
        B = erdos_turan(p)
        beta = B[-1]
        assert len({a + b for i, a in enumerate(B) for b in B[i:]}) == p * (p + 1) // 2
        for mult in [2, 3, 4, 6, 8, 12]:
            m = mult * beta + 1
            z = profile(m, B[1:])
            z['p'] = p
            z['multiple'] = mult
            z['lkyz'] = old_lkyz(z)
            z['old_covered'] = z['q'] <= 3 or p <= 4 or 3 * p >= m or p * (p + 1) >= 2 * m or p * z['lkyz'] >= z['c']
            z['span12'] = 12 * beta <= p * z['s2']
            z['span8'] = 8 * beta <= p * (z['s2'] - 1) and m > 6 * beta + 1
            print(json.dumps(z), flush=True)


if __name__ == '__main__':
    main()
