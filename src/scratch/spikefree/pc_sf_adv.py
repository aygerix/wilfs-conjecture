"""Adversarial search for H-SF: Tile-CL (PC: S >= Lam_r at every phase) on SPIKE-FREE semigroup tiles
(no minimal generator n_b with e_b maximal in the tile).  Hill-climbing on min_phase (S - Lam_r)/m over semigroups
<m, n_1..n_k>; tiles: grlex-least and P-min factorizations.  Also tracks the minimum over tiles WITH spikes.
usage: python pc_sf_adv.py seed restarts steps mmin mmax kmin kmax"""
import sys, random
sys.path.insert(0, '../nowrap')
from pmin_tile import apery, minimal_gens, tile

def pc_eval(m, n, ap, key):
    d = len(n); P = [g % m for g in n]
    D = list(tile(m, n, ap, key).values()); Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    nspk = sum(1 for a in range(d) if tuple(int(i == a) for i in range(d)) in A)
    v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    Tw = {x: sum(x[b]+1 for b in range(d) if up(x, b) not in Ds) for x in D}
    best = None
    for r0 in range(m):
        S = (d+1)*m*(m-1)//2-sum((d+sum(y))*((v[y]+r0) % m) for y in A)
        Lam = sum(Tw[t]*((v[t]+r0) % m) for t in D if t not in A)
        q = (S-Lam)/m
        if best is None or q < best[0]: best = (q, r0)
    return best, nspk, d, max(map(sum, D))

def score(m, gens):
    if None in apery(m, gens): return None
    n, ap = minimal_gens(m, gens)
    if len(n) < 2: return None
    grlex = lambda x: (sum(x), tuple(-t for t in x))
    P = [g % m for g in n]
    pkey = lambda x: (sum(x[i]*P[i] for i in range(len(n))), sum(x), tuple(-t for t in x))
    out = []
    for key in (grlex, pkey):
        out.append(pc_eval(m, n, ap, key))
    return n, out

seed, R, steps, mmin, mmax, kmin, kmax = map(int, sys.argv[1:8]); rng = random.Random(seed)
glob_sf = None; glob_spk = None; nsf = nfail_sf = 0
for rs in range(R):
    m = rng.randint(mmin, mmax); k = rng.randint(kmin, kmax)
    core = rng.randint(2, 3)
    gens = [m+rng.randint(1, m//2) for _ in range(core)]+[rng.randint(m+1, 5*m) for _ in range(k-core)]
    cur = None; curv = None
    for st in range(steps):
        g2 = list(gens)
        if cur is not None:
            i = rng.randrange(len(g2)); g2[i] = max(m+1, g2[i]+rng.choice([-1, 1])*rng.randint(1, m))
        res = score(m, g2)
        if res is None: continue
        n, out = res
        # objective: minimal slack among spike-free tiles (penalize spikes)
        vals = []
        for (q, r0), nspk, d, H in out:
            if nspk == 0:
                nsf += 1; vals.append(q)
                if q < 0:
                    nfail_sf += 1
                    print("SF-FAIL m", m, "n", n, "q", q, "rho0", r0, "d", d, "H", H, flush=True)
                if glob_sf is None or q < glob_sf[0]: glob_sf = (q, m, n, r0, d, H)
            else:
                if glob_spk is None or q < glob_spk[0]: glob_spk = (q, m, n, r0, d, H, nspk)
        obj = min(vals) + 0.0 if vals else 10**9
        if curv is None or obj <= curv:
            gens, curv, cur = g2, obj, n
print("spikefree_evals=%d spikefree_fail=%d" % (nsf, nfail_sf))
print("min spike-free (S-Lam)/m:", glob_sf)
print("min with-spike (S-Lam)/m:", glob_spk)
