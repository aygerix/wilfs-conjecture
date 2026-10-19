"""Test the no-wrap linear part of MaxCL on random down-sets (lead, 2026-10-19).
For a finite down-set D in N^d, A = maximal cells, direction a:
   Phi_a(D) = sum_{y in A} (d+|y|) y_a - (d+1) sum_{x in D} x_a.
If Phi_a <= 0 for all a, then MaxCL holds whenever r(x) = x.rho (no wraps, rho_0 = 0, rho >= 0).
Random down-sets: union of principal ideals [0,g] for random generators g with |g| <= H.
usage: python phi_downset.py seed trials dmax H"""
import sys, random, itertools
def downset(gens, d):
    D = set()
    for g in gens:
        for x in itertools.product(*[range(gi+1) for gi in g]): D.add(x)
    return D
if __name__ == '__main__':
    seed, T, dmax, H = map(int, sys.argv[1:5]); rng = random.Random(seed)
    worst = None; npos = 0
    for t in range(T):
        d = rng.randint(1, dmax); k = rng.randint(1, 8)
        gens = []
        for _ in range(k):
            h = rng.randint(0, H); g = [0]*d
            for _ in range(h): g[rng.randrange(d)] += 1
            gens.append(tuple(g))
        D = downset(gens, d)
        A = [y for y in D if all(tuple(y[i]+(i == a) for i in range(d)) not in D for a in range(d))]
        for a in range(d):
            phi = sum((d+sum(y))*y[a] for y in A)-(d+1)*sum(x[a] for x in D)
            if phi > 0:
                npos += 1
                if npos <= 5: print("Phi>0:", phi, "d", d, "a", a, "gens", gens, "|D|", len(D))
            if worst is None or phi > worst[0]: worst = (phi, d, a, gens, len(D))
    print("trials", T, "positive Phi count", npos, "max Phi", worst)
