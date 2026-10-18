# HCR+ (shape-only): the deficits v(t) = Lam - lam(t) of the m cells are pairwise distinct mod m and v(t) >= (m+1) ht(t).
# Lower bound for B = sum_t w(t) v(t) (w(t) = total length of columns topped at t) by the min-cost assignment of residue
# classes to cells, cost(t, r) = w(t) * (least integer >= (m+1) ht(t) congruent to r mod m).
#   HCR+ = minB / ((d-1) m (m-1)/2) >= 1 certifies Wilf.
import sys; sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
import numpy as np
from scipy.optimize import linear_sum_assignment
def hcrp_shape(D):
    D = sorted(set(D)); d = len(D[0]); m = len(D); Ds = set(D)
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]; add = lambda x, y: tuple(p + q for p, q in zip(x, y))
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, u)] + 1 for u in U if add(x, u) in Ds], default=0)
    w = {x: 0 for x in D}
    for x in D:
        for a in range(d):
            t = x
            while add(t, U[a]) in Ds: t = add(t, U[a])
            w[t] += 1
    C = np.zeros((m, m))
    for i, t in enumerate(D):
        base = (m + 1) * ht[t]
        for r in range(m): C[i, r] = w[t] * (base + ((r - base) % m))
    ri, ci = linear_sum_assignment(C)
    return C[ri, ci].sum() / ((d - 1) * m * (m - 1) / 2)
if __name__ == '__main__':
    from ns import NS
    from cl import factorizations_down_set
    from hcr import parts
    for g in sys.argv[1:]:
        s = NS.from_generators(list(map(int, g.split(','))))
        Pp, best = factorizations_down_set(s, 'grlex'); D = list(best.values())
        print(f'<{g}>: HCR {parts(s)[0]:.4f}  HCR+ {hcrp_shape(D):.4f}')
