# Cross coverage of the top layer: Cov = sum_{u in X} (l(u)+1) vs (d+1)m/2 ; and TOP'' slack. By e.
import sys, collections, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS, all_by_genus
from cl import factorizations_down_set
def cov(s):
    m, c = s.m, s.c; d = s.e - 1
    _, best = factorizations_down_set(s, 'grlex')
    X = [u for u in s.apery() if c <= u < c + m]
    C = sum(sum(best[u]) + 1 for u in X)
    return d, m, C, len(X)
worst = collections.defaultdict(lambda: (-1e9, None))
G = int(sys.argv[1])
for g, s in all_by_genus(G):
    if g == 0 or s.e < 3: continue
    d, m, C, tau = cov(s)
    val = C - (d + 1)*m/2
    if val/m > worst[d][0]: worst[d] = (val/m, (s.P, m, C, tau))
for d in sorted(worst): print('d', d, 'max (Cov - (d+1)m/2)/m =', round(worst[d][0], 3), worst[d][1])
