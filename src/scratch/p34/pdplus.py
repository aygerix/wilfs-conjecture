r"""PD+ (lead, 2026-10-20): sum over cell pairs of (Hamming distance - 1) <= m Dep + sum over pairs of maximal cells of
(min(|s|,|t|) - |s ^ t|), s ^ t = coordinatewise min.  PD+ implies CR_DEP (min of sums >= sum of per-direction mins,
exact on maximal pairs).  Tests: random S, all 3-D tiles, all 4-D down-sets.  Usage: python pdplus.py sg NS SEED MMIN MMAX | tiles N MMIN MMAX"""
import sys, random, itertools
sys.path.insert(0, '.')
from crdep import crdep
def pdplus(D, N):
    Ds = set(D); m = len(D)
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    mx = [x for x in D if all(up(x, b) not in Ds for b in range(N))]
    sl, dep = crdep(D, N)
    ham = 0
    for i in range(m):
        for j in range(i + 1, m):
            ham += sum(1 for t in range(N) if D[i][t] != D[j][t]) - 1
    gain = 0
    for i in range(len(mx)):
        for j in range(i + 1, len(mx)):
            s, t = mx[i], mx[j]; gain += min(sum(s), sum(t)) - sum(min(a, b) for a, b in zip(s, t))
    return m * dep + gain - ham, sl
if __name__ == '__main__':
  if sys.argv[1] == 'sg':
    from tile import build
    NS, SEED, MMIN, MMAX = map(int, sys.argv[2:6]); rnd = random.Random(SEED); cnt = no = f = fo = 0; w = None
    while cnt < NS:
        m = rnd.randint(MMIN, MMAX); k = rnd.randint(2, max(2, m // 2)); c0 = rnd.randint(m + 1, 10 * m)
        G = sorted(rnd.sample(range(m + 1, min(rnd.choice([2 * m, 3 * m, c0 + m]), c0 + m)), min(k, c0 - 1)))
        R = build(m, G)
        if R is None: continue
        c, gens, M = R; d = len(gens)
        if d < 2: continue
        cnt += 1; op = 3 * (d + 1) < m; no += op; v, sl = pdplus(list(M), d)
        if v < 0:
            f += 1; fo += op
            if w is None or v / m / m < w[0]: w = (v / m / m, sl / m / m, m, gens, op)
    print("S %d (open %d): PD+ fails %d (open %d)  worst %s" % (cnt, no, f, fo, w))
  else:
    N, MMIN, MMAX = map(int, sys.argv[2:5])
    from subadd_lp import downsets
    for m in range(MMIN, MMAX + 1):
        tot = f = 0; w = None
        for D in downsets(N, m):
            if not any(len({sum(x * y for x, y in zip(a, b)) % m for a in D}) == m for b in itertools.product(range(1, m), repeat=N)): continue
            tot += 1; v, sl = pdplus(D, N)
            if v < 0:
                f += 1
                if w is None or v < w[0]: w = (v, sl, D if m < 11 else '')
        print("N=%d m=%d tiles %d PD+ fails %d worst %s" % (N, m, tot, f, w), flush=True)
