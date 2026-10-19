"""Check the analytic P9 statements on actual P18, not count relaxations.

All computation must run on fejer, with a single nice process.
"""
import argparse
import itertools
import json
import math
import random
from collections import Counter
from p18 import apery, profile, expanded_bound, isprime
from modulus import by_modulus, certificate, higher_certificate, sumset


def old_bound(p):
    k, q, rho, m = (p[a] for a in ('k', 'q', 'rho', 'm'))
    if q < 3:
        return 0
    d = k if isprime(m) else (k + 2) // 2
    kr = sum(a < m - rho for a in p['A'])
    return q + (q - 2) * k + d * ((q - 3) ** 2 // 4) + max(kr, k + d * ((q - 2) // 2) - rho)


def yz_multi(p):
    e, q, m, th = p['k'] + 1, p['q'], p['m'], p['theta']
    for Q in range(4, q + 1):
        for t in range(1, Q - 1):
            if e * ((Q - t - 1) * th[t] + Q) >= Q * m:
                return True
        if p['rho'] == 0:
            for t in range(1, Q):
                if e * ((Q - t) * th[t] + Q) >= Q * m:
                    return True
    return False


def inspect(m, A, count, failures, examples, secondary=True):
    if math.gcd(m, *A) != 1:
        return
    p = profile(m, A)
    count['all'] += 1
    k, q, s, beta, rho = (p[a] for a in ('k', 'q', 's2', 'beta', 'rho'))
    e = k + 1
    span = p['normalized_span']
    assert p['W'] >= 0, p
    # An independent membership table on the small exhaustive domain.
    if m <= 18:
        c = p['c']
        member = bytearray(c + m + 1)
        member[0] = 1
        for z in range(1, len(member)):
            member[z] = any(z >= a and member[z - a] for a in [m] + [m + b for b in A])
        assert sum(member[:c]) == p['ell'], p
        assert member[c - 1] == 0 and all(member[c:c+m]), p
        count['membership_crosscheck'] += 1
    assert p['c'] >= m * ((m - 2) // span + 1) + (p['offset_gcd'] - 1) * (m - 1), p
    if rho:
        assert m <= (q - 1) * span + 1, p
    if q >= 4:
        count['q4plus'] += 1
        th = p['theta']
        assert th[2] + 1 == s, p
        for H in range(q - 3):
            gain = th[H + 3] - th[H]
            assert gain >= (s + 1) // 2, dict(p, H=H)
            if isprime(m) or m > 4 * beta:
                assert gain >= s - 1, dict(p, H=H)
            if gain < s - 1:
                key = (m, k, list(A), H)
                old = failures.get('unperiodized')
                if old is None or key < (old['m'], old['k'], old['A'], old['H']):
                    failures['unperiodized'] = dict(p, H=H)
            count['step3_checks'] += 1
        assert p['ell'] >= expanded_bound(p, isprime(m)), p
        if k >= 2:
            target = s * q * (q - 1 if rho else q)
            assert 12 * (p['ell'] - q) >= target, p
            count['quadratic12_checks'] += 1
            if 4 * (p['ell'] - q) < s * q * (q - 1):
                old = failures.get('quadratic4_kge2')
                if old is None or (m, k, list(A)) < (old['m'], old['k'], old['A']):
                    failures['quadratic4_kge2'] = p
        if 12 * span <= e * s:
            assert p['W'] >= k * q + rho, p
            count['span12'] += 1
            if q == 4:
                count['span12_q4'] += 1
        if e * old_bound(p) < p['c'] and e * (k + 2) < 2 * m and 3 * e < m and e > 4 and p['A'][0] > 1:
            count['outside_list'] += 1
            if 12 * span <= e * s:
                count['span12_outside'] += 1
                if len(examples) < 12:
                    examples.append(dict(p, criterion='span12', yz_multi=yz_multi(p)))
    if secondary:
        z = by_modulus(m, A)
        assert z['ell'] == p['ell'] and z['c'] == p['c'], (p, z)
        assert z['R'][0] == e, (p, z)
        assert z['R'][1] >= z['s'] if len(z['R']) >= 2 else True, (p, z)
        D, R = z['D'], z['R']
        for H in range(D - 2):
            assert R[H + 2] - R[H] >= z['delta'], (p, z, H)
            if R[H + 2] - R[H] < z['s'] - 1:
                old = failures.get('modulus_unperiodized')
                if old is None or (m, k, list(A), H) < (old['m'], old['k'], old['A'], old['H']):
                    failures['modulus_unperiodized'] = dict(p, H=H, modulus=z)
            count['modulus_step_checks'] += 1
        if D >= 2:
            assert p['ell'] >= z['lower'], (p, z)
            if m > 3 * beta:
                lb = e + D - 2 + (z['s'] - 1) * ((D - 1) ** 2 // 4)
                assert p['ell'] >= lb, (p, z)
                count['modulus_closed_checks'] += 1
        if certificate(m, A):
            assert p['W'] >= e * (e + D - 2), (p, z)
            count['modulus_quadratic'] += 1
        for j in [2, 3, 4]:
            if m <= (2 * j - 1) * beta:
                continue
            sh, cq, cl = higher_certificate(m, A, j)
            assert R[j - 1] >= sh, (p, z, j)
            for H in range(D - j):
                assert R[H + j] - R[H] >= sh - 1, (p, z, j, H)
                count['higher_step_checks'] += 1
            n = D - j
            assert n >= 0
            rr, bb = divmod(n, j)
            F = j * rr * (rr - 1) // 2 + rr * bb
            exact_lb = e + n + (sh - 1) * (n + F)
            assert p['ell'] >= exact_lb, (p, z, j)
            count['higher_closed_checks'] += 1
            if cq:
                assert p['W'] >= e * (e + D - j), (p, z, j)
                count['higher_quadratic'] += 1
            if cl:
                count['higher_linear'] += 1
        count['modulus_crosscheck'] += 1


def main():
    pa = argparse.ArgumentParser()
    pa.add_argument('--maxm', type=int, default=18)
    pa.add_argument('--trials', type=int, default=10000)
    pa.add_argument('--seed', type=int, default=909)
    a = pa.parse_args()
    rng = random.Random(a.seed)
    count, failures, examples = Counter(), {}, []
    for m in range(2, a.maxm + 1):
        for mask in range(1, 1 << (m - 1)):
            A = [b for b in range(1, m) if mask & (1 << (b - 1))]
            inspect(m, A, count, failures, examples, secondary=(m <= 14))
    for i in range(a.trials):
        m = rng.randint(30, 1800)
        k = rng.randint(2, min(55, m - 1))
        mode = i % 5
        if mode == 0:
            A = rng.sample(range(1, m), k)
        elif mode == 1:
            beta = rng.randint(k, min(m - 1, max(k, 3 * k * k)))
            A = rng.sample(range(1, beta + 1), k)
        elif mode == 2:
            start = rng.randint(1, max(1, m - k))
            step = rng.randint(1, max(1, (m - 1 - start) // max(1, k - 2)))
            A = {start + j * step for j in range(k - 1)}
            A.add(rng.randrange(1, m))
            if len(A) != k or max(A) >= m:
                continue
        elif mode == 3:
            u, v = rng.randrange(1, m), rng.randrange(1, m)
            pts = {(j * u + h * v) % m for j in range(8) for h in range(8)} - {0}
            if len(pts) < k:
                continue
            A = rng.sample(sorted(pts), k)
        else:
            beta = rng.randint(k, m - 1)
            A = rng.sample(range(max(1, beta - 3 * k * k), beta + 1), k)
        inspect(m, sorted(A), count, failures, examples, secondary=True)
    print(json.dumps(dict(counts=dict(count), failures=failures, examples=examples), indent=2))


if __name__ == '__main__':
    main()
