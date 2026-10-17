"""E5b: TOP_E / TOP_0 / Wilf on adversarial examples: Eliahou-Fromentin W0<0 semigroups,
large type (Backelin-like), Delgado-type deep families, random generator sets with large depth."""
import sys, random
sys.path.insert(0, 'src')
from ns import NS
from chains import chain_data

def nu(s, w, p):
    k = 0
    while w - (k + 1) * p >= 0 and (w - (k + 1) * p) in s:
        k += 1
    return k

def top_test(s):
    m, c = s.m, s.c
    Pp = [p for p in s.P if p != m]
    d = len(Pp)
    Xq = [w for w in s.apery() if w >= c]
    lhs2 = 2 * sum((u - c + 1) * sum(nu(s, u, p) + 1 for p in Pp) for u in Xq)
    rhs0 = m * ((d + 1) * m + d - 1)
    E = chain_data(s)['E']
    return lhs2 <= rhs0 + 2 * E, lhs2 <= rhs0, (rhs0 + 2 * E - lhs2) // 2

def with_conductor(gens, c):
    """<gens> union [c, oo)"""
    base = NS.from_generators(list(gens) + list(range(c, c + min(gens))))
    return base

if __name__ == '__main__':
    tests = []
    # Eliahou-Fromentin / Fromentin W0 < 0 examples: <A>_c = <A> u [c,oo)
    for gens, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68),
                    ((18, 28, 29), 72), ((30, 44, 48, 49), 118), ((23, 39, 40, 42), 77)]:
        tests.append(('W0<0 ' + str(gens) + '_' + str(c), with_conductor(gens, c)))
    tests.append(('Backelin t=14', NS.from_generators([213, 216, 226, 227])))
    # Delgado-type S(p) = <mu, gamma, gamma+1>_{p mu}
    for mu, gam, p in [(10, 13, 5), (12, 17, 6), (15, 19, 7), (20, 27, 8)]:
        tests.append((f'Delgado <{mu},{gam},{gam+1}>_{p*mu}', with_conductor((mu, gam, gam + 1), p * mu)))
    # random: m in [20,40], few generators, large depth
    rng = random.Random(12345)
    for _ in range(300):
        m = rng.randint(15, 45)
        k = rng.randint(2, 5)
        gens = sorted(set([m] + [rng.randint(m + 1, 4 * m) for _ in range(k)]))
        from math import gcd
        from functools import reduce
        if reduce(gcd, gens) != 1:
            continue
        s = NS.from_generators(gens)
        tests.append(('rand ' + str(gens), s))
        # truncations <gens> u [c', oo) at a few c' (adversarial: cut conductor)
        for frac in (0.5, 0.7, 0.85):
            cc = int(s.c * frac)
            if cc > 3 * m:
                tests.append((f'rand {gens}_{cc}', with_conductor(gens, cc)))
    nE = n0 = 0
    for name, s in tests:
        okE, ok0, slack = top_test(s)
        if not okE:
            nE += 1
            print('TOP_E FAIL', name, s.summary(), slack)
        if not ok0:
            n0 += 1
        if s.W < 0:
            print('WILF COUNTEREXAMPLE?!', name, s.summary())
        if name.startswith(('W0', 'Backelin', 'Delgado')):
            print(f'{name}: m={s.m} e={s.e} c={s.c} q={s.q} W={s.W} TOP_E={okE} TOP_0={ok0} slackE={slack}')
    print(f'{len(tests)} tests; TOP_E fails {nE}; TOP_0 fails {n0}')
