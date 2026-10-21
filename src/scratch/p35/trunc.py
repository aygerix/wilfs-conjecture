r"""Truncated level bounds (lead, 2026-10-20).  For S with multiplicity m, conductor c = q m - rho, d = e - 1 and lex tile
D (tile.build): mu_x = ceil((c - w(x))/m)^+ is the number of elements of S below c in the class of w(x), ell = sum mu_x.
Truncations: U = (d+1)(q + sum_b mu(e_b)) - c (classes of 0 and of the generators only), W2 = (d+1) sum_{|x|<=2} mu_x - c.
HALF: if 2 g_b <= c + m - 1 for every generator b, then W >= U >= q (C(d+2,2) - m) - [q odd] C(d+1,2) + rho (+ rho = 0
refinement).  Asserts W >= W2 >= U and, under HALF, U >= the closed bound.  Also prints the SUPP data (Sigma_supp, Dep,
kappa0, N).  Usage: python trunc.py m g1 .. | python trunc.py -f FILE (lines 'm g1 ..' or containing 'gens=[..]')
"""
import sys, re
from math import comb
sys.path.insert(0, '../p34')
from tile import build
def one(G, tag=''):
    m = min(G); res = build(m, G)
    if res is None: return None
    c, gens, M = res; D = list(M); d = len(gens); Ds = set(D); dl = [g % m for g in gens]
    if c <= 0: return None
    up = lambda x, b, k=1: tuple(x[t] + k * (t == b) for t in range(d))
    w = {x: sum(a * b for a, b in zip(x, gens)) for x in D}
    mu = {x: max(0, -((w[x] - c) // m)) for x in D}
    q = -(-c // m); rho = q * m - c
    ell = sum(mu.values()); W = (d + 1) * ell - c
    unit = [tuple(int(t == b) for t in range(d)) for b in range(d)]
    U = (d + 1) * (q + sum(mu[u] for u in unit)) - c
    W2 = (d + 1) * sum(mu[x] for x in D if sum(x) <= 2) - c
    assert W >= W2 >= U, (G, W, W2, U)
    nbig = sum(1 for g in gens if 2 * g > c + m - 1)
    half = q * (comb(d + 2, 2) - m) - (q % 2) * (comb(d + 1, 2) if rho else 0) + rho
    if nbig == 0: assert U >= half, (G, U, half)
    A = [x for x in D if all(up(x, b) not in Ds for b in range(d))]; As = set(A)
    om = {x: sum(x[b] + 1 for b in range(d) if up(x, b) not in Ds) for x in D}
    dep = sum(om[x] for x in D if x not in As); ss = sum(max(0, sum(1 for t in x if t) - 1) for x in D)
    k0 = sum(sum((x[b] * dl[b]) % m for b in range(d)) // m for x in D)
    h = max(sum(x) for x in D)
    print("%s m=%d d=%d c=%d q=%d rho=%d W=%d W2=%d U=%d | nbig=%d C2-m=%d half=%s | h=%d Ssupp-Dep=%d k0-Dep=%d" % (
        tag, m, d, c, q, rho, W, W2, U, nbig, comb(d + 2, 2) - m, half if nbig == 0 else '-', h, ss - dep, k0 - dep),
        flush=True)
    return dict(m=m, d=d, c=c, q=q, W=W, W2=W2, U=U, nbig=nbig, h=h, mu=ss - dep, mk=k0 - dep)
if __name__ == '__main__':
    if sys.argv[1] == '-f':
        for line in open(sys.argv[2]):
            mm = re.search(r'gens=\[([0-9, ]+)\]', line)
            if mm:
                G = [int(t) for t in mm.group(1).split(',')]; mq = re.search(r'm=(\d+)', line); G = [int(mq.group(1))] + G
            elif line.strip() and line.split()[0].isdigit(): G = list(map(int, line.split()))
            else: continue
            one(G, sys.argv[2])
    else: one(list(map(int, sys.argv[1:])))
