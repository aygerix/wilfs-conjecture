r"""CR_DEP on all down-sets of N^4 (lead, 2026-10-20): enumerate 4-D down-sets of size m as chains of 3-D down-sets
(layers x_1 = 0, 1, ...), compute CR_DEP; for each failure decide whether it is a lattice tile (injective labeling
search, randomized then exhaustive).  Usage: python crdep4.py MMIN MMAX"""
import sys, itertools, random
sys.path.insert(0, '.')
from subadd_lp import downsets
from crdep import crdep
MMIN, MMAX = map(int, sys.argv[1:3])
D3 = {0: [frozenset()]}
for k in range(1, MMAX + 1): D3[k] = [frozenset(D) for D in downsets(3, k)]
def chains(rem, prev):
    if rem == 0: yield []; return
    for k in range(min(rem, len(prev)), 0, -1):
        for L in D3[k]:
            if L <= prev:
                for rest in chains(rem - k, L): yield [L] + rest
def is_tile(D, N, m, rnd):
    for _ in range(3000):
        b = [rnd.randrange(1, m) for _ in range(N)]
        if len({sum(x * y for x, y in zip(a, b)) % m for a in D}) == m: return True
    for b in itertools.product(range(1, m), repeat=N):
        if len({sum(x * y for x, y in zip(a, b)) % m for a in D}) == m: return True
    return False
rnd = random.Random(1)
for m in range(MMIN, MMAX + 1):
    tot = fails = tiles = 0; ex = None
    full = frozenset(itertools.product(range(m), repeat=3))
    for ch in chains(m, None if False else frozenset(x for k in range(m + 1) for L in D3.get(k, []) for x in L) | {(0, 0, 0)}):
        D = [(i,) + x for i, L in enumerate(ch) for x in L]
        if len(D) != m: continue
        tot += 1; sl, dep = crdep(D, 4)
        if sl < 0:
            fails += 1
            if is_tile(D, 4, m, rnd):
                tiles += 1
                if ex is None: ex = (sl, sorted(D))
    print("N=4 m=%d down-sets %d  CR_DEP fails %d  of which lattice tiles %d  %s" % (m, tot, fails, tiles, ex), flush=True)
