# Lemma check: a staircase D in N^2 (|D| = m) on which x.s mod m is bijective has at most 2 corners.
# Enumerates every partition of m with >= 3 distinct row lengths and every s in [1,m-1]^2 (or only s with both
# entries non-units if 'nonunit' is given), reporting any residue-bijective one.
import sys, numpy as np
from math import gcd
m0, m1 = int(sys.argv[1]), int(sys.argv[2]); only_nonunit = len(sys.argv) > 3
def parts(n, mx):
    if n == 0: yield []; return
    for k in range(min(n, mx), 0, -1):
        for r in parts(n - k, k): yield [k] + r
for m in range(m0, m1 + 1):
    S = np.array([(a, b) for a in range(1, m) for b in range(1, m)
                  if not only_nonunit or (gcd(a, m) > 1 and gcd(b, m) > 1)], dtype=np.int64)
    if len(S) == 0: print(f"m={m}: no s", flush=True); continue
    ar = np.arange(m)[:, None]; cnt = found = 0
    for lam in parts(m, m):
        if len(set(lam)) < 3: continue
        cnt += 1
        X = np.array([(i, j) for j, l in enumerate(lam) for i in range(l)], dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if ok.any(): found += 1; print('  FOUND', m, lam, S[ok][:3].tolist(), flush=True)
    print(f"m={m}: staircases with >=3 corners: {cnt}, residue-bijective: {found}", flush=True)
