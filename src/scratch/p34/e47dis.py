r"""Dissect a Tile-CL failure (lead, 2026-10-21): for S = <m, gens>, list V(rho) at every phase, and at the worst phase
the cells, labels, omega, tops, the inversions N and the overflow cells.  Usage: python e47dis.py m g1 .. gk"""
import sys
sys.path.insert(0, '.')
from tile import build
from depcarry import carry
m, *G = map(int, sys.argv[1:]); c, gens, M = build(m, G); N = len(gens); D = list(M); Ds = set(D)
delta = [g % m for g in gens]; up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
V = [s + carry(m, D, delta, s)[0] for s in range(m)]
dep = carry(m, D, delta, 0)[2]
print("m=%d gens=%s c=%d d=%d Dep=%d  V(rho):" % (m, gens, c, N, dep), V, " conductor phase", (-c) % m)
s = min(range(m), key=lambda t: V[t])
mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
def top(x, a):
    k = 0
    while up(x, a) in Ds: x = up(x, a); k += 1
    return x, k
lab = {x: (s + sum(p * q for p, q in zip(x, delta))) % m for x in D}
print("worst phase", s, "V =", V[s])
for x in sorted(D, key=lambda y: lab[y]):
    om = sum(x[b] + 1 for b in range(N) if up(x, b) not in Ds)
    invs = [a for a in range(N) if top(x, a)[1] and lab[x] > lab[top(x, a)[0]]]
    eps = sum((x[a] * delta[a]) % m for a in range(N)) // m
    nm = [b for b in range(N) if up(x, b) not in Ds] if x not in mx else 'MAX'
    print("  lab %2d  x=%s w=%3d om=%d eps=%d inv_dirs=%s top-in-dirs=%s" % (lab[x], x, M[x], om, eps, invs, nm))
