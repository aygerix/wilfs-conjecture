"""GW slack for D = {x in N^a : |x| <= deg} (full simplex), m = |D|, all n_a in (m, 2m), residues complete.
Reports min W = d*ell - g per (a,deg) and the band profile of minimizers.  Run on fejer."""
import itertools, sys
from math import comb
a, deg = int(sys.argv[1]), int(sys.argv[2])
cells = [x for x in itertools.product(range(deg+1), repeat=a) if sum(x) <= deg]
m = len(cells)
best = None; cnt = 0; hist = {}
for n in itertools.combinations(range(m+1, 2*m), a):
    V = [sum(xi*ni for xi, ni in zip(x, n)) for x in cells]
    if len({v % m for v in V}) != m: continue
    M = max(V); K = M // m
    g = sum(v // m for v in V); ell = sum((M - v) // m for v in V)
    W = a*ell - g; cnt += 1
    hist[K] = min(hist.get(K, 10**9), W)
    if best is None or W < best[0]: best = (W, n, K, M)
print(f"a={a} deg={deg} m={m} residue-complete n-tuples={cnt} minW by K={dict(sorted(hist.items()))} best={best}")
