"""E7: near-tight cases of TOP'' (form: m + sum_{u in Xq} pi(u)(ell(u)-1) <= e * sum_{j in Pi^c} j)."""
import sys
sys.path.insert(0, 'src')
from ns import all_by_genus
from top2 import minlen_apery
G = int(sys.argv[1]) if len(sys.argv) > 1 else 18
rows = []
for g, s in all_by_genus(G):
    if s.m <= 2 or s.W == 0:
        continue
    m, c, e = s.m, s.c, s.e
    ml = minlen_apery(s)
    Xq = [w for w in s.apery() if w >= c]
    lhs = m + sum((u - c + 1) * (ml[u] - 1) for u in Xq)
    Pic = [y - c + m + 1 for y in range(c - m, c) if y >= 0 and y in s]
    rhs = e * sum(Pic)
    rows.append(((rhs - lhs) / rhs, rhs - lhs, s.P, s.c, s.q, s.W,
                 sorted((u - c + 1, ml[u]) for u in Xq), Pic))
rows.sort()
for r in rows[:25]:
    print('slack %.3f (%d) P=%s c=%d q=%d W=%d  top(pos,ell)=%s  Pic=%s' % r)
