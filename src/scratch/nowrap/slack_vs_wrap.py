"""Normalized MaxCL slack vs wrap excess (lead, 2026-10-19).  ratio = min_sigma S / (Ctot (m-1)/2), Ctot = (d+1)m - Omega.
Bins by E/m (E = canonical-lift wrap excess) and height; prints min ratio per bin.
usage: python slack_vs_wrap.py seed trials mmin mmax"""
import sys, random
from pmin_tile import apery, minimal_gens, tile
from descent_test import Svals, Eval
seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed); bins = {}
for tr in range(T):
    m = rng.randint(mmin, mmax); kk = rng.randint(2, 8)
    gens = [rng.randint(m+1, rng.choice([2, 3, 4])*m) for _ in range(kk)] if rng.random() < 0.5 else [m+rng.randint(1, max(2, m//rng.choice([2, 3, 5]))) for _ in range(kk)]
    if None in apery(m, gens): continue
    n, ap = minimal_gens(m, gens)
    if len(n) < 2: continue
    d = len(n); P = [g % m for g in n]
    for key in (lambda x: (sum(x), tuple(-t for t in x)), lambda x: (sum(x[i]*P[i] for i in range(d)), sum(x), tuple(-t for t in x))):
        D = list(tile(m, n, ap, key).values()); S, A = Svals(m, P, D); E = Eval(m, P, D)
        Om = sum(d+sum(y) for y in A); Ct = (d+1)*m-Om; ratio = min(S)/(Ct*(m-1)/2)
        b = (min(int(4*E/m), 8), min(max(sum(x) for x in D), 6))
        if b not in bins or ratio < bins[b][0]: bins[b] = (ratio, m, n)
for b in sorted(bins): print("E/m in [%.2f,%.2f) height %s: min ratio %.4f  (m=%d n=%s)" % (b[0]/4, (b[0]+1)/4, b[1] if b[1] < 6 else '>=6', bins[b][0], bins[b][1], bins[b][2]))
