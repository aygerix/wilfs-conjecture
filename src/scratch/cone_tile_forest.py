# Cone tiles (non-two-face, q* present): forest excesses and where Lemma S / P / QF break.
# Per m: max of t-C, 2Tri-t, qO-t, qU-t, LHS-4C, LHS-5C; #cross-direction shared tops (Lemma S violations, tripods+qO);
# floor maxima nf = #{y in Max : y + e_c >= q* for some c}; tripods with a top on the floor; examples.
# usage: cone_tile_forest.py m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from cht_corners import corners
from tile_cone_peel import qstars
from collections import defaultdict
def add(x, a, d=1): y = list(x); y[a] += d; return tuple(y)
def analyze(D, q):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    def top(x, a):
        while add(x, a) in D: x = add(x, a)
        return x
    Max = {x for x in D if ht[x] == 0}
    tri, qU, qO = [], [], []
    for x in D:
        if x in Max: continue
        tp = [top(x, a) for a in range(3)]; hs = [ht[z] for z in tp]
        n = sum(1 for z in hs if z == 0)
        if n == 3: tri.append((x, tp))
        elif n == 2 and sum(hs) == 1:
            c = next(a for a in range(3) if hs[a] == 1)
            (qU if tp[c] == x else qO).append((x, tp, c))
    floor = {y for y in Max if any(all(add(y, c)[i] >= q[i] for i in range(3)) for c in range(3))}
    # cross-direction sharing among tripods + qO (cells with all forward neighbours in D)
    inc = defaultdict(set)
    for x, tp in tri:
        for a in range(3): inc[tp[a]].add(a)
    for x, tp, c in qO:
        for a in range(3):
            if a != c: inc[tp[a]].add(a)
    sviol = [y for y, s in inc.items() if len(s) > 1]
    return len(Max), len(tri), len(qU), len(qO), floor, sviol, tri
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        best = {}; n = 0; ex = {}
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            D = set(D); Q = qstars(D)
            if not Q: continue
            n += 1; q = Q[0]
            t, tr, qu, qo, floor, sv, tri = analyze(D, q); C = corners(D)
            lhs = 2*t + 2*tr + qu + qo
            fl_tri = sum(1 for x, tp in tri if any(z in floor for z in tp))
            vals = {'t-C': t - C, '2Tri-t': 2*tr - t, 'qO-t': qo - t, 'qU-t': qu - t, 'LHS-4C': lhs - 4*C, 'LHS-5C': lhs - 5*C,
                    'Sviol': len(sv), 'floorMax': len(floor), 'floorTri': fl_tri, 'Tri': tr, 'C': C}
            for k, v in vals.items():
                if k not in best or v > best[k]: best[k] = v; ex[k] = (r, q)
        print(f'm={m} cone tiles {n}: ' + ' '.join(f'{k} {best[k]}' for k in best), flush=True)
        print('   ex:', {k: ex[k] for k in ('LHS-4C', '2Tri-t', 'Sviol', 'floorMax')}, flush=True)
