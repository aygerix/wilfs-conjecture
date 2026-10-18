# Pairwise Groebner-vector relaxation of the tile condition (necessary, lattice-free).
# A 3-D lattice tile D = Cyl(h,F,G) \ (q + N^3) has, for each non-axis inner corner of a face, a lattice vector
#   A3 corner (i, h(i)):  (i, h(i), -t),  0 <= t < L3      A2 corner (i, F(i)):  (i, -s, F(i)),  0 <= s < L2
#   A1 corner (j, G(j)):  (-u, j, G(j)),  0 <= u < L1      and q* (if present)          [cylinder lemma (a), (b)]
# Every nonzero lattice vector v satisfies NOT(v+ in D and v- in D) (D is a fundamental domain, down-set).
# feasible(): is there an assignment of the unknowns t, s, u such that all vectors and all pairwise differences and sums
# satisfy this?  (Within one face, differences give the Lattice Corner Lemma; with q* they give the Wall Lemma.)
import sys, itertools
sys.path.insert(0, 'src/scratch')
from is_tile import build
def corners(seq):
    return [(i, seq[i]) for i in range(1, len(seq)) if seq[i - 1] > seq[i] >= 1]
def feasible(h, F, G, q, sums=True, want_all=False):
    D = build(h, F, G, q); L1, L2, L3 = len(h), len(G), G[0]
    def bad(v):
        if v == (0, 0, 0): return True   # two distinct items mapped to the same lattice point
        p = tuple(max(c, 0) for c in v); n = tuple(max(-c, 0) for c in v)
        return p in D and n in D
    items = []   # (kind, corner, domain size)
    for (i, hi) in corners(h): items.append((lambda t, i=i, hi=hi: (i, hi, -t), L3))
    for (i, Fi) in corners(F): items.append((lambda s, i=i, Fi=Fi: (i, -s, Fi), L2))
    for (j, Gj) in corners(G): items.append((lambda u, j=j, Gj=Gj: (-u, j, Gj), L1))
    fixed = [tuple(q)] if q else []
    for f in fixed:
        if bad(f): return False
    vals = [None] * len(items); sols = []
    def ok(k):
        v = items[k][0](vals[k])
        if bad(v): return False
        for f in fixed:
            if bad(tuple(a - b for a, b in zip(v, f))) or (sums and bad(tuple(a + b for a, b in zip(v, f)))): return False
        for l in range(k):
            w = items[l][0](vals[l])
            if bad(tuple(a - b for a, b in zip(v, w))) or (sums and bad(tuple(a + b for a, b in zip(v, w)))): return False
        return True
    def rec(k):
        if k == len(items):
            sols.append(tuple(vals)); return not want_all
        for x in range(items[k][1]):
            vals[k] = x
            if ok(k) and rec(k + 1): return True
        vals[k] = None
        return False
    rec(0)
    return (len(sols) > 0) if not want_all else sols
if __name__ == '__main__':
    import re
    if sys.argv[1] == 'dump':
        tot = surv = 0; ex = []
        for line in open(sys.argv[2]):
            mm = re.search(r'h=([\d,]+) F=([\d,]+) G=([\d,]+) q=\((\d+),(\d+),(\d+)\)', line)
            if not mm: continue
            h, F, G = [tuple(map(int, mm.group(k).split(','))) for k in (1, 2, 3)]; q = tuple(map(int, mm.group(4, 5, 6)))
            tot += 1
            if feasible(h, F, G, q): surv += 1; ex.append(line.strip())
        print(f'{sys.argv[2]}: {tot} sets, {surv} pass the pairwise relaxation')
        for e in ex[:15]: print('  ', e)
    else:
        print(feasible(eval(sys.argv[1]), eval(sys.argv[2]), eval(sys.argv[3]), eval(sys.argv[4])))
