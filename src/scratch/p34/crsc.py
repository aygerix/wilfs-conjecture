r"""Coarse sufficient conditions for CR_DEP (lead, 2026-10-20), using n_k >= |A| for k <= d+1, n_1 = |boundary|:
 SC1: C(|bd|,2) + d C(|A|,2) + m Dep >= (d-1) C(m,2);
 SC2: C(|bd|,2) + sum_{k>=2} C(#{y in A: d+|y| >= k}, 2) + m Dep >= (d-1) C(m,2)  (only maximal weights beyond k = 1).
Tested on lex tiles of random S (open regime and all) and on all 3-D tiles.  Usage: python crsc.py sg NS SEED MMIN MMAX | tiles MMIN MMAX"""
import sys, random, itertools
sys.path.insert(0, '.')
from crdep import crdep
def stats(D, N):
    Ds = set(D); m = len(D)
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    A = [x for x in D if all(up(x, b) not in Ds for b in range(N))]
    I = [x for x in D if all(up(x, b) in Ds for b in range(N))]
    bd = m - len(I)
    sl, dep = crdep(D, N)
    C2 = lambda n: n * (n - 1) // 2
    rhs = (N - 1) * C2(m)
    sc1 = C2(bd) + N * C2(len(A)) + m * dep - rhs
    ws = [N + sum(y) for y in A]
    sc2 = C2(bd) + sum(C2(sum(1 for w in ws if w >= k)) for k in range(2, max(ws) + 1)) + m * dep - rhs
    return sl, sc1, sc2, len(A), len(I), dep
if __name__ == '__main__':
  if sys.argv[1] == 'sg':
    from tile import build
    NS, SEED, MMIN, MMAX = map(int, sys.argv[2:6]); rnd = random.Random(SEED)
    cnt = f1 = f2 = fo1 = fo2 = no = 0; w2 = None
    while cnt < NS:
        m = rnd.randint(MMIN, MMAX); k = rnd.randint(2, max(2, m // 2)); c0 = rnd.randint(m + 1, 10 * m)
        G = sorted(rnd.sample(range(m + 1, min(rnd.choice([2 * m, 3 * m, c0 + m]), c0 + m)), min(k, c0 - 1)))
        R = build(m, G)
        if R is None: continue
        c, gens, M = R; d = len(gens)
        if d < 2: continue
        cnt += 1; sl, s1, s2, a, i, dep = stats(list(M), d); op = 3 * (d + 1) < m
        no += op
        if s1 < 0: f1 += 1; fo1 += op
        if s2 < 0:
            f2 += 1; fo2 += op
            if op and (w2 is None or s2 / m / m < w2[0]): w2 = (s2 / m / m, sl / m / m, m, gens, a, i, dep)
    print("S %d (open %d): SC1 fails %d (open %d), SC2 fails %d (open %d)" % (cnt, no, f1, fo1, f2, fo2)); print("  worst SC2 open:", w2)
  else:
    from subadd_lp import downsets
    MMIN, MMAX = map(int, sys.argv[2:4])
    for m in range(MMIN, MMAX + 1):
        f1 = f2 = tot = 0
        for D in downsets(3, m):
            if not any(len({sum(x * y for x, y in zip(a, b)) % m for a in D}) == m for b in itertools.product(range(1, m), repeat=3)): continue
            tot += 1; sl, s1, s2, a, i, dep = stats(D, 3); f1 += s1 < 0; f2 += s2 < 0
        print("3-D tiles m=%d: %d  SC1 fails %d  SC2 fails %d" % (m, tot, f1, f2), flush=True)
