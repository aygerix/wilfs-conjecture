# n(x) = #{a : column top t_a(x) is maximal}.  T(A) - 2m = N3 - N1 - 2 N0, so HT <=> N1 + 2 N0 + 1 + H2 >= N3.
# Reports per m (non-two-face tiles): min of N1+2N0, min N0, max N3, min (N1 + 2N0 - N3), with tile r.  usage: m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
add = lambda x, i: x[:i] + (x[i] + 1,) + x[i+1:]
def ncounts(D):
    A = {x for x in D if all(add(x, i) not in D for i in range(3))}
    N = [0, 0, 0, 0]
    for x in D:
        n = 0
        for a in range(3):
            t = x
            while add(t, a) in D: t = add(t, a)
            n += t in A
        N[n] += 1
    return N, len(A)
for m in map(int, sys.argv[1:]):
    best = {}
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        N, nA = ncounts(set(D))
        for k, v in (('min N1+2N0', N[1] + 2*N[0]), ('min N0', N[0]), ('max N3', -N[3]), ('min slack', N[1] + 2*N[0] - N[3])):
            if k not in best or v < best[k][0]: best[k] = (v, r, N, nA)
    print(f'm={m}:', {k: ((-v[0] if k == 'max N3' else v[0]),) + v[1:] for k, v in best.items()}, flush=True)
