# All e = 4 semigroups <m, a, b, c> with m in [m0, m1], m < a < b < c < K*m: residual of the sharp tau-criterion,
# split by two-face / non-two-face.
import sys, itertools, time
from math import gcd
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from tau_residual import analyse
m0, m1, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
for m in range(m0, m1 + 1):
    t0 = time.time(); n = res = res_nt = 0; worst_nt = -10**9; ex = None
    for a, b, c in itertools.combinations(range(m + 1, K*m), 3):
        if gcd(gcd(m, a), gcd(b, c)) != 1: continue
        s = NS.from_generators([m, a, b, c])
        if s.e != 4: continue
        r = analyse(s); n += 1
        dfc = 4*r['tau'] + 2*r['P2'] - 2*(m + 1)
        if not r['sharp']:
            res += 1
            if not r['two']: res_nt += 1; ex = (a, b, c)
        if not r['two'] and dfc > worst_nt: worst_nt = dfc
    print(f'm={m}: e=4 semigroups {n}; sharp-criterion residual {res} (non-two-face {res_nt}, ex {ex}); max deficit among non-two-face {worst_nt}  [{time.time()-t0:.0f}s]', flush=True)
