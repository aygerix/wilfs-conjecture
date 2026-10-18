# NON-two-face tiles: number of non-axis inner corners per face, presence of q*, mu = #minimal generators, |A|.
import sys
from collections import Counter
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles, min_nonelements
m0, m1 = map(int, sys.argv[1:3])
for m in range(m0, m1 + 1):
    stat = Counter(); muA = Counter()
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        G = min_nonelements(set(D))
        face = [sum(1 for q in G if q[c] == 0 and sum(1 for i in range(3) if q[i] > 0) == 2) for c in range(3)]
        full = sum(1 for q in G if min(q) > 0)
        A = sum(1 for x in D if all(x[:i] + (x[i]+1,) + x[i+1:] not in D for i in range(3)))
        stat[(tuple(sorted(face)), full)] += 1; muA[(len(G), A)] += 1
    print(f'm={m}: (sorted face inner-corner counts, #full-support) -> #tiles: {dict(sorted(stat.items()))}')
    print(f'      (mu, |A|) -> #tiles: {dict(sorted(muA.items()))}', flush=True)
