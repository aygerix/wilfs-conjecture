"""Early falsification and exact checks. Fejer only, one core."""
import argparse, itertools, json, math, random
from p18 import profile, expanded_bound, isprime, erdos_turan


def examine(p, out):
    q, th, s, k = p['q'], p['theta'], p['s2'], p['k']
    if q < 4:
        return
    assert p['ell'] >= expanded_bound(p, isprime(p['m'])), p
    assert p['m'] <= q * p['beta'] + 1, p
    if p['rho']:
        assert p['m'] <= (q - 1) * p['beta'] + 1, p
    if 12 * p['beta'] <= (k + 1) * s:
        assert p['W'] >= 0, p
        out['span12'] += 1
    for t in range(q - 3):
        # Candidate stronger composite growth (valid for prime m).
        if th[t + 3] < th[t] + s - 1:
            old = out['failures'].get('unperiodized')
            key = (p['m'], k, p['A'], t)
            if old is None or key < (old['m'], old['k'], old['A'], old['t']):
                out['failures']['unperiodized'] = dict(p, t=t)
        if 4 * (p['ell'] - q) < s * q * (q - 1):
            old = out['failures'].get('quadratic4')
            if old is None or (p['m'], k, p['A']) < (old['m'], old['k'], old['A']):
                out['failures']['quadratic4'] = p
    out['q4plus'] += 1
    out['total'] += 1


def main():
    pa = argparse.ArgumentParser()
    pa.add_argument('--maxm', type=int, default=20)
    pa.add_argument('--trials', type=int, default=10000)
    pa.add_argument('--seed', type=int, default=901)
    args = pa.parse_args()
    rng = random.Random(args.seed)
    out = dict(total=0, q4plus=0, span12=0, failures={})
    for m in range(3, args.maxm + 1):
        for k in range(1, min(5, m)):
            for A in itertools.combinations(range(1, m), k):
                if math.gcd(m, *A) == 1:
                    examine(profile(m, A), out)
    for z in range(args.trials):
        m = rng.randint(30, 1000)
        k = rng.randint(2, min(35, m - 1))
        mode = z % 4
        if mode == 0:
            A = rng.sample(range(1, m), k)
        elif mode == 1:
            beta = rng.randint(k, min(m - 1, max(k, 8 * k * k)))
            A = rng.sample(range(1, beta + 1), k)
        elif mode == 2:
            step = rng.randint(1, max(1, (m - 1) // (k + 3)))
            A = {1 + j * step for j in range(k - 1)}
            A.add(rng.randrange(1, m))
            if len(A) != k:
                continue
        else:
            a, b = rng.randrange(1, m), rng.randrange(1, m)
            A = {(i * a + j * b) % m for i in range(5) for j in range(5)} - {0}
            if len(A) < k:
                continue
            A = rng.sample(sorted(A), k)
        if math.gcd(m, *A) == 1:
            examine(profile(m, A), out)
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
