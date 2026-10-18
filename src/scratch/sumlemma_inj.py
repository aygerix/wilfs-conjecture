# Does the Sumset Lemma SL(t) need the tile property?  Test on down-sets D with phi injective mod m (|D| < m):
#   sum_{y maximal, |y|>=2} w_y #{u in [0,y]\{0,y} : r(u)+r(y-u) <= t}  <=  t+1   for all sigma, t.
import sys, itertools, random
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
    for sg in range(m):
        r = {x: (phi[x] - sg) % m for x in D}
        mass = [Fr(0)]*(2*m)
        for u, v, w in spl: mass[r[u] + r[v]] += w
        acc = 0
        for t in range(m):
            acc += mass[t]
            if acc > t + 1: return (sg, t, acc)
    return None
if __name__ == '__main__':
    for d, size, mmax in [(1, 6, 30), (2, 6, 14), (2, 8, 16), (3, 7, 14)]:
        n = f = 0; ex = None
        for D in downsets(size, d):
            if any(all(x[a] == 0 for x in D) for a in range(d)): continue
            for m in range(size + 1, mmax + 1):
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != size: continue
                    n += 1; res = check(D, p, m, d)
                    if res:
                        f += 1
                        if ex is None: ex = (sorted(D), p, m, res)
        print('d', d, '|D|', size, 'm <=', mmax, 'injective instances', n, 'SL fails', f, 'first', ex, flush=True)
