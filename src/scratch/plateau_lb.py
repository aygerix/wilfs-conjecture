# Plateau lower bound.  For direction a and a layer x_b = k (2-D slice in coords (a, c)), each a-row of the slice has
# its end t; up-paths from t inside that layer only move in +c, so ht(t) >= pl(t) := #consecutive rows above (in c)
# whose length is >= the row length.  B_{a|b} := sum_layers sum_rows len * pl.  H_a >= max(B_{a|b}, B_{a|c}).
# LB2 := sum_a max(B_{a|b}, B_{a|c}).  Report min LB2 - (m-1) over complete enumeration (non-two-face).  usage: m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
from heightH import H_of
def B(D, a, b):
    c = 3 - a - b
    L = [max(x[i] for x in D) + 1 for i in range(3)]
    tot = 0
    for k in range(L[b]):
        rows = []
        for z in range(L[c]):
            n = 0
            while True:
                x = [0, 0, 0]; x[a] = n; x[b] = k; x[c] = z
                if tuple(x) in D: n += 1
                else: break
            rows.append(n)
        for z, r in enumerate(rows):
            if r == 0: continue
            pl = 0
            while z + pl + 1 < len(rows) and rows[z + pl + 1] >= r: pl += 1
            tot += r * pl
    return tot
def LB2(D):
    return sum(max(B(D, a, b), B(D, a, 3 - a - b)) for a in range(3) for b in [(a + 1) % 3])
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        worst = None; fails = 0
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            D = set(D); v = LB2(D) - (m - 1)
            fails += v < 0
            if worst is None or v < worst[0]: worst = (v, r, H_of(D) - (m - 1))
        print(f'm={m}: LB2 fails {fails}; min LB2-(m-1) {worst}', flush=True)
