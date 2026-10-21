import sys
from itertools import combinations_with_replacement as cwr
def run(m, A):
    d = len(A)
    best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
            if cl not in best or key < best[cl][0]: best[cl] = (key, c)
    sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}; rep = {cl: best[cl][1] for cl in best}
    M2 = sorted(c for c in sg if sg[c] >= 2 * m); r = max(M2)
    K = sorted((sum(A[i] for i in c) - 2 * m, tuple(A[i] for i in c), c) for c in cwr(range(d), 3) if sum(A[i] for i in c) >= 2 * m)
    print(f"m={m} A={A} M2'={M2} r={r} t={len(M2)} K2={len(K)}")
    for p, y, c in K:
        tag = 'REP' if p in M2 and rep[p] == c else ('inM2-nonrep' if p in M2 else ('>r' if p > r else 'in I'))
        print(f"   pos {p:3d} cube {y} {tag}")
for arg in sys.argv[1:]:
    t = list(map(int, arg.split(','))); run(t[0], t[1:])
