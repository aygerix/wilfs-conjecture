# List near-tight HCR tiles (3-D, all lattice tiles) with structural data.
import sys; sys.path.insert(0, 'src'); sys.path.insert(0, 'fwx')
from tile_enum import enumerate_tiles
from hcr_shape import hcr_shape
U = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]; add = lambda x, y: tuple(p + q for p, q in zip(x, y))
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    seen = set(); rows = []
    for r, D, poly in enumerate_tiles(m):
        k = frozenset(D)
        if k in seen: continue
        seen.add(k); v = hcr_shape(k)
        if v < float(sys.argv[3]):
            Ds = set(k); A = [y for y in Ds if all(add(y, u) not in Ds for u in U)]
            miss = [(a, b) for a in range(3) for b in range(a + 1, 3) if add(U[a], U[b]) not in Ds]
            L = [max(x[a] for x in Ds) + 1 for a in range(3)]
            rows.append((round(v, 4), r, 'two' + str(miss) if miss else 'NTF', 'L', L, 't', len(A), 'maxlens', sorted((sum(y) for y in A), reverse=True)))
    for row in sorted(rows)[:4]: print('m', m, *row)
