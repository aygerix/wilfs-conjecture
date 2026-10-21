# R1: Ap(T, mu) c U  (equivalently: every t in T\U has t - mu in T).  Also R1': every NE class has tau_s - mu in T.
import sys
from itertools import combinations_with_replacement as cwr
for fn in sys.argv[1:]:
    n = bad = 0; ex = []
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            m = int(t[1]); A = list(map(int, t[15:])); mu = A[0]; n += 1
            N = 4 * m; inT = [False] * (N + 1); inT[0] = True
            for x in range(1, N + 1): inT[x] = any(x >= g and inT[x - g] for g in A + [m])
            sig = {}
            for k in range(4):
                for c in cwr(A, k):
                    v = sum(c); s = v % m
                    if s not in sig or v < sig[s]: sig[s] = v
            inU = lambda x: x >= sig[x % m]
            om = [min(x for x in range(i, N + 1, mu) if inT[x]) for i in range(mu)]
            notU = [w for w in om if not inU(w)]
            if notU:
                bad += 1
                if len(ex) < 3: ex.append((m, A, notU))
    print(fn, 'n', n, 'R1 failures (Ap(T,mu) not in U):', bad, ex)
