# 4-D version of rw_flip.py: start from certificate tiles, random flips, test RW for all units; track non-Groebner sets.
import sys, random, gzip, json
from math import gcd
rnd = random.Random(int(sys.argv[1])); d = 4; steps = int(sys.argv[4]); per = int(sys.argv[5])
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
def ex(D, s, m):
    cols = [sum(x[a] for x in D) for a in range(d)]
    return d * m * max(sum(a * b for a, b in zip(x, s)) for x in D) - (d + 1) * sum(c * si for c, si in zip(cols, s)) - (d - 1) * m * (m - 1) // 2
tot = fails = nong = 0; worst = None
for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    units = [u for u in range(1, m) if gcd(u, m) == 1]
    recs = [json.loads(l) for l in gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt')]
    recs = [r for r in recs if 0 not in r['r'] and len(set(r['r'])) == 4]
    for rec in rnd.sample(recs, min(per, len(recs))):
        r = rec['r']; tiles = {frozenset(map(tuple, D)) for D in rec['tile_cells']}
        res = lambda x: sum(a * b for a, b in zip(x, r)) % m
        D = set(rnd.choice(sorted(tiles, key=sorted)))
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
                e_ = ex(D, [u * ri % m for ri in r], m); tot += 1
                if e_ < 0:
                    fails += 1
                    if worst is None or e_ < worst[0]: worst = (e_, m, r, u, g, sorted(D))
    print(f"m={m}: {tot} pairs so far, non-Groebner sets visited {nong}, RW fails {fails}", flush=True)
print('worst', worst)
