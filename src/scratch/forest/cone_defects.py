# Defect structure of the forest arguments on the cone class D = Cyl \ (q + N^3) restricted by proven tile constraints:
#  wall (A_c has <= q_c inner corners in [q_a,inf)x[q_b,inf)), floor (slice x_c = q_c-1 has <= 1 inner corner w >= (q_a,q_b)).
# Tripod elimination (decreasing |x|): excess e(x) = max(0, s(x)-1), s = #tops already seen.  qO elimination (increasing |x|):
# excess = max(0, s(x) - 1) for 2 tops.  qU: cycles.  Each defect is labeled by whether shared tops are floor cells.
import sys
sys.path.insert(0, sys.path[0])
from classify import gen
from collections import Counter, defaultdict
def add(x, a, d=1): y = list(x); y[a] += d; return tuple(y)
def ge(x, q): return all(x[i] >= q[i] for i in range(3))
def tile_ok(D, q, L):
    for c in range(3):
        a, b = [i for i in range(3) if i != c]
        nw = nf = 0
        for u in range(1, L[a] + 1):
            for v in range(1, L[b] + 1):
                w = [0, 0, 0]; w[a] = u; w[b] = v
                for hgt, cnt in ((0, 'w'), (q[c] - 1, 'f')):
                    w[c] = hgt; W = tuple(w)
                    if W in D or add(W, a, -1) not in D or add(W, b, -1) not in D: continue
                    if u >= q[a] and v >= q[b]:
                        if cnt == 'w': nw += 1
                        else: nf += 1
        if nw > q[c] or nf > 1: return False
    return True
def structure(D, q):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    def top(x, a):
        while add(x, a) in D: x = add(x, a)
        return x
    Max = {x for x in D if ht[x] == 0}
    floor = {y for y in D if any(ge(add(y, c), q) for c in range(3))}
    tri, qO, qU = [], [], []
    for x in D:
        if x in Max: continue
        tp = [top(x, a) for a in range(3)]; hs = [ht[z] for z in tp]; n = sum(1 for z in hs if z == 0)
        if n == 3: tri.append((x, tp))
        elif n == 2 and sum(hs) == 1:
            c = next(a for a in range(3) if hs[a] == 1)
            (qU if tp[c] == x else qO).append((x, tp, c))
    return ht, Max, floor, tri, qO, qU
def elim(cells, key, ntops):
    seen = set(); exc = 0; bad = []
    for x, tops in sorted(cells, key=key):
        s = sum(1 for z in tops if z in seen)
        if seen and s > 1: exc += s - 1; bad.append((x, tops))
        seen |= set(tops)
    return exc, bad, len(seen)
if __name__ == '__main__':
    M = int(sys.argv[1]); stats = Counter(); worst = {}
    for key, Cy, C in gen(M):
        L = [max(x[a] for x in Cy) + 1 for a in range(3)]
        for q in [(i, j, k) for (i, j, k) in Cy if i >= 1 and j >= 1 and k >= 1]:
            D = {x for x in Cy if not ge(x, q)}
            if len(D) > M or not tile_ok(D, q, L): continue
            ht, Max, floor, tri, qO, qU = structure(D, q)
            eT, badT, nT = elim([(x, tp) for x, tp in tri], lambda e: -sum(e[0]), 3)
            eO, badO, nO = elim([(x, [tp[a] for a in range(3) if a != c]) for x, tp, c in qO], lambda e: sum(e[0]), 2)
            stats['sets'] += 1
            for name, e, bad in (('T', eT, badT), ('O', eO, badO)):
                if e:
                    stats[name + 'defect_sets'] += 1
                    fl = sum(1 for x, tops in bad if any(z in floor for z in tops))
                    stats[name + 'with_floor_top'] += (fl == len(bad))
                    if name not in worst or e > worst[name][0]: worst[name] = (e, key, q, bad)
    print(dict(stats))
    for k, v in worst.items(): print(k, v)
