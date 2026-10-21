# tileshow: print the Q5 max-length tile of S = <m, m+a_1, ..., m+a_d> with NE/EQ labels (independent of q5d*.c)
import sys
from itertools import combinations_with_replacement as cwr
def show(gens):
    m = gens[0]; A = [g - m for g in gens[1:]]; d = len(A); e = d + 1
    # Apery set of S by brute force membership
    N = 8 * m; inS = [False] * N; inS[0] = True
    for x in range(1, N): inS[x] = any(x >= g and inS[x - g] for g in gens)
    w = [min(x for x in range(s, N, m) if inS[x]) for s in range(m)]
    # max-length factorizations (over level-1 generators) of each w_s; lex-largest among them
    X = {}
    for s in range(m):
        best = None
        for k in range(0, 4):
            for comb in cwr(range(d), k):
                if k * m + sum(A[i] for i in comb) == w[s]:
                    v = tuple(sum(1 for i in comb if i == q) for q in range(d))
                    if best is None or (k, v) > best: best = (k, v)
        assert best is not None, ("no factorization of length <= 3", s)
        X[s] = best[1]
    inT = [False] * N; inT[0] = True
    for x in range(1, N): inT[x] = any(x >= g and inT[x - g] for g in A + [m])
    tau = [min(x for x in range(s, N, m) if inT[x]) for s in range(m)]
    D = set(X.values())
    rows = []
    for s in range(m):
        x = X[s]; h = sum(x); sg = w[s] - h * m; j = (sg - tau[s]) // m
        P = sum((x[i] + 1) * (3 - h) for i in range(d) if tuple(x[q] + (q == i) for q in range(d)) not in D)
        typ = 'EQ' if j == 0 else ('NE2' if h == 2 else 'NE3')
        rows.append((h, sg, s, x, tau[s], j, P, typ))
    D3 = 3 * (e - 1) * m - e * sum(r[0] for r in rows)
    assert D3 == sum(r[6] for r in rows)
    maxtau = max(tau); maxsg = max(r[1] for r in rows)
    print(f"S={gens} m={m} A={A} e={e} Delta3={D3} max sigma={maxsg} max tau={maxtau} dc={maxsg - maxtau}")
    for h, sg, s, x, t, j, P, typ in sorted(rows):
        if typ != 'EQ' or P > 0:
            print(f"  class {s:3d} h={h} x={x} sigma={sg:3d} tau={t:3d} j={j} P={P:2d} {typ}{' ABOVE' if sg > maxtau else ''}")
for arg in sys.argv[1:]:
    show([int(t) for t in arg.split(',')])
