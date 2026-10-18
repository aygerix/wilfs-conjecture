# phi = S_T/(d m) = fraction of (cell, direction) pairs whose column top is a maximal cell, over e=5 tiles.
# Crude HCR: (m+1)(dm - S_T) + R >= (d-1)m(m-1)/2 holds whenever S_T <= (d+1)m/2 + ~d (phi <= 5/8 + o(1)).
import gzip, json, sys
from fractions import Fraction
from hcr4_low import analyse
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for m in range(lo, hi + 1):
    best = {True: (0, None), False: (0, None)}; cnt = {True: 0, False: 0}; tot = {True: 0, False: 0}
    with gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r = rec['r']
            if len(set(r)) < 4 or 0 in r: continue
            for D in rec['tile_cells']:
                S = set(map(tuple, D))
                if any(tuple(int(i == a) for i in range(4)) not in S for a in range(4)): continue
                z = analyse(D); tf = bool(z['two']); tot[tf] += 1
                if z['phi'] > Fraction(5, 8): cnt[tf] += 1
                if z['phi'] > best[tf][0]: best[tf] = (z['phi'], (r, float(z['hcr']), z['t'], z['lev'][:6], z['ext']))
    for tf in (False, True):
        b = best[tf]
        print(f"m {m} {'TF ' if tf else 'NTF'} n={tot[tf]} #phi>5/8={cnt[tf]} max phi={float(b[0]):.3f} {b[1]}", flush=True)
