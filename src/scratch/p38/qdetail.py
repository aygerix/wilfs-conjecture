# qdetail: anatomy of Q' versus the missing children of large squares, in the eta-partition [0,m) = Z | M1 | M2'.
import sys
from itertools import combinations_with_replacement as cwr
def run(m, A):
    d = len(A); e = d + 1
    best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
            if cl not in best or key < best[cl][0]: best[cl] = (key, c)
    sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}; rep = {cl: best[cl][1] for cl in best}
    eta = {c: sg[c] // m for c in range(m)}
    Z = sorted(c for c in range(m) if eta[c] == 0); M1 = sorted(c for c in range(m) if eta[c] == 1); M2 = sorted(c for c in range(m) if eta[c] == 2)
    cover = set((z + a) % m for z in Z for a in [0] + A); Q = sorted(set(range(m)) - cover)
    print(f"m={m} A={A}\n Z={Z}\n M1={M1}\n M2'={M2}\n Q'={Q}  (eta: {[eta[c] for c in Q]})")
    inU = lambda x: x >= sg[x % m]
    for c in M1:
        if len(rep[c]) != 2: continue
        u = c; miss = [A[l] for l in range(d) if inU(u + A[l])]
        qch = [A[l] for l in range(d) if ((u + A[l]) % m) in Q and sg[(u + A[l]) % m] == u + A[l] + m]
        print(f"   large square {tuple(A[i] for i in rep[c])} = {c + m}: u={u}; missing children a in {miss}; Q'-children a in {qch}")
for arg in sys.argv[1:]:
    t = list(map(int, arg.split(','))); run(t[0], t[1:])
