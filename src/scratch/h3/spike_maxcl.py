"""Adversarial "core + spikes" family for height-3 MaxCL (lead, 2026-10-19).
E47 (<14,22,23,57,61,62,63>) = Delta_3 core in 2 directions + 4 spike generators filling the uncovered residues; it kills
Tile-CL.  Here: choose m, k core generators m + tau_i (small tau, near-B_3 or random), and for every residue NOT hit by a
height-<=3 core sum add a spike generator K*m + residue (K in {3,4}) -- unless that residue is already hit.
Compute the actual Apery tile of the resulting semigroup (grlex), keep it if height <= 3, and evaluate MaxCL at every
sigma; report the minimum normalized slack and any failure.  Also reports Tile-CL failures (min over sigma of the
G-BR value), to confirm the family is adversarial.
usage: python spike_maxcl.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup


def maxcl_min(m, gens):
    best = apery_tile(m, gens)
    if len(best) != m: return None
    d = len(gens); D = {x: w for (w, x) in best.values()}
    for a in range(d):
        if tuple(1 if i == a else 0 for i in range(d)) not in D: return None
    H = max(sum(x) for x in D)
    def add(x, a): return tuple(x[i]+(i == a) for i in range(d))
    def sub(x, c): return tuple(x[i]-(i == c) for i in range(d))
    A = [y for y in D if all(add(y, a) not in D for a in range(d))]; Aset = set(A)
    tot = (d+1)*m*(m-1)/2
    mn = None; tcl = None
    high = [y for y in D if sum(y) >= 2]
    for sig in range(m):
        r = {x: (w-sig) % m for x, w in D.items()}
        lhs = sum((sum(y)-1)*r[y] for y in A); rhs = (d+1)*sum(r[x] for x in D if x not in Aset)
        s = rhs-lhs
        if mn is None or s < mn[0]: mn = (s, sig)
        r0 = r[(0,)*d]; g = 0
        for y in high:
            g += (sum(y[c]*r[sub(y, c)] for c in range(d) if y[c])-(sum(y)-1)*r[y]-r0)//m
        if tcl is None or g+r0 < tcl[0]: tcl = (g+r0, sig)
    return H, d, mn, mn[0]/tot, tcl


if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
    n = 0; fails = 0; worst = None; tclfail = 0
    for t in range(T):
        m = rng.randint(mmin, mmax); k = rng.randint(2, 4)
        L = rng.randint(2, max(3, m//3)) if rng.random() < 0.3 else rng.randint(2, m-1)
        tau = sorted(set(rng.randint(1, L) for _ in range(k)))
        core = [m+x for x in tau]
        hit = set()
        sums = {0}
        for _ in range(3): sums |= {s+x for s in sums for x in [0]+core}
        hit = {s % m for s in sums}
        K = rng.choice([3, 4])
        spikes = [K*m+res for res in range(1, m) if res not in hit]
        if not spikes or len(spikes) > 12: continue
        gens = sorted(set(core+spikes))
        gens = [g for g in gens if not in_semigroup(g, m, [h for h in gens if h != g])]
        if len(set(g % m for g in gens)) < len(gens): continue
        R = maxcl_min(m, gens)
        if R is None: continue
        H, d, (s, sig), ns, (tv, tsig) = R
        if H > 3: continue
        n += 1
        if tv < 0:
            tclfail += 1
            if tclfail <= 6: print("TILE-CL FAIL", m, gens, "sigma", tsig, "value", tv, "MaxCL min slack", s, "norm", round(ns, 4), flush=True)
        if s < 0:
            fails += 1
            if fails <= 10: print("MAXCL FAIL", m, gens, "sigma", sig, "slack", s, flush=True)
        if H == 3 and (worst is None or ns < worst[0]): worst = (ns, s, m, gens, sig, d, tv)
    print("core+spike height-3 tiles", n, "MaxCL failures", fails, "Tile-CL(G-BR) failures", tclfail)
    print("min normalized MaxCL slack (height exactly 3):", worst)
