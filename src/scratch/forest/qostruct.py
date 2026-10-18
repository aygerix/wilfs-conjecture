# qO structure: (Q1) qO cells sharing a maximal top share it in the same direction;
# (Q2) for each qO cell x, at most one of its two max-top directions a has another qO cell strictly BELOW x on the a-line (x - k e_a) sharing top_a
# (Q2up) same with ABOVE; also record the direction pattern (c, a) of shared tops.
import sys
sys.path.insert(0, sys.path[0])
from classify import gen
from hyper import cells
from collections import defaultdict, Counter
def toplist(D, x):
    out = []
    for a in range(3):
        y = list(x)
        while True:
            y[a] += 1
            if tuple(y) not in D: y[a] -= 1; break
        out.append(tuple(y))
    return out
M = int(sys.argv[1]); bad = Counter(); ex = {}; pat = Counter(); nD = 0
for key, D, C in gen(M):
    Max, cl = cells(D); nD += 1
    qo = []
    for k, x, ms in cl:
        if k != 'O': continue
        tp = toplist(D, x); dirs = [a for a in range(3) if tp[a] in Max]; c = [a for a in range(3) if a not in dirs][0]
        qo.append((x, tp, dirs, c))
    inc = defaultdict(list)
    for x, tp, dirs, c in qo:
        for a in dirs: inc[tp[a]].append((x, a, c))
    for y, L in inc.items():
        if len({a for _, a, _ in L}) > 1: bad['Q1'] += 1; ex.setdefault('Q1', (key, y, L))
        if len(L) > 1:
            for (x1, a1, c1) in L:
                for (x2, a2, c2) in L:
                    if x1 < x2: pat[(a1, c1, c2)] += 1
    for x, tp, dirs, c in qo:
        below = [a for a in dirs if any(x2 != x and x2[a] < x[a] for x2, a2, _ in inc[tp[a]])]
        above = [a for a in dirs if any(x2 != x and x2[a] > x[a] for x2, a2, _ in inc[tp[a]])]
        if len(below) > 1: bad['Q2below'] += 1; ex.setdefault('Q2below', (key, x))
        if len(above) > 1: bad['Q2above'] += 1; ex.setdefault('Q2above', (key, x))
print('sets', nD, dict(bad)); print('share patterns (dir, c_low, c_high):', dict(pat))
for k, v in ex.items(): print(k, v)
