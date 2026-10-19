"""Adversarial carried P18, checking candidates after each mutation. Fejer only."""
import argparse, json, math, random
from collections import Counter
from audit import inspect, old_bound, yz_multi
from modulus import by_modulus, certificate
from p18 import profile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=911)
    ap.add_argument('--chains', type=int, default=80)
    ap.add_argument('--steps', type=int, default=100)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    count, failures, examples = Counter(), {}, []
    best = None
    for chain in range(a.chains):
        m = rng.randint(120, 1600)
        k = rng.randint(4, min(28, m // 8))
        mode = chain % 4
        if mode == 0:
            A = rng.sample(range(2, min(m, max(k + 4, m // 5))), k)
        elif mode == 1:
            d = rng.randint(2, max(3, m // (2 * k)))
            A = [1 + d * i for i in range(k)]
            A[-1] = rng.randint(2, m - 1)
        elif mode == 2:
            u, v = rng.randrange(1, m), rng.randrange(1, m)
            C = {(i*u+j*v) % m for i in range(8) for j in range(8)} - {0}
            if len(C) < k:
                continue
            A = rng.sample(sorted(C), k)
        else:
            A = rng.sample(range(2, m), k)
        A = sorted(set(A))
        if len(A) != k or math.gcd(m, *A) != 1:
            continue
        p = profile(m, A)
        score = p['W'] / p['c']
        for step in range(a.steps):
            C = A.copy()
            at = rng.randrange(k)
            C[at] = rng.randrange(1, m) if rng.random() < .3 else max(1, min(m-1, C[at] + rng.randint(-12, 12)))
            C = sorted(set(C))
            if len(C) != k or math.gcd(m, *C) != 1:
                continue
            inspect(m, C, count, failures, examples)
            z = profile(m, C)
            val = z['W'] / z['c']
            if z['q'] >= 4 and C[0] > 1 and (best is None or val < best['W'] / best['c']):
                best = dict(z, yz_multi=yz_multi(z), old_lkyz=old_bound(z))
            temp = .03 * (1 - step / a.steps)
            if val < score or rng.random() < math.exp(min(0, (score - val) / max(.0001, temp))):
                A, p, score = C, z, val
    print(json.dumps(dict(counts=dict(count), failures=failures, examples=examples, best=best), indent=2))


if __name__ == '__main__':
    main()
