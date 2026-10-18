# Lemma P check: projections of tripods to each coordinate plane form a chain (no strictly anti-ordered pair)
import sys
sys.path.insert(0, sys.path[0])
from classify import gen
from hyper import cells
M = int(sys.argv[1]); bad = 0; n = 0
for key, D, C in gen(M):
    Max, cl = cells(D); n += 1
    T = [x for k, x, ms in cl if k == 'T']
    for a, b in [(0, 1), (0, 2), (1, 2)]:
        for x in T:
            for y in T:
                if x[a] < y[a] and x[b] > y[b]: bad += 1; print('BAD', key, x, y, a, b); break
print('sets', n, 'chain violations', bad)
