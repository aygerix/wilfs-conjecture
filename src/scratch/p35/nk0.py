r"""N(sigma_c), kappa_0, Dep, Sigma_supp of the lex tile of S, and the L7' slack N + Dep - kappa_0 (lead, 2026-10-20).
kappa_0 = sum_x floor(sum_b <x_b delta_b> / m); N = #{(x,b): k_b(x) >= 1, r(x) > r(t_b(x))}, r = <w - c>.
Checks the identity W >= Dep - kappa_0 + N against the brute-force W.  Usage: python nk0.py m g1 g2 ..."""
import sys
sys.path.insert(0, '../p34')
from tile import build
from tcldich import stats
G = list(map(int, sys.argv[1:])); m = min(G)
c, gens, M = build(m, G); D = list(M); d = len(gens); Ds = set(D); dl = [g % m for g in gens]
up = lambda x, b, k=1: tuple(x[t] + k * (t == b) for t in range(d))
w = {x: sum(a * b for a, b in zip(x, gens)) for x in D}
k0 = sum(sum((x[b] * dl[b]) % m for b in range(d)) // m for x in D)
N = 0
for x in D:
    for b in range(d):
        k = 0
        while up(x, b, k + 1) in Ds: k += 1
        if k >= 1 and (w[x] - c) % m > (w[up(x, b, k)] - c) % m: N += 1
v, dep, ss = stats(m, D, dl)
genus = sum(x // m for x in w.values()); W = (d + 1) * (c - genus) - c
print("m=%d d=%d c=%d W=%d Dep=%d Ssupp=%d kappa0=%d N=%d  L7'-slack N+Dep-kappa0=%d  bound Dep-k0+N=%d <= W: %s  mu=%d" % (
    m, d, c, W, dep, ss, k0, N, N + dep - k0, dep - k0 + N, dep - k0 + N <= W, ss - dep))
