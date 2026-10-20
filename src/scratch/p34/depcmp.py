r"""Compare MaxCL, DEP-CARRY and S1 slacks (lead, 2026-10-21) at every phase on given semigroup tiles (lex tile, all
units u): MaxCL slack = (d+1)M' - sum_A T r;  DEP slack = MaxCL slack + sum_{nonmax tops} |C|(m - r) - Lnm... i.e.
DEP slack = (d+1)M' - sum_{tops} |C| rt with rt = r on maximal tops, r - m on non-maximal tops;  S1 slack = (d+1)M'
+ m*BD - sum_{tops} |C| r.  Prints min over phases/units of each, normalized by m^2.  Usage: python depcmp.py m g1 g2 ..."""
import sys
from math import gcd
sys.path.insert(0, '.')
from tile import build
def slacks(m, D, delta, s):
    N = len(delta); Ds = set(D)
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    r = {x: (s + sum(a * b for a, b in zip(x, delta))) % m for x in D}
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    N1 = {x for x in D if all(up(x, b) in Ds for b in range(N))}
    BD = len(D) - len(N1) - len(mx)
    M2 = (N + 1) * m * (m - 1) // 2
    tops_all = 0; tops_max = 0; tops_dep = 0
    for b in range(N):
        for x in D:
            if x[b] == 0:
                y = x
                while up(y, b) in Ds: y = up(y, b)
                L = y[b] + 1; tops_all += L * r[y]
                if y in mx: tops_max += L * r[y]; tops_dep += L * r[y]
                else: tops_dep += L * (r[y] - m)
    return M2 - tops_max, M2 - tops_dep, M2 + m * BD - tops_all
def main(m, G):
    c, gens, M = build(m, G); D = list(M); N = len(gens); best = [None] * 3
    for u in range(1, m):
        if gcd(u, m) != 1: continue
        delta = [(u * g) % m for g in gens]
        for s in range(m):
            v = slacks(m, D, delta, s)
            for i in range(3):
                if best[i] is None or v[i] < best[i][0]: best[i] = (v[i], u, s)
    cs = (-c) % m; v0 = slacks(m, D, [g % m for g in gens], cs)
    print("S=<%d|%s> c=%d d=%d  min over (u,s)/m^2: MaxCL %.4f  DEP %.4f  S1 %.4f   at conductor phase: %s" % (m, gens, c, N, best[0][0] / m / m, best[1][0] / m / m, best[2][0] / m / m, tuple(round(x / m / m, 4) for x in v0)), flush=True)
if __name__ == '__main__':
    a = list(map(int, sys.argv[1:])); main(a[0], a[1:])
