import sys
from itertools import combinations_with_replacement as cwr
import heapq
def run(m, A):
    d = len(A); e = d + 1
    best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
            if cl not in best or key < best[cl][0]: best[cl] = (key, c)
    sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}; rep = {cl: best[cl][1] for cl in best}
    tau = [None] * m; tau[0] = 0; pq = [(0, 0)]; done = [False] * m
    while pq:
        t, c = heapq.heappop(pq)
        if done[c]: continue
        done[c] = True
        for a in A:
            u = t + a; cc = u % m
            if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
    Z = sorted(c for c in range(m) if sg[c] < m)
    M1 = [c for c in range(m) if m <= sg[c] < 2 * m]
    Q1p = [c for c in M1 if A[max(rep[c])] <= c]
    N = [(x, a) for x in Z for a in A if x + a < m]
    print(f"m={m} A={A} e={e} z={len(Z)} Z={Z}")
    print(f"  N_< ({len(N)}): {N}")
    print(f"  Q1' ({len(Q1p)}): " + ", ".join(f"{c}:{tuple(A[i] for i in rep[c])}{'NE' if tau[c] < sg[c] else ''}" for c in Q1p))
    NE2 = [c for c in range(m) if tau[c] < sg[c] and len(rep[c]) == 2]
    print(f"  NE2 values (tau): {[tau[c] for c in NE2]}  H = {[a for a in A if 2 * a >= m]}")
for arg in sys.argv[1:]:
    t = list(map(int, arg.split(','))); run(t[0], t[1:])
