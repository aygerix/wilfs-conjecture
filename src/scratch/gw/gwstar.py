# GW* (no residue hypothesis): for EVERY down-set D (|D| = m, all d directions) and EVERY n in [1,N]^d,
#   d*m*max v - (d+1)*sum v  >=  (d-1) * sum (v mod q)     with q = m (and other q if given).
# For residue-complete (D,n) and q = m the right side is (d-1)m(m-1)/2, i.e. GW.
import sys, numpy as np
from itertools import product
d, m0, m1, Nmax = map(int, sys.argv[1:5]); qmode = sys.argv[5] if len(sys.argv) > 5 else 'm'
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
    N = np.array(list(product(range(1, Nmax + 1), repeat=d)), dtype=np.int64)
    qs = [m] if qmode == 'm' else list(range(2, 2 * m + 1))
    res = {q: [0, 0, None] for q in qs}
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64); V = X @ N.T
        B = d * m * V.max(0) - (d + 1) * V.sum(0)
        for q in qs:
            R = B - (d - 1) * (V % q).sum(0)
            r = res[q]; r[0] += len(R); bad = np.nonzero(R < 0)[0]; r[1] += len(bad)
            if len(bad):
                j = bad[np.argmin(R[bad])]
                if r[2] is None or R[j] < r[2][0]: r[2] = (int(R[j]), tuple(int(t) for t in N[j]), sorted(D))
    if qmode == 'm':
        r = res[m]; print(f"d={d} m={m} N<={Nmax} q=m tested={r[0]} fails={r[1]} worst={r[2]}", flush=True)
    else:
        print(f"d={d} m={m}: q with fails: {[(q, r[1]) for q, r in res.items() if r[1]]}", flush=True)
