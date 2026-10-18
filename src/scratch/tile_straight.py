# NON-two-face tiles: straight-run quantities.  r_b(t) = max{j : t + j e_b in D}.  Hs = sum_{(x,a)} max_{b != a} r_b(t_a x)
# (<= H), Pi = sum_{(x,a)} sum_{b != a} r_b(t_a x) (H >= Pi/2).  usage: m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
for m in map(int, sys.argv[1:]):
    wHs = wPi = None
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        def top(x, i):
            while add(x, i) in D: x = add(x, i)
            return x
        def run(t, b):
            j = 0
            while add(t, b) in D: t = add(t, b); j += 1
            return j
        Hs = Pi = 0
        for x in D:
            for a in range(3):
                t = top(x, a); rs = [run(t, b) for b in range(3) if b != a]
                Hs += max(rs); Pi += sum(rs)
        if wHs is None or Hs - m + 1 < wHs[0]: wHs = (Hs - m + 1, r)
        if wPi is None or Pi - 2*m + 2 < wPi[0]: wPi = (Pi - 2*m + 2, r)
    print(f'm={m}: min Hs-(m-1) {wHs}; min Pi-2(m-1) {wPi}', flush=True)
