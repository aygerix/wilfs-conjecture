# validate src/tile_enum.py: every grlex Apery tile of every e = 4 semigroup <m,a,b,c> (gens < K m) appears among the
# enumerated tiles of its canonical lattice (after the unit/permutation canonicalisation).   usage: m0 m1 K
import sys, itertools
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
from tile_enum import enumerate_lattice, canonical_residues
m0, m1, K = map(int, sys.argv[1:4])
for m in range(m0, m1 + 1):
    units = [u for u in range(1, m) if gcd(u, m) == 1]
    canon = set(canonical_residues(m)); cache = {}
    n = miss = 0; shapes = set()
    for g3 in itertools.combinations(range(m + 1, K*m), 3):
        if reduce(gcd, (m,) + g3) != 1: continue
        s = NS.from_generators([m, *g3])
        if s.e != 4: continue
        p, best = factorizations_down_set(s, 'grlex'); D = set(best.values())
        r = tuple(x % m for x in p)
        ok = False
        for u in units:
            ur = [(u*x) % m for x in r]
            c = tuple(sorted(ur))
            if c not in canon: continue
            if c not in cache: cache[c] = enumerate_lattice(m, c)
            for sig in itertools.permutations(range(3)):
                if tuple(ur[sig[i]] for i in range(3)) != c: continue
                D2 = frozenset(tuple(x[sig[i]] for i in range(3)) for x in D)
                if D2 in cache[c]: ok = True; shapes.add((c, D2)); break
            if ok: break
        n += 1
        if not ok:
            miss += 1
            if miss <= 3: print('  MISSING', [m, *g3], r)
    tot = sum(len(v) for v in cache.values())
    print(f'm={m}: semigroups {n}, missing {miss}; distinct tiles realised {len(shapes)} of {tot} enumerated (lattices touched {len(cache)})', flush=True)
