# (SC): 2|A| + P2(A) <= m + 1 + H2  (shape-only; implies HT via the Cross Lemma on the antichain A).  Also |A| vs 2*sumL+3
# (Betti bound), and the number mu of minimal generators of N^3 \ D.   usage: m0 m1 K
import sys, itertools
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
m0, m1, K = map(int, sys.argv[1:4])
for m in range(m0, m1 + 1):
    worst = None; n = 0; fails = 0; betti = None
    for g3 in itertools.combinations(range(m + 1, K*m), 3):
        if reduce(gcd, (m,) + g3) != 1: continue
        s = NS.from_generators([m, *g3])
        if s.e != 4: continue
        p, best = factorizations_down_set(s, 'grlex'); D = set(best.values())
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        ht = {}
        for x in sorted(D, key=lambda x: -sum(x)):
            ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
        def top(x, i):
            while add(x, i) in D: x = add(x, i)
            return x
        H2 = sum(max(0, ht[top(x, i)] - 1) for x in D for i in range(3))
        A = [x for x in D if ht[x] == 0]
        P2 = sum(1 for y, z in itertools.combinations(A, 2) if sum(y[i] != z[i] for i in range(3)) == 2)
        sl = m + 1 + H2 - 2*len(A) - P2; n += 1; fails += sl < 0
        L = [max(x[i] for x in D) + 1 for i in range(3)]
        cand = {add(x, i) for x in D for i in range(3)} - D
        G = [q for q in cand if all(q[i] == 0 or q[:i] + (q[i]-1,) + q[i+1:] in D for i in range(3))]
        bt = 2*len(G) - 5 - len(A)
        if betti is None or bt < betti[0]: betti = (bt, [m, *g3])
        if worst is None or sl < worst[0]: worst = (sl, [m, *g3], len(A), P2, H2)
    print(f'm={m}: {n}; min SC slack {worst}; fails {fails}; min (2mu-5-|A|) {betti}', flush=True)
