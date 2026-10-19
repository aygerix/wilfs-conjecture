"""Core+spike adversarial family for MaxCL at ANY height (lead, 2026-10-19).  As spike_maxcl.py, but the core
residues are filled to core height Hc (random in [3,6]), and each missing residue gets a spike K*m + res with
K random in [2, Hc+2] (per spike), so spikes can sit below, at, or above the core top.  All sigma are tested; the
Wilf sigma (sigma = c mod m, i.e. r(top Apery element) = m-1) is reported separately.
usage: python spike_maxcl_h.py seed trials mmin mmax maxspikes"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup


def maxcl_all(m, gens):
    best = apery_tile(m, gens)
    if len(best) != m: return None
    d = len(gens); D = {x: w for (w, x) in best.values()}
    H = max(sum(x) for x in D)
    def add(x, a): return tuple(x[i]+(i == a) for i in range(d))
    A = set(y for y in D if all(add(y, a) not in D for a in range(d)))
    tot = (d+1)*m*(m-1)/2
    wmax = max(D.values()); sigW = (wmax+1) % m
    mn = None; sW = None
    for sig in range(m):
        r = {x: (w-sig) % m for x, w in D.items()}
        s = (d+1)*sum(r[x] for x in D if x not in A)-sum((sum(y)-1)*r[y] for y in A)
        if mn is None or s < mn[0]: mn = (s, sig)
        if sig == sigW: sW = s
    return H, d, mn, mn[0]/tot, sW, sW/tot


if __name__ == '__main__':
    seed, T, mmin, mmax, maxsp = map(int, sys.argv[1:6]); rng = random.Random(seed)
    stats = {}; fails = 0; wfails = 0
    for t in range(T):
        m = rng.randint(mmin, mmax); k = rng.randint(2, 4); Hc = rng.randint(3, 6)
        tau = sorted(set(rng.randint(1, m-1) for _ in range(k)))
        core = [m+x for x in tau]
        sums = {0}
        for _ in range(Hc): sums |= {s+x for s in sums for x in core}
        hit = {s % m for s in sums}
        spikes = [rng.randint(2, Hc+2)*m+res for res in range(1, m) if res not in hit]
        if len(spikes) > maxsp: continue
        gens = sorted(set(core+spikes))
        gens = [g for g in gens if not in_semigroup(g, m, [h for h in gens if h != g])]
        if len(set(g % m for g in gens)) < len(gens): continue
        R = maxcl_all(m, gens)
        if R is None: continue
        H, d, (s, sig), ns, sW, nsW = R
        st = stats.setdefault(H, [0, None, None])
        st[0] += 1
        if s < 0:
            fails += 1
            if fails <= 10: print("MAXCL FAIL (some sigma)", m, gens, "H", H, "sigma", sig, "slack", s, flush=True)
        if sW < 0:
            wfails += 1
            if wfails <= 10: print("MAXCL FAIL at Wilf sigma", m, gens, "H", H, "slack", sW, flush=True)
        if st[1] is None or ns < st[1][0]: st[1] = (round(ns, 4), s, m, gens, sig, d)
        if st[2] is None or nsW < st[2][0]: st[2] = (round(nsW, 4), sW, m, gens, d)
    print("MaxCL failures (any sigma)", fails, " at Wilf sigma", wfails)
    for H in sorted(stats):
        print("height", H, "tiles", stats[H][0], "min norm slack any sigma", stats[H][1], " at Wilf sigma", stats[H][2])
