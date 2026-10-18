# Locate the dimension threshold of Tile-CL with core+spike tiles: core C = 2-D (or 1-D) down-set with phi injective,
# k = m - |C| single-cell spikes in new directions (d = d0 + k).  Random search over m, core shapes, p.
import sys, random
sys.path.insert(0, 'src/scratch')
from spikes import tile_slack, with_spikes
def young(rng, n, maxw):
    # random partition of n as a Young diagram (row lengths non-increasing)
    rows = []; left = n
    while left > 0:
        w = rng.randint(1, min(left, rows[-1] if rows else maxw)); rows.append(w); left -= w
    return [(x, y) for y, w in enumerate(rows) for x in range(w)]
rng = random.Random(int(sys.argv[1])); K = int(sys.argv[2]); N = int(sys.argv[3]); MMAX = int(sys.argv[4])
fails = 0; tried = 0; worst = (0, None)
while tried < N:
    m = rng.randint(K + 3, MMAX); n = m - K
    C = young(rng, n, rng.randint(1, n))
    p1, p2 = rng.randrange(1, m), rng.randrange(1, m)
    if len({(x*p1 + y*p2) % m for x, y in C}) != n: continue
    tried += 1
    D, p = with_spikes(C, (p1, p2), m)
    sl = tile_slack(D, p, m); mn = min(sl)
    if mn < 0:
        fails += 1
        if fails <= 3: print('FAIL d =', len(p), 'm', m, 'core', sorted(C), 'p', p, 'min slack', mn, flush=True)
    if mn < worst[0]: worst = (mn, (m, len(p)))
print(f'k={K} spikes: tried {tried}, Tile-CL fails {fails}, worst {worst}')
