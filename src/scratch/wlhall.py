# Wrap Lemma refinement (WL-Hall): demands B_y (uniform-split wrap mass of maximal y) can be assigned to distinct
# top-window cells inside the box Q_y = [0,y] (each cell capacity 1).  Checks (i) B_y <= |W ∩ Q_y| per y and
# (ii) the full transportation feasibility (exact LP via max-flow with Fractions -> use networkx-free greedy on Hall
# over all subsets when #wrapped y <= 12).
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
def box(y): return list(itertools.product(*[range(k+1) for k in y]))
def check(D, p, m, d):
    S = set(D); zero = tuple([0]*d)
    A = [y for y in D if sum(y) >= 2 and all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    boxes = {y: box(y) for y in A}
    phi = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
    f1 = f2 = 0
    for sg in range(m):
        r = {x: (phi[x] - sg) % m for x in D}; r0 = r[zero]
        if r0 == 0: continue
        Wc = {x for x in D if r[x] >= m - r0}
        By = {}; nb = {}
        for y in A:
            us = [u for u in boxes[y] if u != zero and u != y]; w = Fr(sum(y) - 1, len(us))
            N = sum(1 for u in us if r[u] + r[tuple(a - b for a, b in zip(y, u))] < r0)
            if N:
                By[y] = w*N; nb[y] = set(boxes[y]) & Wc
                if By[y] > len(nb[y]): f1 += 1
        ys = list(By)
        if len(ys) <= 12:
            for k in range(2, len(ys) + 1):
                for Y in itertools.combinations(ys, k):
                    if sum(By[y] for y in Y) > len(set().union(*[nb[y] for y in Y])): f2 += 1; break
                else: continue
                break
    return f1, f2
if __name__ == '__main__':
    for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
        n = F1 = F2 = 0; ex = None
        for m in range(3, mmax + 1):
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    n += 1; f1, f2 = check(D, p, m, d)
                    F1 += f1 > 0; F2 += f2 > 0
                    if (f1 or f2) and ex is None: ex = (m, sorted(D), p)
        print('d', d, 'tiles', n, 'per-box fails', F1, 'Hall fails', F2, 'first', ex, flush=True)
