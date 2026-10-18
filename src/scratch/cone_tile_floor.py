# cone tiles: per direction c, floor maxima (y in Max, y + e_c >= q*), face corners of A_c inside quadrant [q_a,inf)x[q_b,inf),
# and distribution of q* (sorted).  usage: cone_tile_floor.py m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_cone_peel import qstars
from collections import Counter
def add(x, a): y = list(x); y[a] += 1; return tuple(y)
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        qdist = Counter(); fl = Counter(); fc = Counter(); worst = (0, None); n = 0
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            D = set(D); Q = qstars(D)
            if not Q: continue
            n += 1; q = Q[0]; qdist[tuple(sorted(q))] += 1
            Max = [y for y in D if all(add(y, a) not in D for a in range(3))]
            for c in range(3):
                a, b = [i for i in range(3) if i != c]
                nf = sum(1 for y in Max if y[c] == q[c] - 1 and y[a] >= q[a] and y[b] >= q[b])
                face = [y for y in D if y[c] == 0]
                nfc = sum(1 for y in face if y[a] >= q[a] and y[b] >= q[b] and add(y, a) not in D and add(y, b) not in D)
                fl[nf] += 1; fc[nfc] += 1
                if nf > worst[0]: worst = (nf, r, q, c)
        print(f'm={m} cone tiles {n}; q* (sorted) {dict(qdist.most_common(8))}; floor-max per direction {dict(sorted(fl.items()))}; '
              f'face corners in quadrant per direction {dict(sorted(fc.items()))}; worst {worst}', flush=True)
