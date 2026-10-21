"""List equality cases of TILE-MAX-AFF (slack 0) among all down-set tiles (lead, 2026-10-20).
Usage: python tilemax_eq.py N MMIN MMAX"""
import sys, itertools
sys.path.insert(0, '.')
from subadd_lp import downsets
N, MMIN, MMAX = map(int, sys.argv[1:4])
for m in range(MMIN, MMAX + 1):
    seen = 0
    for D in downsets(N, m):
        Ds = set(D)
        mx = [a for a in D if all(tuple(a[s] + (s == t) for s in range(N)) not in Ds for t in range(N))]
        for b in itertools.product(range(m), repeat=N):
            e0 = {a: sum(x * y for x, y in zip(a, b)) % m for a in D}
            if len(set(e0.values())) != m: continue
            for sh in range(m):
                sl = (N + 1) * m * (m - 1) // 2 - sum((sum(y) + N) * ((e0[y] + sh) % m) for y in mx)
                if sl == 0 and seen < 4:
                    seen += 1; print("m=%d EQUALITY D=%s max=%s b=%s shift=%d" % (m, D, mx, b, sh), flush=True)
