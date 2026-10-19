# Near-stars D = {0, e_1..e_d} u Q, Q = set of level-2 cells (multigraph with loops on [d]), m = 1 + d + q.
# GW <=> [*] := sum_a (d+1-deg a) U_a + (d+2) sum_{e in Q} U_e  >=  (d-1) m (m-1)/2,  U = M - v.
# Exhaustive over Q (up to relabelling), s in [1,m-1]^d (residue-complete), k in [0,K]^d.  Per (d,q): min of
# ([*] - target), min E, and the extremal configurations.  Also asserts [*]-identity against E directly.
import sys, numpy as np
from itertools import product, combinations, permutations
d, K, qmin, qmax = map(int, sys.argv[1:5])
pairs = [(a, b) for a in range(d) for b in range(a, d)]
def canon(Q):
    return min(tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in Q)) for p in permutations(range(d)))
seen = set()
for q in range(qmin, qmax + 1):
    m = 1 + d + q; S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    ks = np.array(list(product(range(K + 1), repeat=d)), dtype=np.int64)
    best = None; bestE = None; nQ = ninst = 0
    for Q in combinations(pairs, q):
        cQ = canon(Q)
        if cQ in seen: continue
        seen.add(cQ); nQ += 1
        cells = [tuple(0 for _ in range(d))] + [tuple(int(i == a) for i in range(d)) for a in range(d)] + \
                [tuple(int(i == a) + int(i == b) for i in range(d)) for a, b in Q]
        X = np.array(cells, dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if not ok.any(): continue
        deg = np.zeros(d, dtype=np.int64)
        for a, b in Q: deg[a] += 1; deg[b] += 1
        N = (S[ok][:, None, :] + m * ks[None, :, :]).reshape(-1, d)
        V = X @ N.T; M = V.max(0); Uc = M[None, :] - V
        star = ((d + 1 - deg)[:, None] * Uc[1:1 + d]).sum(0) + (d + 2) * Uc[1 + d:].sum(0)
        tgt = (d - 1) * m * (m - 1) // 2
        E = d * (M - m + 1) - (d + 1) * (V // m).sum(0)
        assert np.all((star - tgt) == m * E), "identity"
        ninst += len(E); j = int(np.argmin(E))
        if bestE is None or E[j] < bestE[0]:
            bestE = (int(E[j]), tuple(int(t) for t in N[j]), Q, int(M[j]))
    print(f"d={d} q={q} m={m} graphs={nQ} instances={ninst} minE={bestE}", flush=True)
