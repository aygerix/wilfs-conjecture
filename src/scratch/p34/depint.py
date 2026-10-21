r"""Candidate lattice-tile inequalities for Dep (lead, 2026-10-20): i = |interior|, a = |A|, b = |bd \ A|.
 H1: Dep >= (d-1)(i-1);   H2: Dep >= d(i-1) - (number of maximal cells of height >= 2)... (reported, not asserted);
 also the minimum of Dep/((d-1)(i-1)) and the SC1 slack.  Usage: python depint.py sg NS SEED MMIN MMAX | tiles N MMIN MMAX"""
import sys, random, itertools
sys.path.insert(0, '.')
from crsc import stats
def show(tag, D, N):
    sl, s1, s2, a, i, dep = stats(D, N); m = len(D)
    return dep - (N - 1) * (i - 1), (dep / ((N - 1) * (i - 1)) if i > 1 and N > 1 else None), s1, a, i, dep
if __name__ == '__main__':
  if sys.argv[1] == 'sg':
    from tile import build
    NS, SEED, MMIN, MMAX = map(int, sys.argv[2:6]); rnd = random.Random(SEED); cnt = f = fo = 0; wr = None
    while cnt < NS:
        m = rnd.randint(MMIN, MMAX); k = rnd.randint(2, max(2, m // 2)); c0 = rnd.randint(m + 1, 10 * m)
        G = sorted(rnd.sample(range(m + 1, min(rnd.choice([2 * m, 3 * m, c0 + m]), c0 + m)), min(k, c0 - 1)))
        R = build(m, G)
        if R is None: continue
        c, gens, M = R; d = len(gens)
        if d < 2: continue
        cnt += 1; h1, rat, s1, a, i, dep = show('', list(M), d)
        if h1 < 0: f += 1; fo += 3 * (d + 1) < m
        if rat is not None and (wr is None or rat < wr[0]): wr = (rat, m, gens, a, i, dep)
    print("S %d  H1 fails %d (open %d)  min Dep/((d-1)(i-1)) %s" % (cnt, f, fo, wr))
  else:
    from subadd_lp import downsets
    N, MMIN, MMAX = map(int, sys.argv[2:5])
    for m in range(MMIN, MMAX + 1):
        tot = f = 0; wr = None
        for D in downsets(N, m):
            if not any(len({sum(x * y for x, y in zip(a, b)) % m for a in D}) == m for b in itertools.product(range(1, m), repeat=N)): continue
            tot += 1; h1, rat, s1, a, i, dep = show('', D, N)
            if h1 < 0: f += 1
            if rat is not None and (wr is None or rat < wr[0]): wr = (round(rat, 3), D if m < 10 else m, a, i, dep)
        print("N=%d m=%d tiles %d H1 fails %d  min ratio %s" % (N, m, tot, f, wr), flush=True)
