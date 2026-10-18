# Wrap Lemma test: uniform ordered geometric splits (u, y-u), 0<u<y, weight (|y|-1)/s(y) each, s(y) = |[0,y]| - 2.
# B = weighted number of wrapped splits (r(u)+r(y-u) < r(0)).  Conjecture: B <= r(0) for all tiles and sigma.
# Also record the per-y bound B_y <= min(|y|-1, w*(delta_y+1)) and whether sum_y min(...) <= r(0).
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
def box(y):
    return [u for u in itertools.product(*[range(k+1) for k in y])]
def test(D, p, m, d):
    S = set(D); zero = tuple([0]*d)
    A = [y for y in D if sum(y) >= 2 and all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    splits = {}
    for y in A:
        us = [u for u in box(y) if u != zero and u != y]
        splits[y] = us
    phi = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
    worst = None
    for sg in range(m):
        r = {x: (phi[x] - sg) % m for x in D}; r0 = r[zero]
        B = Fr(0)
        for y in A:
            us = splits[y]; w = Fr(sum(y) - 1, len(us))
            for u in us:
                v = tuple(a - b for a, b in zip(y, u))
                if r[u] + r[v] < r0: B += w
        ex = B - r0
        if worst is None or ex > worst[0]: worst = (ex, sg, r0)
    return worst
if __name__ == '__main__':
    for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
        n = f = 0; ex = None
        for m in range(3, mmax + 1):
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    n += 1; w = test(D, p, m, d)
                    if w[0] > 0:
                        f += 1
                        if ex is None or w[0] > ex[0]: ex = (w[0], m, sorted(D), p, w[1], w[2])
        print('d', d, 'tiles', n, 'B > r0 fails', f, 'worst', ex, flush=True)
