"""INJ-SUBADD test (lead, 2026-10-21): for down-sets E in N^n (n = 2, 3; all of size k) and chi(a) = a.b mod m
injective on E (any m >= k), lambda in LAMS, eps = (chi + lambda) mod m:
    sum_{y in Max(E)} (|y|-1) eps(y) <= (n+1) sum_{E \\ Max(E)} eps.
(lambda = 0 with E = ↓Z inside a tile is Hall's condition for the box transport.) Usage: python injsub.py N KMIN KMAX MEXTRA [aff]"""
import sys, itertools
sys.path.insert(0, '.')
from subadd_lp import downsets
N, KMIN, KMAX, MEXTRA = map(int, sys.argv[1:5]); AFF = len(sys.argv) > 5
tot = fail = 0
for k in range(KMIN, KMAX + 1):
    for E in downsets(N, k):
        Es = set(E)
        mx = [a for a in E if all(tuple(a[s] + (s == t) for s in range(N)) not in Es for t in range(N))]
        mxs = set(mx)
        for m in range(k, k + MEXTRA + 1):
            for b in itertools.product(range(m), repeat=N):
                e0 = [sum(x * y for x, y in zip(a, b)) % m for a in E]
                if len(set(e0)) != k: continue
                for lam in (range(m) if AFF else [0]):
                    eps = dict(zip(E, [(v + lam) % m for v in e0])); tot += 1
                    sl = (N + 1) * sum(eps[a] for a in E if a not in mxs) - sum((sum(y) - 1) * eps[y] for y in mx)
                    if sl < 0:
                        fail += 1
                        if fail <= 4: print("INJ-SUBADD FAIL k=%d m=%d E=%s b=%s lam=%d slack=%d" % (k, m, E, b, lam, sl), flush=True)
    print("k=%d tested %d failures %d" % (k, tot, fail), flush=True)
