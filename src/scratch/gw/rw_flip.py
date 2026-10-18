# Is RW a statement about ALL residue-bijective down-sets (fundamental domains), or does it need the Groebner property?
# Random walk by flips: remove a maximal cell y, add a cell q not in D with q = y mod L whose predecessors are in D \ {y}.
# Test RW(D, u r mod m) for all units u along the walk; record failures (and whether the set is a Groebner tile).
import sys, random, itertools; sys.path.insert(0, 'src')
from math import gcd
from tile_enum import canonical_residues, enumerate_lattice
rnd = random.Random(int(sys.argv[1])); d = 3; steps = int(sys.argv[4])
def rw_excess(D, s, m):
    cols = [sum(x[a] for x in D) for a in range(d)]
    return d * m * max(sum(a * b for a, b in zip(x, s)) for x in D) - (d + 1) * sum(c * si for c, si in zip(cols, s)) - (d - 1) * m * (m - 1) // 2
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
tot = fails = nong = 0; worst = None
for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    units = [u for u in range(1, m) if gcd(u, m) == 1]
    for r in canonical_residues(m):
        if 0 in r or len(set(r)) < 3: continue
        tiles = set(enumerate_lattice(m, tuple(r)))
        D = set(rnd.choice(sorted(tiles, key=sorted)))
        res = lambda x: sum(a * b for a, b in zip(x, r)) % m
        for st in range(steps):
            mx = [y for y in D if all(add(y, u) not in D for u in U) and sum(y) > 0]
            y = rnd.choice(mx); D.remove(y); ry = res(y)
            cand = [add(x, u) for x in D for u in U if add(x, u) not in D and add(x, u) != y and res(add(x, u)) == ry
                    and all(sub(add(x, u), U[a]) in D for a in range(d) if add(x, u)[a] > 0)]
            if not cand: D.add(y); continue
            D.add(rnd.choice(cand))
            if any(u not in D for u in U): continue
            g = frozenset(D) in tiles; nong += not g
            for u in units:
                s = [u * ri % m for ri in r]; ex = rw_excess(D, s, m); tot += 1
                if ex < 0:
                    fails += 1
                    if worst is None or ex < worst[0]: worst = (ex, m, r, u, g, sorted(D))
    print(f"m={m}: tested {tot} (set, unit) pairs so far, non-Groebner sets {nong}, RW fails {fails}", flush=True)
print('worst', worst)
