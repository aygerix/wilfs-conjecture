# (**_i):  i*|Y^(i)| <= d * sum_{j=1}^{i-1} j*|T^(j)| + beta'_i      (all i >= 2), multiplicity form, residue-complete
#   T^(j) = non-maximal w with j*m <= h(w) < (j+1)*m   (h = max upward value)
#   Y^(i) = nonzero x all of whose lower covers w have h(w) < i*m
#   beta'_i = sum_{x != 0} (i - kappa(x))_+
# (**_i) implies the local P_i; check both, per i.
import sys, numpy as np
from itertools import product
d, m0, m1, Kmax = map(int, sys.argv[1:5]); mode = sys.argv[5] if len(sys.argv) > 5 else 'res'
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
def downsets(M):
    lev = {frozenset([tuple([0] * d)])}
    for m in range(1, M + 1):
        if m >= m0: yield m, lev
        nxt = set()
        for D in lev:
            for x in D:
                for u in U:
                    y = add(x, u)
                    if y not in D and all(y[a] == 0 or sub(y, U[a]) in D for a in range(d)): nxt.add(D | {y})
        lev = nxt
for m, lev in downsets(m1):
    if mode == 'res':
        S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
        ks = np.array(list(product(range(1, Kmax + 1), repeat=d)), dtype=np.int64)
    else:
        Nall = np.array(list(product(range(m + 1, Kmax * m + 1), repeat=d)), dtype=np.int64)
    tot = 0; fails = {}; lpf = {}; ex = {}
    for D in lev:
        if any(u not in D for u in U): continue
        Ds = sorted(D); X = np.array(Ds, dtype=np.int64); idx = {x: i for i, x in enumerate(Ds)}
        above = np.all(X[None, :, :] >= X[:, None, :], axis=2)
        nonmax = np.array([any(add(x, u) in D for u in U) for x in Ds])
        L = np.zeros((len(Ds), len(Ds)), dtype=bool)          # L[x, w] = w is a lower cover of x
        for i, x in enumerate(Ds):
            for a in range(d):
                if x[a] > 0: L[i, idx[sub(x, U[a])]] = True
        hasl = L.any(1)
        supp = np.array([sum(1 for t in x if t > 0) for x in Ds])
        if mode == 'res':
            ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
            Ns = [s[None, :] + m * ks for s in S[ok]]
        else: Ns = [Nall]
        for N in Ns:
            V = X @ N.T; H = np.where(above[:, :, None], V[None, :, :], -1).max(1) - V
            kap = V // m; lam = H // m; tot += V.shape[1]
            top = int(max(kap.max(), lam.max())) + 1
            for i in range(2, top + 1):
                shallow = H < i * m                                   # (m, nk)
                # Y^(i): x != 0 with every lower cover shallow
                Y = hasl[:, None] & ~(L[:, :, None] & ~shallow[None, :, :]).any(1)
                k = N // m                                              # (nk, d)
                lhs = (Y * np.maximum(i - supp[:, None], 0)).sum(0)     # low-support trapped cells
                rhs = np.maximum(i - kap, 0).sum(0) - i                 # beta'_i (exclude x = 0)
                for j in range(1, i):
                    dj = (k <= j).sum(1)
                    rhs = rhs + (d * j - dj) * (nonmax[:, None] & (H >= j * m) & (H < (j + 1) * m)).sum(0)
                b = lhs > rhs
                if b.any():
                    fails[i] = fails.get(i, 0) + int(b.sum())
                    if i not in ex: j = int(np.argmax(b)); ex[i] = (tuple(int(t) for t in N[j]), Ds)
                lp = np.minimum(kap, i).sum(0) - d * np.minimum(lam, i).sum(0)
                if (lp > 0).any(): lpf[i] = lpf.get(i, 0) + int((lp > 0).sum())
    print(f"d={d} m={m} {mode} inst={tot} (***_i) fails by i: {dict(sorted(fails.items()))}  localP_i fails: {dict(sorted(lpf.items()))}", flush=True)
    for i in sorted(ex)[:3]: print("   ex i=%d" % i, ex[i], flush=True)
