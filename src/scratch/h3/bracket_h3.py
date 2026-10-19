"""(also tests H3-BR: Br_0 + rho_0 >= 0)
Height-3 MaxCL unit form: where does the carry bracket go negative, and how tight is lin >= -m*Br? (lead, 2026-10-19)
For each (tile, sigma) with Br < 0 report ratio = lin / (-m*Br) (MaxCL <=> ratio >= 1), and the three negative parts
  n1 = #maximal pairs with K=-1, n2 = sum over cubics of -2K (K<0), n3 = sum over N2 pairs with K=+1 of (psi-1),
and the positive parts p1 = #A2 with K=+1, p2 = sum over cubics of 2K (K>0), p3 = sum over N2 with K=-1 of (psi-1).
Families as in unitform_h3.py; all sigma.
usage: python bracket_h3.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup


MODES = None
def gen(rng, mmin, mmax):
    m = rng.randint(mmin, mmax); mode = rng.randrange(3) if MODES is None else rng.choice(MODES)
    if mode == 0:
        d = rng.randint(2, 9); gens = sorted(set(rng.randint(m+1, 2*m-1) for _ in range(d)))
    elif mode == 1:
        d = rng.randint(3, 8); L = rng.randint(d*d, max(d*d+1, d**3//2)); rho = sorted(set(rng.randint(1, L) for _ in range(d)))
        sums = set([0])
        for _ in range(3): sums |= {x+y for x in sums for y in [0]+rho}
        m = max(d+2, len(sums)-rng.randint(0, max(1, len(sums)//4))); gens = sorted(set(m+(r % m) for r in rho if r % m))
    else:
        d = rng.randint(3, 8); a0 = rng.randint(m+1, 2*m); st = rng.randint(1, max(1, m//(2*d))); gens = sorted(set(a0+i*st for i in range(d)))
    return m, [x for x in gens if x % m and x > m]


if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed); n = 0; nneg = 0
    if len(sys.argv) > 5: MODES = [int(x) for x in sys.argv[5].split(',')]
    worst = []; agg = [0]*6; hbr = None; hbr_fail = 0; tight = []
    for t in range(T):
        m, gens = gen(rng, mmin, mmax)
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
        sigs = range(m) if m <= 160 else sorted(set(rng.sample(range(m), 120) + [ (-(max(D.values())-m+1)) % m ]))
        for sig in sigs:
            r = {x: (w-sig) % m for x, w in D.items()}; r0 = r[(0,)*d]; ru = [r[E[a]] for a in range(d)]
            l = {x: (1-sum(x))*r0+sum(x[a]*ru[a] for a in range(d)) for x in D}
            K = {x: (l[x]-r[x])//m for x in D}
            lin = sum((d+1-deg[a])*ru[a] for a in range(d) if E[a] not in A)+m*r0+sum((d+2-psi[z])*r[z] for z in N2)
            n1 = sum(1 for z in A2 if K[z] < 0); n2 = sum(-2*K[y] for y in cub if K[y] < 0); n3 = sum(psi[z]-1 for z in N2 if K[z] > 0)
            p1 = sum(1 for z in A2 if K[z] > 0); p2 = sum(2*K[y] for y in cub if K[y] > 0); p3 = sum(psi[z]-1 for z in N2 if K[z] < 0)
            br = p1+p2+p3-n1-n2-n3
            if hbr is None or br+r0 < hbr[0]: hbr = (br+r0, m, gens, sig, r0, br, (n1, n2, n3), (p1, p2, p3))
            if br+r0 < 0: hbr_fail += 1
            if br+r0 <= 1 and (n1+n2+n3) > 0 and len(tight) < 40: tight.append((br+r0, m, gens, sig, r0, br, (n1, n2, n3), (p1, p2, p3), len(A2), len(N2), len(cub)))
            n += 1
            for i, v in enumerate((n1, n2, n3, p1, p2, p3)): agg[i] += v
            if br < 0:
                nneg += 1
                worst.append((lin/(-m*br), m, gens, sig, r0, (n1, n2, n3), (p1, p2, p3), lin, br))
    worst.sort()
    print("H3-BR: failures", hbr_fail, "min (Br+rho0, m, gens, sig, rho0, Br, neg, pos) =", hbr)
    for tt in tight: print("  TIGHT", tt)
    print("pairs", n, "with Br<0:", nneg, "aggregate n1,n2,n3,p1,p2,p3 =", agg)
    for w in worst[:8]: print("  ratio %.3f m=%d gens=%s sig=%d rho0=%d neg=%s pos=%s lin=%d Br=%d" % w)
