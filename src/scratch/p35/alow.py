r"""Maximal cells below the conductor in a lex tile (lead, 2026-10-20).  For S: A_< = {y in A : w(y) < c},
LOW = sum_{y in A_<} (|y| + d) mu_y (mu = ceil((c - w)/m)), versus kappa_0, Dep, N.  Exact identity
W = N - kappa_0 + sum_x om(x) mu_x is asserted.  Usage: python alow.py m g1 g2 ... (one S) or -f FILE (lines 'm g1 ..')"""
import sys
sys.path.insert(0, '../p34')
from tile import build
def one(G):
    m = min(G); c, gens, M = build(m, G); D = list(M); d = len(gens); Ds = set(D); dl = [g % m for g in gens]
    up = lambda x, b, k=1: tuple(x[t] + k * (t == b) for t in range(d))
    w = {x: sum(a * b for a, b in zip(x, gens)) for x in D}
    mu = {x: max(0, -((w[x] - c) // m)) for x in D}
    A = [x for x in D if all(up(x, b) not in Ds for b in range(d))]
    om = {x: sum(x[b] + 1 for b in range(d) if up(x, b) not in Ds) for x in D}
    k0 = sum(sum((x[b] * dl[b]) % m for b in range(d)) // m for x in D)
    N = 0
    for x in D:
        for b in range(d):
            k = 0
            while up(x, b, k + 1) in Ds: k += 1
            if k >= 1 and (w[x] - c) % m > (w[up(x, b, k)] - c) % m: N += 1
    genus = sum(v // m for v in w.values()); W = (d + 1) * (c - genus) - c
    assert W == N - k0 + sum(om[x] * mu[x] for x in D), "level identity fails"
    Al = [y for y in A if w[y] < c]; LOW = sum((sum(y) + d) * mu[y] for y in Al)
    dep = sum(om[x] for x in D if x not in set(A)); ss = sum(max(0, sum(1 for t in x if t) - 1) for x in D)
    h = max(sum(x) for x in D)
    print("m=%d d=%d c=%d W=%d h=%d | |A|=%d |A_<|=%d LOW=%d kappa0=%d Dep=%d N=%d Ssupp=%d | LOW>=kappa0: %s" % (
        m, d, c, W, h, len(A), len(Al), LOW, k0, dep, N, ss, LOW >= k0))
if sys.argv[1] == '-f':
    for line in open(sys.argv[2]):
        if line.strip(): one(list(map(int, line.split())))
else: one(list(map(int, sys.argv[1:])))
