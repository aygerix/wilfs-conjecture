# random NON-two-face e = 4 tiles at given m: distribution of H/m (shape-only).  usage: seed N m K
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from cl import factorizations_down_set
from heightH import H_of
seed, N, m, K = map(int, sys.argv[1:5]); rng = random.Random(seed); vals = []
while len(vals) < N:
    g = sorted(set([m] + [rng.randint(m + 1, K*m) for _ in range(3)]))
    if len(g) != 4 or reduce(gcd, g) != 1: continue
    s = NS.from_generators(g)
    if s.e != 4: continue
    p, best = factorizations_down_set(s, 'grlex'); D = set(best.values())
    if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
    vals.append((H_of(D)/m, g))
vals.sort()
print(f'm={m} K={K} N={N}: min H/m {vals[0][0]:.3f} {vals[0][1]}; 5% {vals[N//20][0]:.3f}; median {vals[N//2][0]:.3f}')
