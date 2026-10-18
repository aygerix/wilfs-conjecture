# MAXSUM_d:  S1 := sum_{y maximal} (d + |y|)  <=  (d+1) m / 2 + (d-1)/2   (implies CR, hence Wilf, any c).
import sys, random, time; sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
def S1(D, d):
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    return sum(d + sum(y) for y in D if all(tuple(p + q for p, q in zip(y, u)) not in D for u in U))
def twoface(D, d): return any(tuple(int(i in (a, b)) for i in range(d)) not in D for a in range(d) for b in range(a + 1, d))
mode = sys.argv[1]
if mode == 'enum':
    from tile_enum import enumerate_tiles
    for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        w = None; bad = 0; n = 0; seen = set()
        for r, D, poly in enumerate_tiles(m):
            k = frozenset(D)
            if k in seen: continue
            seen.add(k); D = set(D)
            if twoface(D, 3): continue
            ex = S1(D, 3) - (4 * m / 2 + 1); n += 1; bad += ex > 0
            if w is None or ex > w[0]: w = (ex, r)
        print(f'm={m}: {n} non-two-face tiles, MAXSUM_3 fails {bad}, max excess {w}', flush=True)
else:
    from ns import NS
    from cl import factorizations_down_set
    E0, E1, seed, budget, mmax, K = map(int, sys.argv[2:8]); rnd = random.Random(seed); t0 = time.time(); res = {}
    while time.time() - t0 < budget:
        e = rnd.randint(E0, E1); m = rnd.randint(3 * e + 1, mmax)
        try: s = NS.from_generators([m] + rnd.sample(range(m + 1, K * m), e - 1))
        except ValueError: continue
        if s.e != e or s.c <= 3 * s.m: continue
        Pp, best = factorizations_down_set(s, 'grlex'); d = len(Pp); D = set(best.values())
        key = (e, twoface(D, d)); ex = S1(D, d) - ((d + 1) * m / 2 + (d - 1) / 2)
        R = res.setdefault(key, [0, 0, None]); R[0] += 1; R[1] += ex > 0
        if R[2] is None or ex / m > R[2][0]: R[2] = (round(ex / m, 4), s.P)
    for k in sorted(res): print(f'  e={k[0]} two-face={k[1]}: {res[k][0]} S, MAXSUM fails {res[k][1]}, max excess/m {res[k][2]}')
