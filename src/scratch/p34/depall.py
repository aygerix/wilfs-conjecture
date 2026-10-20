r"""DEP-ALL extremals (lead, 2026-10-21): over all lattice tiles (D, delta) of N^d (all down-sets of size m, all
delta in [1,m)^d with x -> x.delta mod m bijective) and every phase rho: min of V(rho) + Dep, where
V(rho) = (m-1)/2 - f(rho)/m, f(rho) = sum_t omega(t) r_rho(t) - d M'.  DEP-ALL claims V + Dep >= 0.
Reports per (d, m): #tiles, min V+Dep, #(tile,phase) at the min, the first minimizers, #equality (V+Dep=0).
Usage: python depall.py d MMIN MMAX"""
import sys, itertools
sys.path.insert(0, '.')
from subadd_lp import downsets
def ds4(m):
    D3 = {0: [frozenset()]}
    for k in range(1, m + 1): D3[k] = [frozenset(D) for D in downsets(3, k)]
    def chains(rem, prev):
        if rem == 0: yield []; return
        for k in range(1, rem + 1):
            for L in D3[k]:
                if prev is None or L <= prev:
                    for rest in chains(rem - k, L): yield [L] + rest
    for ch in chains(m, None): yield [(i,) + x for i, L in enumerate(ch) for x in L]
def omega(D, N):
    Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    om = {x: 0 for x in D}
    for b in range(N):
        for x in D:
            if up(x, b) not in Ds: om[x] += x[b] + 1
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    return om, sum(v for x, v in om.items() if x not in mx)
N, MMIN, MMAX = map(int, sys.argv[1:4])
for m in range(MMIN, MMAX + 1):
    gen = ds4(m) if N == 4 else downsets(N, m)
    ntile = 0; best = None; nbest = 0; neq = 0; ex = []
    Mp = m * (m - 1) // 2
    for D in gen:
        if any(sum(1 for t in x if t) == 0 for x in D[1:]): pass
        # skip down-sets not using every direction (they are tiles of lower d)
        if any(all(x[b] == 0 for x in D) for b in range(N)): continue
        om, dep = omega(D, N)
        for delta in itertools.product(range(1, m), repeat=N):
            lab = [sum(a * b for a, b in zip(x, delta)) % m for x in D]
            if len(set(lab)) != m: continue
            ntile += 1
            wt = [0] * m
            for x, l in zip(D, lab): wt[l] += om[x]
            for rho in range(m):
                f = sum(wt[l] * ((l + rho) % m) for l in range(m)) - N * Mp
                v2 = Mp - f + m * dep          # = m (V + Dep)
                assert v2 % m == 0
                v = v2 // m
                if v == 0: neq += 1
                if best is None or v < best: best = v; nbest = 0; ex = []
                if v == best:
                    nbest += 1
                    if len(ex) < 3: ex.append((sorted(D) if m <= 12 else len(D), delta, rho, dep))
    print("d=%d m=%d tiles %d  min V+Dep %s  (#%d)  equality cases %d  ex %s" % (N, m, ntile, best, nbest, neq, ex), flush=True)
