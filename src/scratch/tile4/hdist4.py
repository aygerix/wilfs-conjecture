# Per m (e=5 domain): min H/m, min (m+1)H/Tg, min R/Tg, and min HCR among tiles with H/m below a cut,
# plus the max level N and t of the min-H tile. Tests whether "small H" tiles (thin) persist as m grows.
import gzip, json, sys
from hcr4_low import analyse
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for m in range(lo, hi + 1):
    Tg = 3 * m * (m - 1) / 2; mh = (9e9, None); mr = 9e9; cnt = 0; hist = {}
    with gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r = rec['r']
            if len(set(r)) < 4 or 0 in r: continue
            for D in rec['tile_cells']:
                S = set(map(tuple, D))
                if any(tuple(int(i == a) for i in range(4)) not in S for a in range(4)): continue
                z = analyse(D); cnt += 1; hm = z['H'] / m
                k = min(int(hm * 2) / 2, 5); hist[k] = hist.get(k, 0) + 1
                if hm < mh[0]: mh = (hm, (tuple(r), round(float(z['hcr']), 3), z['t'], z['lev'][:3], round(z['R'] / Tg, 3)))
                mr = min(mr, z['R'] / Tg)
    print(f"m {m} n={cnt} minH/m {mh[0]:.3f} {mh[1]} minR/Tg {mr:.3f} hist(H/m) {dict(sorted(hist.items()))}", flush=True)
