"""Q7: for fixed (p, s), minimize G(D) = f(s) - (d-1)m(m-1)/2 over all down-set tiles D of ker(phi).
Report: distribution of min_D G over (p,s); which tiles attain it."""
import sys, itertools
from collections import defaultdict, Counter
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets, Tvals
d = int(sys.argv[1]); m = int(sys.argv[2])
target = (d-1)*m*(m-1)//2
tiles = defaultdict(list)   # p -> list of (D, T, res)
for D in downsets(m, d):
    Dl = sorted(D)
    if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
    T = Tvals(D, d)
    for p in itertools.product(range(m), repeat=d):
        res = [sum(x*y for x, y in zip(n, p)) % m for n in Dl]
        if len(set(res)) != m: continue
        tiles[p].append((Dl, T, res))
mins = Counter(); ntiles = Counter()
for p, L in tiles.items():
    ntiles[len(L)] += 1
    for s in range(m):
        Gs = []
        for Dl, T, res in L:
            Gs.append(sum(T[n]*((s - r) % m) for n, r in zip(Dl, res)) - target)
        mins[min(Gs)//m] += 1
print('d', d, 'm', m, '#p with tiles', len(tiles), 'tiles-per-p histogram', dict(sorted(ntiles.items())))
print('min over tiles of G/m, histogram over (p,s):', dict(sorted(mins.items())))
