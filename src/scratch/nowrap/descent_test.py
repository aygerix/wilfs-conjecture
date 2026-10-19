"""WRAP-DESCENT probe (lead, 2026-10-19).  Fix a lattice (p mod m).  A flip moves a maximal cell y of a tile D to
y' != y with the same label, so that D' = D - {y} + {y'} is again a down-set (hence a tile).
E(D) = sum_D floor(x.P/m) (canonical lift) is minimized by the P-min tile.  Question: for every tile D with
E(D) > E_min and every sigma, is there a flip with E(D') < E(D) and S_{D'}(sigma) <= S_D(sigma)?
If yes, MaxCL for all tiles reduces to MaxCL for E-minimal tiles.
Tiles: grlex Apery tiles of random S, then random E-increasing flips to diversify.
usage: python descent_test.py seed trials mmin mmax"""
import sys, random, itertools
from pmin_tile import apery, minimal_gens, tile

def Svals(m, P, D):
    d = len(P); Ds = set(D)
    A = [y for y in D if all(tuple(y[i]+(i == a) for i in range(d)) not in Ds for a in range(d))]
    lab = {y: sum(y[i]*P[i] for i in range(d)) % m for y in A}
    M1 = m*(m-1)//2
    return [(d+1)*M1-sum((d+sum(y))*((lab[y]-sg) % m) for y in A) for sg in range(m)], A

def Eval(m, P, D): return sum(sum(x[i]*P[i] for i in range(len(P)))//m for x in D)

def flips(m, P, D, A, H):
    d = len(P); Ds = set(D); out = []
    for y in A:
        L = sum(y[i]*P[i] for i in range(d)) % m
        for h in range(1, H+1):
            for comb in itertools.combinations_with_replacement(range(d), h):
                z = [0]*d
                for a in comb: z[a] += 1
                z = tuple(z)
                if z == y or z in Ds or sum(z[i]*P[i] for i in range(d)) % m != L: continue
                if all(tuple(z[i]-(i == a) for i in range(d)) in Ds and tuple(z[i]-(i == a) for i in range(d)) != y for a in range(d) if z[a] > 0):
                    out.append((y, z))
    return out

if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
    tested = 0; stuck = 0; examples = []; nolower = [0]
    for tr in range(T):
        m = rng.randint(mmin, mmax); kk = rng.randint(2, 4)
        gens = [rng.randint(m+1, 3*m) for _ in range(kk)]
        if None in apery(m, gens): continue
        n, ap = minimal_gens(m, gens)
        if len(n) < 2 or len(n) > 4: continue
        d = len(n); P = [g % m for g in n]
        D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values())
        H = max(sum(x) for x in D)+2
        for step in range(rng.randint(0, 6)):           # diversify by random flips
            S, A = Svals(m, P, D); fl = flips(m, P, D, A, H)
            if not fl: break
            y, z = rng.choice(fl); D = [x for x in D if x != y]+[z]
        Emin = Eval(m, P, list(tile(m, n, ap, lambda x: (sum(x[i]*P[i] for i in range(d)), sum(x), tuple(-t for t in x))).values()))
        E = Eval(m, P, D)
        if E == Emin: continue
        S, A = Svals(m, P, D); fl = flips(m, P, D, A, H)
        cand = []
        for (y, z) in fl:
            D2 = [x for x in D if x != y]+[z]
            if Eval(m, P, D2) < E: cand.append(Svals(m, P, D2)[0])
        if not cand: nolower[0] += 1
        for sg in range(m):
            tested += 1
            if not any(S2[sg] <= S[sg] for S2 in cand):
                stuck += 1
                if len(examples) < 6: examples.append((m, n, sg, S[sg], E, Emin, len(cand)))
    print("(tile,sigma) tested", tested, "no descending flip:", stuck, "; tiles with E > Emin but no E-lowering single flip:", nolower[0])
    for e in examples: print("  stuck: m %d n %s sigma %d S %d E %d Emin %d #E-lowering flips %d" % e)
