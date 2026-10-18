# WL-t: for every t in [0, r0): sum over maximal y with delta_y = r(y)+r0-m in [0,t] of B_y  <=  t+1.
# Also WL-slot: wrapped ordered split (u,v) of y may use slots {r(u), r(v), delta_y}; is there an assignment with
# every slot load <= 1?  (checked by LP-free greedy Hall test on slots: for every set of slots J, the total weight of
# splits whose three slots all lie in J must be <= |J|; tested on all J that are unions of slot-triples, small cases.)
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
def box(y): return list(itertools.product(*[range(k+1) for k in y]))
def check(D, p, m, d):
    S = set(D); zero = tuple([0]*d)
    A = [y for y in D if sum(y) >= 2 and all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    boxes = {y: [u for u in box(y) if u != zero and u != y] for y in A}
    phi = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
    bad = 0
    for sg in range(m):
        r = {x: (phi[x] - sg) % m for x in D}; r0 = r[zero]
        if r0 == 0: continue
        mass = [Fr(0)]*r0
        for y in A:
            dl = r[y] + r0 - m
            if dl < 0: continue
            w = Fr(sum(y) - 1, len(boxes[y]))
            N = sum(1 for u in boxes[y] if r[u] + r[tuple(a - b for a, b in zip(y, u))] < r0)
            mass[dl] += w*N
        acc = 0
        for t in range(r0):
            acc += mass[t]
            if acc > t + 1: bad += 1; break
    return bad
if __name__ == '__main__':
    for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
        n = F = 0; ex = None
        for m in range(3, mmax + 1):
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    n += 1; b = check(D, p, m, d)
                    if b:
                        F += 1
                        if ex is None: ex = (m, sorted(D), p)
        print('d', d, 'tiles', n, 'WL-t fails', F, 'first', ex, flush=True)
