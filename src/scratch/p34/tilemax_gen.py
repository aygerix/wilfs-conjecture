"""TILE-MAX on ALL down-set tiles (lead, 2026-10-21). D down-set in N^n (n = 2: partitions, n = 3: plane partitions)
with |D| = m, b in (Z/m)^n, eps(a) = a.b mod m injective on D. Test
    sum_{y in Max(D)} (|y|-1) eps(y) <= (n+1) sum_{D \\ Max(D)} eps.
Usage: python tilemax_gen.py N MMIN MMAX"""
import sys, itertools
sys.path.insert(0, '.')
from subadd_lp import downsets
N, MMIN, MMAX = map(int, sys.argv[1:4]); AFF = len(sys.argv) > 4 and sys.argv[4] == 'aff'
tot = fail = 0; worst = None
for m in range(MMIN, MMAX + 1):
    Ds = list(downsets(N, m))
    for D in Ds:
        Ds_ = set(D)
        mx = [a for a in D if all(tuple(a[s] + (s == t) for s in range(N)) not in Ds_ for t in range(N))]
        mxs = set(mx)
        for b in itertools.product(range(m), repeat=N):
          eps0 = [sum(x * y for x, y in zip(a, b)) % m for a in D]
          if len(set(eps0)) != m: continue
          for sh in (range(m) if AFF else [0]):
            eps = [(e + sh) % m for e in eps0]
            tot += 1
            E = dict(zip(D, eps))
            sl = (N + 1) * sum(E[a] for a in D if a not in mxs) - sum((sum(a) - 1) * E[a] for a in mx)
            if worst is None or sl < worst[0]: worst = (sl, m, D, b)
            if sl < 0:
                fail += 1
                if fail <= 5: print("TILEMAX FAIL m=%d D=%s b=%s shift=%d slack=%d" % (m, D, b, sh, sl), flush=True)
    print("m=%d: tiles x b tested %d, failures %d, worst slack %s" % (m, tot, fail, worst[0] if worst else None), flush=True)
