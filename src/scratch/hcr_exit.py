# HCR_exit: H_n >= sum_x (d - outdeg(x)) ht(x)  (every exit (x, a), x + e_a not in D, makes x its own a-top).
#   HCR_exit(D) := [(m+1) sum_x (d - outdeg x) ht(x) + sum_i T_(i) i] / ((d-1) m (m-1)/2)  <=  HCR(D).
import sys, random, time; sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch'); sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from hcr_shape import hcr_shape
def hcr_exit(D):
    D = set(D); d = len(next(iter(D))); m = len(D)
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]; add = lambda x, y: tuple(p + q for p, q in zip(x, y))
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, u)] + 1 for u in U if add(x, u) in D], default=0)
    S = sum((d - sum(add(x, u) in D for u in U)) * ht[x] for x in D)
    T = sorted((d + sum(y) for y in D if ht[y] == 0), reverse=True)
    return ((m + 1) * S + sum(i * t for i, t in enumerate(T))) / ((d - 1) * m * (m - 1) / 2)
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'enum3':
        from tile_enum import enumerate_tiles
        for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
            seen = set(); n = bad = 0; w = None
            for r, D, poly in enumerate_tiles(m):
                k = frozenset(D)
                if k in seen: continue
                seen.add(k); v = hcr_exit(k); n += 1; bad += v < 1 - 1e-12
                if w is None or v < w[0]: w = (round(v, 4), r)
            print(f'm={m}: {n} 3-D tiles, HCR_exit fails {bad}, worst {w}', flush=True)
    else:
        from ns import NS
        from cl import factorizations_down_set
        E0, E1, seed, budget = map(int, sys.argv[2:6]); rnd = random.Random(seed); t0 = time.time(); res = {}
        while time.time() - t0 < budget:
            e = rnd.randint(E0, E1); m = rnd.randint(max(20, 3 * e + 1), 55)
            try: s = NS.from_generators([m] + rnd.sample(range(m + 1, 3 * m), e - 1))
            except ValueError: continue
            if s.e != e or s.c <= 3 * s.m: continue
            Pp, best = factorizations_down_set(s, 'grlex'); D = set(best.values())
            v = hcr_exit(D); R = res.setdefault(e, [0, 0, None]); R[0] += 1; R[1] += v < 1 - 1e-12
            if R[2] is None or v < R[2][0]: R[2] = (round(v, 4), s.P, round(hcr_shape(D), 4))
        for e in sorted(res): print(f'  e={e}: {res[e][0]} S (m >= 20), HCR_exit fails {res[e][1]}, worst (exit, P, HCR) {res[e][2]}')
