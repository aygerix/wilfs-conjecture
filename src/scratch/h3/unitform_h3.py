"""Unit-expansion identity for MaxCL at height <= 3 (lead, 2026-10-19).  With l(x) = (1-|x|) rho_0 + sum_a x_a rho_a,
K(x) = floor(l(x)/m), psi(z) = sum_{c: z+e_c in D} (z_c+1) for pairs z, deg(a) = sum_{pairs z} z_a:
  RHS-LHS = sum_a (d+1-deg a) rho_a [a non-max] + m rho_0 + sum_{z in N2} (d+2-psi z) rho_z
            + m [ sum_{A2} K + 2 sum_T K - sum_{N2} (psi(z)-1) K(z) ].
Checks the identity, and reports the distribution of the bracket's negative parts against the positive linear terms.
usage: python unitform_h3.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup
if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed); n = 0; bad = 0
    worst = None
    for t in range(T):
        m = rng.randint(mmin, mmax); mode = rng.randrange(3)
        if mode == 0:
            d = rng.randint(2, 9); gens = sorted(set(rng.randint(m+1, 2*m-1) for _ in range(d)))
        elif mode == 1:
            d = rng.randint(3, 8); L = rng.randint(d*d, max(d*d+1, d**3//2)); rho = sorted(set(rng.randint(1, L) for _ in range(d)))
            sums = set([0])
            for _ in range(3): sums |= {x+y for x in sums for y in [0]+rho}
            m = max(d+2, len(sums)-rng.randint(0, max(1, len(sums)//4))); gens = sorted(set(m+(r % m) for r in rho if r % m))
        else:
            d = rng.randint(3, 8); a0 = rng.randint(m+1, 2*m); st = rng.randint(1, max(1, m//(2*d))); gens = sorted(set(a0+i*st for i in range(d)))
        gens = [x for x in gens if x % m and x > m]
        if len(gens) < 2 or len(set(x % m for x in gens)) < len(gens): continue
        if any(in_semigroup(gens[a], m, gens[:a]+gens[a+1:]) for a in range(len(gens))): continue
        best = apery_tile(m, gens)
        if len(best) != m: continue
        d = len(gens); D = {x: w for (w, x) in best.values()}
        E = [tuple(1 if i == a else 0 for i in range(d)) for a in range(d)]
        if any(e not in D for e in E) or max(sum(x) for x in D) != 3: continue
        def add(x, a): return tuple(x[i]+(i == a) for i in range(d))
        A = set(y for y in D if all(add(y, a) not in D for a in range(d)))
        prs = [x for x in D if sum(x) == 2]; cub = [x for x in D if sum(x) == 3]
        A2 = [x for x in prs if x in A]; N2 = [x for x in prs if x not in A]
        psi = {z: sum(z[c]+1 for c in range(d) if add(z, c) in D) for z in N2}
        deg = [sum(z[a] for z in prs) for a in range(d)]
        for sig in rng.sample(range(m), min(m, 6)):
            r = {x: (w-sig) % m for x, w in D.items()}; r0 = r[(0,)*d]; ru = [r[E[a]] for a in range(d)]
            lhs = sum((sum(y)-1)*r[y] for y in A); rhs = (d+1)*sum(r[x] for x in D if x not in A)
            l = {x: (1-sum(x))*r0+sum(x[a]*ru[a] for a in range(d)) for x in D}
            K = {x: (l[x]-r[x])//m for x in D}; assert all((l[x]-r[x]) % m == 0 for x in D)
            lin = sum((d+1-deg[a])*ru[a] for a in range(d) if E[a] not in A)+m*r0+sum((d+2-psi[z])*r[z] for z in N2)
            br = sum(K[z] for z in A2)+2*sum(K[y] for y in cub)-sum((psi[z]-1)*K[z] for z in N2)
            n += 1
            if rhs-lhs != lin+m*br:
                bad += 1
                if bad <= 3: print("MISMATCH", m, gens, sig, rhs-lhs, lin+m*br)
            neg = sum(1 for z in A2 if K[z] < 0)+2*sum(-K[y] for y in cub if K[y] < 0)+sum((psi[z]-1) for z in N2 if K[z] > 0)
            ratio = (br*m+lin)/(m*m)
            if worst is None or br < worst[0]: worst = (br, lin/m, r0, m, gens, sig, neg)
    print("checked", n, "mismatches", bad)
    print("most negative bracket (br, lin/m, rho0, m, gens, sigma, total negative part):", worst)
