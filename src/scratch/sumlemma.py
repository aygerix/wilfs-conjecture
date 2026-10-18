# Sumset Lemma SL(t): for every tile, sigma, and t in [0, m):
#   sum over maximal y (|y|>=2), ordered geometric splits y = u + v (u,v != 0) with r(u)+r(v) <= t, of w_y  <=  t + 1,
#   w_y = (|y|-1)/(|[0,y]|-2).   For t < r(0) this is WL-t (all such splits wrap).  Report fails split by t<r0 / t>=r0.
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
def box(y): return list(itertools.product(*[range(k+1) for k in y]))
def check(D, p, m, d):
    S = set(D); zero = tuple([0]*d)
    A = [y for y in D if sum(y) >= 2 and all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    spl = []
    for y in A:
        us = [u for u in box(y) if u != zero and u != y]; w = Fr(sum(y) - 1, len(us))
        for u in us: spl.append((u, tuple(a - b for a, b in zip(y, u)), w))
    phi = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
    lo = hi = 0; worst = None
    for sg in range(m):
        r = {x: (phi[x] - sg) % m for x in D}; r0 = r[zero]
        mass = [Fr(0)]*(2*m)
        for u, v, w in spl: mass[r[u] + r[v]] += w
        acc = 0
        for t in range(m):
            acc += mass[t]
            if acc > t + 1:
                if t < r0: lo += 1
                else: hi += 1
                if worst is None or acc - t - 1 > worst[0]: worst = (acc - t - 1, sg, t, r0)
                break
    return lo, hi, worst
if __name__ == '__main__':
    for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
        n = L = Hh = 0; ex = None
        for m in range(3, mmax + 1):
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    n += 1; lo, hi, w = check(D, p, m, d)
                    L += lo > 0; Hh += hi > 0
                    if hi and (ex is None or w[0] > ex[0]): ex = (w[0], m, sorted(D), p, w[1:])
        print('d', d, 'tiles', n, 'fails with t<r0', L, 'fails with t>=r0', Hh, 'worst', ex, flush=True)
