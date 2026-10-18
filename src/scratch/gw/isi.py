# ISI test (no residues): ALL down-sets D of N^d with |D| = m using all d directions, ALL n in [1,N]^d with v = x.n
# INJECTIVE on D.  Tests  B(D,n) = d*m*max v - (d+1)*sum v  >=  (d-1)*m*(m-1)/2.  Also reports how many tested
# pairs are residue-complete mod m (those are the GW cases).
import sys, numpy as np
from itertools import product
d, m0, m1, Nmax = map(int, sys.argv[1:5])
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
def downsets(M):
    lev = {frozenset([tuple([0] * d)])}
    for m in range(1, M + 1):
        if m >= m0: yield m, lev
        nxt = set()
        for D in lev:
            for x in D:
                for u in U:
                    y = tuple(p + q for p, q in zip(x, u))
                    if y not in D and all(y[a] == 0 or tuple(y[b] - (b == a) for b in range(d)) in D for a in range(d)):
                        nxt.add(D | {y})
        lev = nxt
for m, lev in downsets(m1):
    N = np.array(list(product(range(1, Nmax + 1), repeat=d)), dtype=np.int64); tau = (d - 1) * m * (m - 1) // 2
    tested = fails = rc = 0; worst = None; ar = np.arange(m)[:, None]
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        V = np.sort(X @ N.T, axis=0)
        inj = np.all(np.diff(V, axis=0) > 0, axis=0)
        if not inj.any(): continue
        V = V[:, inj]
        B = d * m * V[-1] - (d + 1) * V.sum(0) - tau
        tested += len(B); rc += int(np.all(np.sort(V % m, axis=0) == ar, axis=0).sum())
        bad = np.nonzero(B < 0)[0]; fails += len(bad)
        j = int(np.argmin(B))
        if worst is None or B[j] < worst[0]: worst = (int(B[j]), tuple(int(t) for t in N[inj][j]), sorted(D))
    print(f"d={d} m={m} N<={Nmax} tested={tested} residue_complete={rc} fails={fails} min(B-tau)={worst[0]} n={worst[1]} D={worst[2][:14]}", flush=True)
