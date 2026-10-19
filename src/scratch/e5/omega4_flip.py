"""Adversary for OMEGA-4 (lead 2026-10-19): maximize Omega/m = sum_A (d+|y|)/m over complete 4-D lattice tiles.
Moves: (i) flip a maximal cell y to an addable cell z of D-{y} with the same label (stays a down-set tile);
(ii) restart from the grlex Apery tile of <m, m+r> for a perturbed r.  Simulated annealing on Omega.
Reports best Omega/m, its shape and the exact MaxCL min ratio.  usage: python omega4_flip.py seed m restarts steps"""
import sys, random, math
sys.path.insert(0, '/home/jmercedes/wilf/nowrap')
from pmin_tile import apery, minimal_gens, tile
seed, m, R, ST = map(int, sys.argv[1:5]); rng = random.Random(seed); d = 4
E = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, e: tuple(p+q for p, q in zip(x, e)); sub = lambda x, e: tuple(p-q for p, q in zip(x, e))
def start(r):
    gens = [m+x for x in r]
    if len(set(x % m for x in gens)) < 4 or None in apery(m, gens): return None
    n, ap = minimal_gens(m, gens)
    if len(n) != 4: return None
    return set(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values()), [g % m for g in n]
def maxcells(D): return [y for y in D if all(add(y, e) not in D for e in E)]
def omega(D): return sum(d+sum(y) for y in maxcells(D))
def flips(D, P):
    A = maxcells(D); out = []
    for y in A:
        Dy = D - {y}; L = sum(y[i]*P[i] for i in range(d)) % m
        cand = set()
        for x in Dy:
            for e in E:
                z = add(x, e)
                if z in Dy or z == y: continue
                if all(sub(z, f) in Dy for f, zi in zip(E, z) if zi > 0) and sum(z[i]*P[i] for i in range(d)) % m == L: cand.add(z)
        for z in cand: out.append((y, z))
    return out
best = None
for rs in range(R):
    st = None
    while st is None: st = start(sorted(rng.sample(range(1, m), 4)))
    D, P = st; cur = omega(D)
    if best is None or cur > best[0]: best = (cur, set(D), list(P))
    nfl = 0
    for it in range(ST):
        T = 2.0*(0.01/2.0)**(it/ST)
        fl = flips(D, P)
        if not fl: break
        nfl += 1
        y, z = rng.choice(fl); D2 = (D - {y}) | {z}; o2 = omega(D2)
        if o2 >= cur or rng.random() < math.exp((o2-cur)/(T*m*0.01)): D, cur = D2, o2
        if best is None or cur > best[0]: best = (cur, set(D), list(P))
Om, D, P = best; A = maxcells(D); M1 = m*(m-1)//2
S = min((d+1)*M1-sum((d+sum(y))*((sum(y[i]*P[i] for i in range(d))-sg) % m) for y in A) for sg in range(m))
Ct = (d+1)*m-Om
lev = {}
for y in A: lev[sum(y)] = lev.get(sum(y), 0)+1
print("m=%d best Omega/m=%.3f P=%s height=%d t=%d levels(A)=%s MaxCL_ratio=%.3f" % (m, Om/m, P, max(sum(x) for x in D), len(A), sorted(lev.items()), S/(Ct*(m-1)/2)), flush=True)
