"""Extremal search for MaxCL on Apery tiles of height exactly 3 (lead, 2026-10-19).
MaxCL(sigma):  sum_{y in A} (d+|y|) r(y) <= (d+1) m(m-1)/2,  r = (w - sigma) mod m  (A = maximal cells of the
grlex factorization tile).  Reports, per d, the minimum over tiles and sigma of the normalized slack
   nslack = 1 - sum_A (d+|y|) r(y) / ((d+1) m(m-1)/2),
the minimizing tile, sigma, and its height profile (#units, #pairs, #cubics, #maximal pairs).
Families: random gens in (m,2m); near-arithmetic a0+i*st; 'Sidon-like' m+b_i with b a greedy B_3-ish set scaled.
usage: python h3_extremal.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup

def tile_stats(m, gens):
    if any(in_semigroup(gens[a], m, gens[:a]+gens[a+1:]) for a in range(len(gens))): return None
    best = apery_tile(m, gens)
    if len(best) != m: return None
    d = len(gens)
    D = {x: w for (w, x) in best.values()}
    for a in range(d):
        if tuple(1 if i == a else 0 for i in range(d)) not in D: return None
    H = max(sum(x) for x in D)
    if H != 3: return None
    A = [x for x in D if all(tuple(x[i]+(i == a) for i in range(d)) not in D for a in range(d))]
    wts = [(d+sum(y), D[y]) for y in A]
    tot = (d+1)*m*(m-1)/2
    best_s = None
    for sig in range(m):
        lhs = sum(wt*((w-sig) % m) for wt, w in wts)
        ns = 1-lhs/tot
        if best_s is None or ns < best_s[0]: best_s = (ns, sig)
    M = max(D.values()); c = M-m+1
    lhs_c = sum(wt*((w-c) % m) for wt, w in wts)
    prof = (d, sum(1 for x in D if sum(x) == 2), sum(1 for x in D if sum(x) == 3), sum(1 for x in A if sum(x) == 2))
    if '--show' in sys.argv: pass
    return best_s, 1-lhs_c/tot, prof

if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); MODES = [int(x) for x in sys.argv[5].split(',')] if len(sys.argv) > 5 else None
    rng = random.Random(seed)
    worst = {}; n = 0
    for tr in range(T):
        m = rng.randint(mmin, mmax); mode = rng.randrange(4) if MODES is None else rng.choice(MODES)
        if mode == 4:
            # near-B_3 family: units rho in [1,L] random, m close to the number of distinct <=3-sums of {0} u rho
            d = rng.randint(3, 9); L = rng.randint(d*d, max(d*d+1, d**3//2))
            rho = sorted(set(rng.randint(1, L) for _ in range(d)))
            sums = set([0]); 
            for _ in range(3): sums |= {x+y for x in sums for y in [0]+rho}
            N3 = len(sums); m = max(d+2, N3-rng.randint(0, max(1, N3//4)))
            gens = sorted(set(m+(r % m) for r in rho if r % m))
        elif mode == 0:
            d = rng.randint(2, 12); gens = sorted(set(rng.randint(m+1, 2*m-1) for _ in range(d)))
        elif mode == 1:
            d = rng.randint(2, 10); a0 = rng.randint(m+1, 2*m); st = rng.randint(1, max(1, m//(2*d)))
            gens = sorted(set(a0+i*st for i in range(d)))
        elif mode == 2:
            # few generators chosen to make many distinct cubic residues: random multipliers
            d = rng.randint(2, 8); gens = sorted(set(m+rng.randint(1, m-1) for _ in range(d)))
            if len(gens) >= 2 and rng.random() < 0.5: gens[-1] = gens[0]+gens[1]-m+rng.randint(-2, 2)
        else:
            d = rng.randint(3, 10); base = rng.randint(m+1, 2*m)
            gens = sorted(set(base+rng.randint(0, m//2) for _ in range(d)))
        gens = [x for x in gens if x % m and x > m]
        if len(gens) < 2 or len(set(x % m for x in gens)) < len(gens): continue
        R = tile_stats(m, gens)
        if R is None: continue
        n += 1
        (ns, sig), nsc, prof = R
        d = prof[0]
        if d not in worst or ns < worst[d][0]: worst[d] = (ns, nsc, m, gens, sig, prof)
    print(f"seed={seed} height-3 tiles tested={n}")
    for d in sorted(worst):
        v = worst[d]; print(f"  d={d:2d} min nslack={v[0]:.4f} (at sigma=c: {v[1]:.4f}) m={v[2]} gens={v[3]} sigma={v[4]} (d,pairs,cubics,maxpairs)={v[5]}")
