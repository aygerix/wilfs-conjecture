# z1min: on residual dumps, z = |3A' cap [0,m)|; list the S with smallest e*z - m, and the distribution of z vs m/e.
import sys
from itertools import combinations_with_replacement as cwr
rows = []
for fn in sys.argv[1:]:
    for L in open(fn):
        t = L.split()
        if t[0] != 'DUMP': continue
        m = int(t[1]); A = list(map(int, t[15:])); e = len(A) + 1
        Z = set(v for k in range(4) for c in cwr(A, k) for v in [sum(c)] if v < m)
        lo = sum(1 for a in A if a < m / 2)
        rows.append((e * len(Z) - m, m, e, len(Z), lo, A))
rows.sort()
print(sys.argv[1], len(rows), 'min slack', rows[0][0], 'median', rows[len(rows) // 2][0])
for r in rows[:8]: print('  slack', r[0], 'm', r[1], 'z', r[3], '#a<m/2', r[4], 'A', r[5])
