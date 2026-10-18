# RW on every 3-D lattice tile (src/tile_enum.py, the e = 4 domain: distinct nonzero residues, all e_a in D), every unit.
import sys; sys.path.insert(0, 'src')
from math import gcd
from tile_enum import canonical_residues, enumerate_lattice
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    units = [u for u in range(1, m) if gcd(u, m) == 1]; tgt = (d - 1) * m * (m - 1) // 2; n = fails = eq = 0; worst = None
    for r in canonical_residues(m):
        if 0 in r or len(set(r)) < 3: continue
        for D in enumerate_lattice(m, tuple(r)):
            if any(tuple(int(i == a) for i in range(3)) not in D for a in range(3)): continue
            cols = [sum(x[a] for x in D) for a in range(3)]
            for u in units:
                s = [u * ri % m for ri in r]
                ex = d * m * max(sum(a * b for a, b in zip(x, s)) for x in D) - (d + 1) * sum(c * si for c, si in zip(cols, s)) - tgt
                n += 1; eq += ex == 0
                if ex < 0:
                    fails += 1
                    if worst is None or ex < worst[0]: worst = (ex, r, u, sorted(D))
    print(f"m={m}: {n} pairs, RW fails {fails}, equality {eq}" + (f", worst {worst}" if worst else ''), flush=True)
