"""E12: Is TOP'' purely combinatorial?  'Free positions' version: replace the true positions by the
worst-case bijection given only (m, d, top set with lengths):  tops get the largest positions, sorted by ell.
TOPfree: sum_i (m-i+1)(ell_(i)+1) <= m^2 + (d-1) * (sum of the remaining positions 1..m-k)."""
import sys
sys.path.insert(0, 'src')
from ns import all_by_genus
from top2 import minlen_apery
G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
n = f = 0; ex = []
for g, s in all_by_genus(G):
    if s.m <= 1: continue
    m, c, d = s.m, s.c, s.e - 1
    ml = minlen_apery(s)
    lens = sorted((ml[u] for u in s.apery() if u >= c), reverse=True)
    k = len(lens)
    lhs = sum((m - i) * (L + 1) for i, L in enumerate(lens))
    rhs = m * m + (d - 1) * (m - k) * (m - k + 1) // 2
    n += 1
    if lhs > rhs:
        f += 1
        if len(ex) < 6: ex.append((s.P, s.c, s.W, lens, lhs - rhs))
print(f'genus<={G}: {n}; TOPfree fails {f}')
for x in ex: print('  ', x)
