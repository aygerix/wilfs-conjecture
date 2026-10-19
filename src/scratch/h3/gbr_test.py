"""G-BR test (lead, 2026-10-19): for a tile (D, p) of ANY height and every sigma,
   Delta(y) = ( sum_c y_c r(y-e_c) - (|y|-1) r(y) - r(0) ) / m   (an integer, for every |y| >= 2),
   G-BR:  sum_{|y|>=2} Delta(y) >= -r(0).
Equivalently (linear form):  sum_{|y|>=2} (|y|-1) r(y) <= (d+1) r(0) + sum_{|x|>=1} L(x) r(x),
   L(x) = sum_c (x_c+1) [x+e_c in D].   G-BR => MaxCL (termwise weights L(x)-(|x|-1) <= d+1 on N, 0 on A).
At height 2 G-BR is exactly the Flat-MaxCL inequality (proved).  Tests random Apery tiles (grlex factorization tile)
and named instances; reports failures and the minimum of sum Delta + r(0), by height.
usage: python gbr_test.py seed trials mmin mmax [named]"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup


def check(m, gens, sigs=None):
    if any(in_semigroup(gens[a], m, gens[:a]+gens[a+1:]) for a in range(len(gens))): return None
    best = apery_tile(m, gens)
    if len(best) != m: return None
    d = len(gens); D = {x: w for (w, x) in best.values()}
    for a in range(d):
        if tuple(1 if i == a else 0 for i in range(d)) not in D: return None
    H = max(sum(x) for x in D)
    def sub(x, c): return tuple(x[i]-(i == c) for i in range(d))
    high = [y for y in D if sum(y) >= 2]
    res = []
    for sig in (range(m) if sigs is None else sigs):
        r = {x: (w-sig) % m for x, w in D.items()}; r0 = r[(0,)*d]
        tot = 0
        for y in high:
            num = sum(y[c]*r[sub(y, c)] for c in range(d) if y[c])-(sum(y)-1)*r[y]-r0
            assert num % m == 0
            tot += num//m
        res.append((tot+r0, sig))
    return H, d, min(res)


if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
    if len(sys.argv) > 5:
        for (m, gens) in [(39, [71, 72, 77]), (16, [17, 20, 21]), (14, [15, 18, 19]), (80, [291, 292, 293]),
                          (62, [87, 88, 89]), (14, [15, 23, 24, 26]), (36, [37, 42, 43])]:
            R = check(m, gens)
            print("named", m, gens, "->", R, flush=True)
    worst = {}; fails = 0; n = 0
    for t in range(T):
        m = rng.randint(mmin, mmax); mode = rng.randrange(3)
        if mode == 0:
            d = rng.randint(2, 7); gens = sorted(set(rng.randint(m+1, 3*m) for _ in range(d)))
        elif mode == 1:
            d = rng.randint(2, 6); a0 = rng.randint(m+1, 3*m); st = rng.randint(1, max(1, m//(2*d))); gens = sorted(set(a0+i*st for i in range(d)))
        else:
            d = rng.randint(2, 5); gens = sorted(set(rng.randint(m+1, 6*m) for _ in range(d)))
        gens = [x for x in gens if x % m]
        if len(gens) < 2 or len(set(x % m for x in gens)) < len(gens): continue
        R = check(m, gens)
        if R is None: continue
        H, d, (v, sig) = R; n += 1
        if v < 0:
            fails += 1
            if fails <= 10: print("FAIL", m, gens, "H", H, "sum Delta + r0 =", v, "sigma", sig, flush=True)
        if H not in worst or v < worst[H][0]: worst[H] = (v, m, gens, sig)
    print("tiles", n, "fails", fails)
    for H in sorted(worst): print("  height", H, "min(sum Delta + r0) =", worst[H])
