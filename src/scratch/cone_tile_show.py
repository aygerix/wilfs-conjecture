# show a tile (m, r) level by level along x3 with labels (M, T, uK/oK, h) and q*
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch'); sys.path.insert(0, 'src/scratch/forest')
from tile_enum import tile_for_weight, enumerate_tiles
from tile_cone_peel import qstars
from gdraw import labels
m = int(sys.argv[1]); r = eval(sys.argv[2]); which = int(sys.argv[3]) if len(sys.argv) > 3 else None
for rr, D, poly in enumerate_tiles(m):
    if tuple(rr) != tuple(r): continue
    D = set(D); Q = qstars(D)
    if which is not None and (not Q or Q[0] != tuple(eval(sys.argv[3]) if False else Q[0])): pass
    lab = labels(D)
    L = [max(x[a] for x in D) + 1 for a in range(3)]
    print('r', rr, 'q*', Q, 'extents', L, 'counts', {k: sum(1 for v in lab.values() if v.strip() == k) for k in ('M', 'T')},
          'Q', sum(1 for v in lab.values() if v[0] in 'uo'))
    for v in range(L[2]):
        print(' level x3=%d' % v)
        for y in range(L[1] - 1, -1, -1):
            row = [lab.get((x, y, v), ' .') for x in range(L[0])]
            if any(c != ' .' for c in row): print('   ' + ' '.join(row))
    print()
