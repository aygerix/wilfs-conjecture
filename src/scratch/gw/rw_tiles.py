# Exhaustive test of RW on every enumerated 4-D tile (e = 5 domain) and every unit u (each (D, u.r) is realized by some S:
# the open Groebner cone of D contains integer points in every residue class, with all n_a > m):
#   RW(D, s):  d m max_D x.s - (d+1) sum_D x.s >= (d-1) m (m-1)/2,   s = (u r mod m) in [1, m-1]^4.
import gzip, json, sys
from math import gcd
lo, hi = int(sys.argv[1]), int(sys.argv[2]); d = 4
for m in range(lo, hi + 1):
    units = [u for u in range(1, m) if gcd(u, m) == 1]; tgt = (d - 1) * m * (m - 1) // 2
    n = fails = 0; worst = None; eq = 0
    with gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r = rec['r']
            if 0 in r or len(set(r)) < 4: continue
            for D in rec['tile_cells']:
                S = set(map(tuple, D))
                if any(tuple(int(i == a) for i in range(4)) not in S for a in range(4)): continue
                cols = [sum(x[a] for x in D) for a in range(4)]
                for u in units:
                    s = [u * ri % m for ri in r]
                    mx = max(sum(a * b for a, b in zip(x, s)) for x in D)
                    ex = d * m * mx - (d + 1) * sum(c * si for c, si in zip(cols, s)) - tgt
                    n += 1; eq += ex == 0
                    if ex < 0:
                        fails += 1
                        if worst is None or ex < worst[0]: worst = (ex, r, u, sorted(D))
    print(f"m={m}: {n} (tile, unit) pairs, RW fails {fails}, equality {eq}" + (f", worst excess {worst[0]} r={worst[1]} u={worst[2]}" if worst else ''), flush=True)
    if worst: print('   tile', worst[3], flush=True)
