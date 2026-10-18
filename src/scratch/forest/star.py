# Tripod star structure test: (S1) two tripods sharing a top lie on a common ray whose top is the shared vertex;
# (S2) components of tripod hypergraph are stars. Also qO edge order test (sum_asc).
import sys
sys.path.insert(0, sys.path[0])
from classify import gen
from hyper import cells
def toplist(D, x):
    out = []
    for a in range(3):
        y = list(x)
        while True:
            y[a] += 1
            if tuple(y) not in D: y[a] -= 1; break
        out.append(tuple(y))
    return out
M = int(sys.argv[1]); nD = 0; s1bad = s2bad = qbad = 0; ex = {}
from collections import defaultdict
for key, D, C in gen(M):
    Max, cl = cells(D); nD += 1
    tr = [(x, toplist(D, x)) for (k, x, ms) in cl if k == 'T']
    inc = defaultdict(list)
    for x, tp in tr:
        for a in range(3): inc[tp[a]].append((x, a))
    for y, L in inc.items():
        if len(L) > 1:
            dirs = {a for x, a in L}
            if len(dirs) > 1: s1bad += 1; ex.setdefault('S1', (key, y, L)); break
    # star: for each tripod, at most one of its tops is shared
    for x, tp in tr:
        if sum(1 for a in range(3) if len(inc[tp[a]]) > 1) > 1: s2bad += 1; ex.setdefault('S2', (key, x, tp)); break
    qo = sorted([(x, ms) for (k, x, ms) in cl if k == 'O'], key=lambda e: sum(e[0]))
    seen = set()
    for x, ms in qo:
        if len(seen & set(ms)) > 1: qbad += 1; ex.setdefault('Q', key); break
        seen |= set(ms)
print("sets", nD, "S1bad", s1bad, "S2bad", s2bad, "qO-sumasc-bad", qbad)
for k, v in ex.items(): print(k, v)
