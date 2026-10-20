r"""MD (and TMD) on every numerical semigroup of genus <= G (lead, 2026-10-20), via the semigroup tree
(children: remove a minimal generator > F).  usage: mdtree.py G"""
import sys
sys.path.insert(0, ".")
from md import analyse
G = int(sys.argv[1]); stats = {}; nfail = 0
def visit(gaps, F, m, gens, g):
    global nfail
    if m >= 2:
        r = analyse(list(gens))
        if r is not None:
            s = stats.setdefault(g, [0, 0, 0])
            s[0] += 1
            if r["MD"] < 0: s[1] += 1
            if r["TMD"] < 0: s[2] += 1
            if (r["MD"] < 0 or r["TMD"] < 0) and nfail < 10: nfail += 1; print("FAIL", r, flush=True)
    if g == G: return
    inS = lambda x, gp, FF: x >= 0 and (x > FF or x not in gp)
    for n in gens:
        if n <= F: continue
        gp2 = gaps | {n}
        if n == m:
            m2 = m + 1; ng = list(range(m2, 2 * m2))
        else:
            m2 = m; ng = [x for x in gens if x != n]
            y = n + m
            dec = any(a != n and inS(a, gp2, n) and (y - a) != n and inS(y - a, gp2, n) for a in range(m, y // 2 + 1))
            if not dec: ng.append(y)
        visit(gp2, n, m2, ng, g + 1)
visit(frozenset(), -1, 1, [1], 0)
for g in sorted(stats): print(g, stats[g], flush=True)
