# c(x) = #{a : t_a(x) maximal}; T(A) - 2m = sum_x (c(x) - 2). Distribution by support size of x, two-face vs non-two-face.
import sys, random, itertools
from collections import Counter
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from cl import factorizations_down_set
def cstats(s):
    _, best = factorizations_down_set(s, 'grlex'); cells = set(best.values()); d = 3
    def up(x, a): return x[:a] + (x[a] + 1,) + x[a+1:]
    maxi = {x for x in cells if all(up(x, a) not in cells for a in range(d))}
    cnt = Counter()
    for x in cells:
        c = 0
        for a in range(d):
            t = x
            while up(t, a) in cells: t = up(t, a)
            c += t in maxi
        supp = sum(1 for v in x if v)
        cnt[(supp, 'M' if x in maxi else c)] += 1
    two = any(tuple(int(i in (a, b)) for i in range(3)) not in cells for a in range(3) for b in range(a+1, 3))
    TA = sum(sum(y) + 3 for y in maxi)
    return two, TA - 2*len(cells), cnt, len(cells)
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2])
agg = {True: Counter(), False: Counter()}; worst = {True: None, False: None}; n = {True: 0, False: 0}
gens = []
while len(gens) < N:
    m = rng.randint(20, int(sys.argv[3])); K = rng.choice([2, 3, 4])
    g = sorted(set([m] + [rng.randint(m + 1, K*m) for _ in range(3)]))
    if len(g) == 4 and reduce(gcd, g) == 1: gens.append(g)
for a in range(4, 10): gens.append([a*a, a*a+1, a*a+a, a*a+a+1])
for g in gens:
    s = NS.from_generators(g)
    if s.e != 4: continue
    two, ex, cnt, m = cstats(s); n[two] += 1
    for k, v in cnt.items(): agg[two][k] += v/m
    if worst[two] is None or ex/m > worst[two][0]: worst[two] = (round(ex/m, 3), g, ex, dict(cnt))
for two in (True, False):
    print('TWO-FACE' if two else 'NON-TWO-FACE', 'tiles', n[two], 'worst (T(A)-2m)/m', worst[two][:3])
    print('   average fraction of cells by (support, c or M):', {k: round(v/n[two], 3) for k, v in sorted(agg[two].items(), key=lambda t: (t[0][0], str(t[0][1])))})
    print('   worst tile counts:', worst[two][3])
