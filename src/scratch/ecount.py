# E-count (Hall condition for the Load Lemma): for every nonempty Y subset of A (maximal cells of a tile D), E = down-closure of Y:
#    2 sum_{y in Y} (|y| - 1) <= (d+1) (|E| - |Y| - 1).
# Y = A is the count condition.  Exhaustive over tile shapes; also on adversarial Apery tiles (random subsets Y when |A| large).
import sys, itertools, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
def down(Y):
    E = set()
    for y in Y:
        for u in itertools.product(*[range(v + 1) for v in y]): E.add(u)
    return E
def ecount(A, d, subsets):
    worst = None
    for Y in subsets:
        if all(sum(y) <= 1 for y in Y): continue
        E = down(Y)
        v = (d+1)*(len(E) - len(Y) - 1) - 2*sum(sum(y) - 1 for y in Y)
        if worst is None or v < worst[0]: worst = (v, sorted(Y))
    return worst
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'exh':
        from exp_cl_tiling import downsets
        for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
            for m in range(3, mmax + 1):
                f = 0; n = 0; ex = None
                for D in downsets(m, d):
                    if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                    if not any(len({sum(i*j for i, j in zip(y, p)) % m for y in D}) == m for p in itertools.product(range(1, m), repeat=d)): continue
                    n += 1; S = set(D)
                    A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
                    subs = [Y for k in range(1, len(A) + 1) for Y in itertools.combinations(A, k)]
                    w = ecount(A, d, subs)
                    if w and w[0] < 0:
                        f += 1
                        if ex is None: ex = (sorted(D), w)
                print('d', d, 'm', m, 'tile shapes', n, 'E-count fails', f, ex, flush=True)
    else:
        from ns import NS
        from exp_cl_adv import with_conductor
        from srcl import tile_of
        from math import gcd
        from functools import reduce
        rng = random.Random(int(sys.argv[2])); NT = int(sys.argv[3]); MMAX = int(sys.argv[4])
        f = 0; cnt = 0; worst = None
        while cnt < NT:
            m = rng.randint(6, MMAX); k = rng.randint(2, 12)
            if rng.random() < 0.5:
                base = rng.randint(m + 1, 3*m); gens = sorted(set([m] + [base + rng.randint(0, max(1, m//3)) for _ in range(k)]))
            else:
                gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4])*m) for _ in range(k)]))
            if reduce(gcd, gens) != 1: continue
            s0 = NS.from_generators(gens)
            for s in [s0] + [with_conductor(gens, int(s0.c*fr)) for fr in (0.4, 0.7) if int(s0.c*fr) > m]:
                cnt += 1
                cells, d = tile_of(s); S = set(cells)
                A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
                A2 = [y for y in A if sum(y) >= 2]
                subs = [[y] for y in A2] + [A] + [rng.sample(A, rng.randint(1, len(A))) for _ in range(60)]
                subs += [[y for y in A if rng.random() < q] for q in (0.3, 0.6, 0.9) for _ in range(20)]
                w = ecount(A, d, [Y for Y in subs if Y])
                if w and w[0] < 0:
                    f += 1
                    if f <= 3: print('FAIL', gens, s.c, w)
                if w and (worst is None or w[0] < worst[0]): worst = (w[0], gens[:6], s.c)
        print(cnt, 'tiles; E-count fails', f, 'worst', worst)
