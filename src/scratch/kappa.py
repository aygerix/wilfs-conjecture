# Exact per-cell form:  TOP'' <=> sum_{z not top} kappa(z) <= sum_{u top} (m - pi(u)),
#   kappa(z) = sum_{a: t_a z in X} pi(t_a z) - m - (d-1) psi(z).
import sys, itertools
from collections import defaultdict
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS, all_by_genus
from cl import factorizations_down_set
def kap(s, verbose=False):
    m, c = s.m, s.c; d = s.e - 1
    _, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}
    S = set(cells); pos = {x: ((w - c) % m) + 1 for x, w in cells.items()}
    top = {x for x, w in cells.items() if w >= c}
    by = defaultdict(lambda: [0, 0, 0]); K = []
    for z in cells:
        if z in top: continue
        ps = []
        for a in range(d):
            t = z
            while True:
                y = t[:a] + (t[a] + 1,) + t[a+1:]
                if y in S: t = y
                else: break
            if t in top: ps.append(pos[t])
        k = sum(ps) - m - (d - 1)*pos[z]; K.append((k, len(ps), z, pos[z], sorted(ps)))
        b = by[len(ps)]; b[0] += 1; b[1] += max(k, 0); b[2] += min(k, 0)
    budget = sum(m - pos[u] for u in top); tot = sum(k for k, *_ in K)
    assert (tot <= budget) == (sum(pos[u]*(d + sum(u)) for u in top) <= m*((d+1)*m + d - 1)//2)
    if verbose:
        print(s.P, f'm={m} tau={len(top)} budget={budget} total kappa={tot}', {k: tuple(v) for k, v in sorted(by.items())})
        print('   positive:', sorted([x for x in K if x[0] > 0], key=lambda x: -x[0])[:12])
    return tot, budget, by
if __name__ == '__main__':
    for g in ([36, 37, 42, 43], [49, 50, 56, 57], [15, 39, 41, 44], [19, 29, 41, 42], [29, 30, 35, 36], [22, 30, 31, 43], [30, 38, 59, 77]):
        kap(NS.from_generators(g), True)
