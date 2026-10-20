r"""ONE-MAX-TOP (lead, 2026-10-21): in a lattice tile, does every interior cell x != 0 have at most one direction c
whose column top top_c(x) is maximal?  (It implies H1: Dep >= (d-1)(i-1).)  Also tests the variant for all
non-maximal cells x != 0.  Usage: python onemax.py sg NS SEED MMIN MMAX | tiles N MMIN MMAX"""
import sys, random, itertools
sys.path.insert(0, '.')
def check(D, N):
    Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    bad_int = bad_nm = 0; ex = None
    for x in D:
        if x in mx or not any(x): continue
        k = 0
        for b in range(N):
            y = x
            while up(y, b) in Ds: y = up(y, b)
            k += y in mx
        interior = all(up(x, b) in Ds for b in range(N))
        if k >= 2:
            bad_nm += 1
            if interior:
                bad_int += 1
                if ex is None: ex = (x, k)
    return bad_int, bad_nm, ex
if __name__ == '__main__':
  if sys.argv[1] == 'sg':
    from tile import build
    NS, SEED, MMIN, MMAX = map(int, sys.argv[2:6]); rnd = random.Random(SEED); cnt = fi = fn = 0; ex = None
    while cnt < NS:
        m = rnd.randint(MMIN, MMAX); k = rnd.randint(2, max(2, m // 2)); c0 = rnd.randint(m + 1, 10 * m)
        G = sorted(rnd.sample(range(m + 1, min(rnd.choice([2 * m, 3 * m, c0 + m]), c0 + m)), min(k, c0 - 1)))
        R = build(m, G)
        if R is None: continue
        c, gens, M = R; d = len(gens)
        if d < 2: continue
        cnt += 1; bi, bn, e = check(list(M), d); fi += bi > 0; fn += bn > 0
        if e and ex is None: ex = (m, gens, e)
    print("S %d  tiles with an interior x != 0 having >= 2 maximal tops: %d; non-max x: %d; example %s" % (cnt, fi, fn, ex))
  else:
    from subadd_lp import downsets
    N, MMIN, MMAX = map(int, sys.argv[2:5])
    for m in range(MMIN, MMAX + 1):
        tot = fi = fn = 0; ex = None
        for D in downsets(N, m):
            if not any(len({sum(x * y for x, y in zip(a, b)) % m for a in D}) == m for b in itertools.product(range(1, m), repeat=N)): continue
            tot += 1; bi, bn, e = check(D, N); fi += bi > 0; fn += bn > 0
            if e and ex is None: ex = (D, e)
        print("N=%d m=%d tiles %d  interior-violations %d  nonmax-violations %d  %s" % (N, m, tot, fi, fn, ex), flush=True)
