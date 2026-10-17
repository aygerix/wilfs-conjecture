"""E11: monotonicity of TOP'' slack sigma along the semigroup tree (parent T = S u {F})."""
import sys
sys.path.insert(0, 'src')
from ns import NS, children
from top2 import minlen_apery
from collections import Counter

def sigma(s):
    if s.m == 1:
        return 0
    m, c, e = s.m, s.c, s.e
    ml = minlen_apery(s); pos = lambda x: ((x - c) % m) + 1
    ap = s.apery()
    return e * sum(pos(w) for w in ap if w < c) - m - sum(pos(u) * (ml[u] - 1) for u in ap if u >= c)

G = int(sys.argv[1]) if len(sys.argv) > 1 else 14
level = [NS(0, 1, bytes([1]))]
dec = Counter(); n = 0; worst = []
for g in range(G):
    nxt = []
    for T in level:
        sT = sigma(T)
        for S in children(T):
            sS = sigma(S)
            n += 1
            diff = sS - sT
            dec['neg' if diff < 0 else ('zero' if diff == 0 else 'pos')] += 1
            if diff < 0 and len(worst) < 6:
                worst.append((T.P, S.P, sT, sS))
            nxt.append(S)
    level = nxt
print('parent->child pairs', n, dict(dec))
for w in worst: print('  decrease', w)
