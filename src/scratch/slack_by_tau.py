# e = 4: TOP'' relative slack 1 - lhs/rhs by tau, over all <m,a,b,c> with generators < K*m, m in [m0,m1].
import sys, itertools
from math import gcd
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from cl import factorizations_down_set
m0, m1, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
best = {}
for m in range(m0, m1 + 1):
    for a, b, cc in itertools.combinations(range(m + 1, K*m), 3):
        if gcd(gcd(m, a), gcd(b, cc)) != 1: continue
        s = NS.from_generators([m, a, b, cc])
        if s.e != 4: continue
        c = s.c; ap = s.apery(); X = [u for u in ap if c <= u < c + m]
        _, bst = factorizations_down_set(s, 'grlex')
        lhs = sum((u - c + 1)*(3 + sum(bst[u])) for u in X); rhs = m*(4*m + 2)//2
        sl = 1 - lhs/rhs; t = len(X)
        if t not in best or sl < best[t][0]: best[t] = (round(sl, 4), s.P, m)
for t in sorted(best): print('tau', t, 'min rel slack', best[t])
