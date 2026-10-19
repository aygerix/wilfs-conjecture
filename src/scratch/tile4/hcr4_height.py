# e = 5 tiles (4-D, distinct nonzero residues, every e_a in D) from the exact enumeration certificates (E153), split
# by tile height h(D) = max |x|  (lead, 2026-10-19).  Height <= 3 tiles are covered by height-3 MaxCL (codex P6, if it
# is proved), so the question is what the remaining height >= 4 tiles need: per m, the minimum HCR and minimum H/m
# (H = the HCR column-headroom sum of hcr4_low.py) separately for h <= 3 and h >= 4.
# usage (in the certificate directory): python hcr4_height.py lo hi
import gzip, json, sys
from hcr4_low import analyse
if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for m in range(lo, hi + 1):
        st = {}
        with gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt') as f:
            for line in f:
                rec = json.loads(line); r = rec['r']
                if len(set(r)) < 4 or 0 in r: continue
                for D in rec['tile_cells']:
                    S = set(map(tuple, D))
                    if any(tuple(int(i == a) for i in range(4)) not in S for a in range(4)): continue
                    h = max(sum(x) for x in S); key = '<=3' if h <= 3 else '>=4'
                    z = analyse(D)
                    s = st.setdefault(key, [0, None, None, {}])
                    s[0] += 1; s[3][h] = s[3].get(h, 0) + 1
                    if s[1] is None or z['hcr'] < s[1][0]: s[1] = (z['hcr'], tuple(r), h, z['t'])
                    if s[2] is None or z['H'] < s[2][0]: s[2] = (z['H'], tuple(r), h, z['t'])
        out = []
        for key in ('<=3', '>=4'):
            if key in st:
                n, mh, mH, hd = st[key]
                out.append(f"h{key}: n={n} minHCR={float(mh[0]):.4f} r{mh[1]} h={mh[2]} t={mh[3]}  minH/m={mH[0]/m:.3f} r{mH[1]} h={mH[2]} t={mH[3]}  heights={dict(sorted(hd.items()))}")
        print(f"m {m}: " + " | ".join(out), flush=True)
