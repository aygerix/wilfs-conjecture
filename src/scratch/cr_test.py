# CR (crude rearrangement, residue-free, any c): with T(y) = d + |y| over maximal cells y sorted decreasingly,
#   sum_i T_(i) (m-1-i) <= (d+1) m (m-1)/2   implies MaxCL for every sigma, hence Wilf.
import sys, random, time, itertools; sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def cr(s):
    Pp, best = factorizations_down_set(s, 'grlex'); d = len(Pp); D = set(best.values()); m = s.m
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    A = sorted((d + sum(y) for y in D if all(tuple(p + q for p, q in zip(y, u)) not in D for u in U)), reverse=True)
    lhs = sum(t * (m - 1 - i) for i, t in enumerate(A)); rhs = (d + 1) * m * (m - 1) / 2
    two = any(tuple(int(i in (a, b)) for i in range(d)) not in D for a in range(d) for b in range(a + 1, d))
    return lhs / rhs, two
if __name__ == '__main__':
    E0, E1, seed, budget, mmax, K = map(int, sys.argv[1:7]); rnd = random.Random(seed); t0 = time.time()
    n = 0; fails = {}; worst = {}
    while time.time() - t0 < budget:
        e = rnd.randint(E0, E1); m = rnd.randint(3 * e + 1, mmax)
        try: s = NS.from_generators([m] + rnd.sample(range(m + 1, K * m), e - 1))
        except ValueError: continue
        if s.e != e or s.c <= 3 * s.m: continue
        r, two = cr(s); n += 1
        if r > 1 + 1e-12: fails.setdefault((e, two), []).append((s.P, round(r, 4)))
        if (e, two) not in worst or r > worst[(e, two)][0]: worst[(e, two)] = (round(r, 4), s.P)
    print(f'e in [{E0},{E1}], c>3m, 3e<m, gens<{K}m, seed {seed}: {n} S; CR fails by (e, two-face): ' + str({k: len(v) for k, v in fails.items()}))
    for k in sorted(worst): print('  worst', k, worst[k], ' e.g. fail', fails.get(k, [None])[:2])
