"""Carried Sidon stress examples, including the analytic infinite family."""
import json
from fractions import Fraction
from p18 import erdos_turan, profile
from audit import old_bound, yz_multi, inspect
from modulus import certificate, by_modulus
from collections import Counter


def main():
    counts, failures, examples = Counter(), {}, []
    for prime in [17, 19, 23, 31, 47, 67, 97]:
        B = erdos_turan(prime)
        beta = B[-1]
        for ratio in [Fraction(1), Fraction(6, 5), Fraction(3, 2), Fraction(2), Fraction(31), Fraction(100)]:
            m = beta * ratio.numerator // ratio.denominator + 1
            inspect(m, B[1:], counts, failures, examples)
            z = profile(m, B[1:])
            z['p'] = prime
            z['ratio'] = str(ratio)
            z['old_lkyz'] = old_bound(z)
            z['yz_multi'] = yz_multi(z)
            z['span12'] = 12 * beta <= prime * z['s2']
            z['quadratic'] = certificate(m, B[1:])
            Ndata = by_modulus(m, B[1:])
            z['Ndata'] = {k: Ndata[k] for k in ['N', 'D', 'lower']}
            print(json.dumps(z), flush=True)
    print(json.dumps(dict(counts=dict(counts), failures=failures)), flush=True)


if __name__ == '__main__':
    main()
