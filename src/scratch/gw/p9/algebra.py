"""Exact algebra and cyclic short-arc audits; fejer only."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd
import json
from p18 import floor_sum


def short_arc():
    sets = pairs = proper = 0
    for n in range(3, 15):
        width = (n - 1) // 2
        full = (1 << n) - 1
        for mask in range(1 << width):
            C = [0] + [j for j in range(1, width + 1) if mask & (1 << (j - 1))]
            if gcd(n, *C) != 1:
                continue
            sets += 1
            for X in range(1, full + 1):
                pairs += 1
                total = 0
                for c in C:
                    total |= ((X << c) | (X >> (n - c))) & full if c else X
                if total != full:
                    proper += 1
                    assert total.bit_count() >= X.bit_count() + len(C) - 1, (n, C, X)
    return dict(sets=sets, pairs=pairs, proper=proper)


def main():
    cases = 0
    for q in range(4, 100001):
        for rhozero in [False, True]:
            n = q - (2 if rhozero else 3)
            A = F(n) + F(floor_sum(n, 3), 2)
            target = F(q * (q if rhozero else q - 1), 12)
            # Difference is increasing in k and s; k=2, s=3 is the minimum.
            diff = 2 + (2 if rhozero else 3) - q + 3 * (A - target)
            assert diff >= 0, (q, rhozero, diff)
            cases += 1
    # Explicit polynomial shifts, checked coefficient-by-coefficient with interpolation.
    poly = {
        'p47': lambda z: (47 + z)**3 - 47 * (47 + z)**2 + 48 * (47 + z) - 24,
        'p17': lambda z: 27 * (17 + z)**3 - 485 * (17 + z)**2 + 458 * (17 + z) - 256,
        'x31': lambda z: 5 * (31 + z)**2 - 150 * (31 + z) - 91,
    }
    expected = {'p47': [2232, 2257, 94, 1], 'p17': [16, 7377, 892, 27], 'x31': [64, 160, 5]}
    for key, f in poly.items():
        for z in range(101):
            assert f(z) == sum(a * z**i for i, a in enumerate(expected[key]))
    # The block-sum identity is exact for every nonnegative integer n and j.
    blocks = 0
    for j in range(2, 101):
        for n in range(1001):
            b = n % j
            lhs = n + floor_sum(n, j)
            rhs = F(n * (n + j) + b * (j - b), 2 * j)
            assert lhs == rhs
            blocks += 1
    print(json.dumps(dict(quadratic_cases=cases, block_cases=blocks,
                         polynomials=expected, short_arc=short_arc()), indent=2))


if __name__ == '__main__':
    main()
