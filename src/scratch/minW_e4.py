# min W (and W/m) among e = 4 semigroups <m,a,b,c> with generators < K*m, per m; also the minimizer.
import sys, itertools
from math import gcd
sys.path.insert(0, 'src')
from ns import NS
m0, m1, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
for m in range(m0, m1 + 1):
    best = None
    for a, b, cc in itertools.combinations(range(m + 1, K*m), 3):
        if gcd(gcd(m, a), gcd(b, cc)) != 1: continue
        s = NS.from_generators([m, a, b, cc])
        if s.e != 4: continue
        if best is None or s.W < best[0]: best = (s.W, s.P, s.c, s.ell)
    print(f'm={m}: min W {best[0]} (W/m={best[0]/m:.2f}) at {best[1]} c={best[2]} ell={best[3]}', flush=True)
