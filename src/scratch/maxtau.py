# max tau (= #gaps in [c-m,c)) and max type t among e = 4 semigroups <m,a,b,c>, generators < K*m.
import sys, itertools
from math import gcd, isqrt
sys.path.insert(0, 'src')
from ns import NS
m0, m1, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
for m in range(m0, m1 + 1):
    bt = (0,); btt = (0,)
    for a, b, cc in itertools.combinations(range(m + 1, K*m), 3):
        if gcd(gcd(m, a), gcd(b, cc)) != 1: continue
        s = NS.from_generators([m, a, b, cc])
        if s.e != 4: continue
        c = s.c; tau = sum(1 for u in s.apery() if c <= u < c + m)
        if tau > bt[0]: bt = (tau, s.P)
        t = s.t()
        if t > btt[0]: btt = (t, s.P)
    print(f'm={m}: max tau {bt}  (2sqrt(m)={2*m**0.5:.1f}, sqrt(2m)={(2*m)**0.5:.1f}); max type {btt}', flush=True)
