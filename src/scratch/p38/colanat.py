# colanat: column-top anatomy of D3 = sum_i sum_{i-columns} |C|(3 - |top|) for given S; per direction and per top level;
# Q3 cubes listed with their parents' P.
import sys
from itertools import combinations_with_replacement as cwr
def run(m, A):
    d = len(A); e = d + 1
    best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
            if cl not in best or key < best[cl][0]: best[cl] = (key, c)
    D = set(best[cl][1] for cl in best); val = lambda c: sum(A[i] for i in c)
    h = sum(len(x) for x in D); D3 = 3 * (e - 1) * m - e * h
    per = [[0] * 3 for _ in range(d)]; tot = 0
    for x in D:
        for i in range(d):
            y = tuple(sorted(x + (i,)))
            if y in D or len(x) == 3: continue
            # x is the top of an i-column of length x_i + 1
            per[i][len(x)] += (x.count(i) + 1) * (3 - len(x)); tot += (x.count(i) + 1) * (3 - len(x))
    assert tot == D3, (tot, D3)
    Q3 = [c for c in D if len(c) == 3 and val(c) >= m and all(val(c) - A[i] >= m for i in c)]
    M2 = sum(1 for c in cwr(range(d), 2) if c not in D); M3 = sum(1 for c in cwr(range(d), 3) if c not in D)
    print(f"m={m} A={A} e={e} D3={D3} |Q3|={len(Q3)} M2={M2} M3={M3} n2={sum(1 for x in D if len(x)==2)} n3={sum(1 for x in D if len(x)==3)}")
    for i in range(d): print(f"   dir a={A[i]:3d}: tops level0/1/2 contribute {per[i]}  sum {sum(per[i])}")
    print('   Q3 cubes:', sorted([tuple(A[i] for i in c) for c in Q3]))
for arg in sys.argv[1:]:
    t = list(map(int, arg.split(','))); run(t[0], t[1:])
