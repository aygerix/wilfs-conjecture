"""For crude-failing 4-D tiles (height >= 4): largest h with the coordinate simplex Delta_h inside D, |D \\ Delta_h|,
and the max-Omega tile per m (lead 2026-10-19).  usage: python crude_fail_simplex.py mlo mhi certdir"""
import gzip, json, sys
from math import comb
from collections import Counter
mlo, mhi, cdir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
for m in range(mlo, mhi+1):
    hc = Counter(); best = None
    with gzip.open(f'{cdir}/certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r = rec['r']
            if len(set(r)) < 4 or 0 in r: continue
            d = 4
            for Dl in rec['tile_cells']:
                D = set(map(tuple, Dl))
                if any(tuple(int(i == a) for i in range(d)) not in D for a in range(d)): continue
                if max(sum(x) for x in D) < 4: continue
                up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
                A = [y for y in D if all(up(y, a) not in D for a in range(d))]
                Om = sum(d+sum(y) for y in A)
                if 2*Om <= (d+1)*m: continue
                # largest h with Delta_h subset of D: every cell of degree <= h present
                lev = Counter(sum(x) for x in D); h = 0
                while lev.get(h+1, 0) == comb(h+1+d-1, d-1): h += 1
                hc[(h, m-comb(h+d, d))] += 1
                if best is None or Om > best[0]: best = (Om, r, sorted(lev.items()), sorted(Counter(sum(y) for y in A).items()))
    print("m=%d (h, |D|-|Delta_h|) counts:" % m, sorted(hc.items()), "| max Omega/m %.3f r=%s levels(D)=%s levels(A)=%s" % (best[0]/m, best[1], best[2], best[3]), flush=True)
