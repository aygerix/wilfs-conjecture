"""Adversarial search for height-<=3 tiles on which the crude bound CR fails (lead, 2026-10-19).
CR (shape-only, implies MaxCL at every sigma):  sum_i w_i (m-1-i) <= (d+1) |N|(|N|-1)/2,  w = (|y|-1) over maximal y
sorted decreasing.  Near-perfect cores make CR fail; the question is whether that can happen with d >= 6.
Families: (0) cyclic near-perfect: k core residues p in Z/m with m in [C(k+3,3), 2C(k+3,3)], spikes K*m+res for the
residues not hit by a <=3-sum; (1) integer near-B_3 sets (as h3_extremal mode 4) with spikes; (2) mode 1 without
spikes.  For every CR failure the actual MaxCL slack (min over sigma) is computed as well.
usage: python crude_adv.py seed trials kmin kmax"""
import sys, random
from math import comb
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup


def analyse(m, gens):
    best = apery_tile(m, gens)
    if len(best) != m: return None
    d = len(gens); D = {x: w for (w, x) in best.values()}
    if max(sum(x) for x in D) > 3: return None
    def add(x, a): return tuple(x[i]+(i == a) for i in range(d))
    A = [y for y in D if all(add(y, a) not in D for a in range(d))]; Aset = set(A)
    N = [x for x in D if x not in Aset]
    w = sorted((sum(y)-1 for y in A), reverse=True)
    lhs = sum(wi*(m-1-i) for i, wi in enumerate(w)); rhs = (d+1)*len(N)*(len(N)-1)//2
    s = sum(1 for y in A if sum(y) == 1)
    out = dict(d=d, s=s, k=d-s, m=m, cr=rhs-lhs, T=sum(1 for y in D if sum(y) == 3), N=len(N))
    if rhs < lhs:
        mn = None
        for sig in range(m):
            r = {x: (v-sig) % m for x, v in D.items()}
            sl = (d+1)*sum(r[x] for x in N)-sum((sum(y)-1)*r[y] for y in A)
            if mn is None or sl < mn: mn = sl
        out['maxcl'] = mn
    return out


if __name__ == '__main__':
    seed, T, kmin, kmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
    n = 0; fails = {}; ex = []
    for t in range(T):
        k = rng.randint(kmin, kmax); fam = rng.randrange(3)
        if fam == 0:
            c3 = comb(k+3, 3); m = rng.randint(max(k+2, c3//2), 2*c3)
            p = sorted(set(rng.randrange(1, m) for _ in range(k)))
        elif fam == 1:
            L = rng.randint(k*k, max(k*k+1, k**3//2)); rho = sorted(set(rng.randint(1, L) for _ in range(k)))
            sums = {0}
            for _ in range(3): sums |= {x+y for x in sums for y in [0]+rho}
            N3 = len(sums); m = max(k+2, N3-rng.randint(0, max(1, N3//4))); p = sorted(set(r % m for r in rho if r % m))
        else:
            m = rng.randint(2*k, comb(k+3, 3)+10); a0 = rng.randint(1, m-1); st = rng.randint(1, max(1, m//(2*k)))
            p = sorted(set((a0+i*st) % m for i in range(k)) - {0})
        core = [m+x for x in p]
        sums = {0}
        for _ in range(3): sums |= {x+y for x in sums for y in [0]+core}
        hit = {x % m for x in sums}
        spikes = [] if fam == 2 else [rng.randint(2, 4)*m+res for res in range(1, m) if res not in hit]
        if len(spikes) > 40: continue
        gens = sorted(set(core+spikes))
        gens = [g for g in gens if not in_semigroup(g, m, [h for h in gens if h != g])]
        if len(gens) < 2 or len(set(g % m for g in gens)) < len(gens): continue
        R = analyse(m, gens)
        if R is None: continue
        n += 1
        if R['cr'] < 0:
            key = R['d']; fails[key] = fails.get(key, 0)+1
            if R['d'] >= 6 and len(ex) < 12: ex.append((m, gens, R))
            if R.get('maxcl', 0) < 0: print("MAXCL FAIL", m, gens, R, flush=True)
    print("height<=3 tiles", n, "CR failures by d:", dict(sorted(fails.items())))
    for e in ex: print("  d>=6 CR failure:", e)
