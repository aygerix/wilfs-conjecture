"""G-BR without surjectivity (lead, 2026-10-19).  D = random finite down-set in N^d, m >= |D|, p in (Z/m)^d with
x -> x.p mod m INJECTIVE on D (not necessarily onto).  For every sigma, r(x) = (x.p - sigma) mod m, test
   G-BR:  sum_{|y|>=2} Delta(y) >= -r(0),   m Delta(y) = sum_c y_c r(y-e_c) - (|y|-1) r(y) - r(0).
Also reports whether the tile (bijective) instances found this way pass.
usage: python gbr_inj.py seed trials dmax hmax mslack"""
import sys, random, itertools


def downset(gens, d):
    D = set()
    for g in gens:
        for x in itertools.product(*[range(gi+1) for gi in g]): D.add(x)
    return sorted(D)


if __name__ == '__main__':
    seed, T, dmax, hmax, mslack = map(int, sys.argv[1:6]); rng = random.Random(seed)
    fails = 0; n = 0; worst = None; nt = 0
    for t in range(T):
        d = rng.randint(1, dmax); gens = []
        for _ in range(rng.randint(1, 6)):
            h = rng.randint(1, hmax); g = [0]*d
            for _ in range(h): g[rng.randrange(d)] += 1
            gens.append(tuple(g))
        D = downset(gens, d)
        if len(D) < 3: continue
        m = len(D)+rng.randint(0, mslack)
        ok = False
        for _ in range(200):
            p = [rng.randrange(m) for _ in range(d)]
            vals = [sum(x[i]*p[i] for i in range(d)) % m for x in D]
            if len(set(vals)) == len(D): ok = True; break
        if not ok: continue
        n += 1; nt += (m == len(D))
        Dset = set(D)
        def sub(x, c): return tuple(x[i]-(i == c) for i in range(d))
        high = [y for y in D if sum(y) >= 2]
        phi = {x: sum(x[i]*p[i] for i in range(d)) for x in D}
        for sig in range(m):
            r = {x: (phi[x]-sig) % m for x in D}; r0 = r[(0,)*d]
            tot = 0
            for y in high:
                num = sum(y[c]*r[sub(y, c)] for c in range(d) if y[c])-(sum(y)-1)*r[y]-r0
                assert num % m == 0
                tot += num//m
            v = tot+r0
            if worst is None or v < worst[0]: worst = (v, d, m, len(D), gens, p, sig)
            if v < 0:
                fails += 1
                if fails <= 8: print("FAIL", "d", d, "m", m, "|D|", len(D), "gens", gens, "p", p, "sigma", sig, "value", v, flush=True)
    print("instances", n, "(bijective:", nt, ") failures (instance,sigma)", fails, "worst", worst)
