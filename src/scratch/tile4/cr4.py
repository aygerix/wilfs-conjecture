# Crude MaxCL bound CR on every e = 5 tile of the exact 4-D enumeration (E153 certificates), by m and height
# (lead, 2026-10-19).  CR: sum_i w_i (m-1-i) <= (d+1)|N|(|N|-1)/2 with w = (|y|-1) over maximal y sorted decreasing;
# CR implies MaxCL at every sigma (shape-only).  Prints per m: #tiles, #CR failures, failure counts by height, and the
# minimum CR ratio rhs/lhs.
# usage (in the certificate directory): python cr4.py lo hi
import gzip, json, sys
if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2]); d = 4
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    for m in range(lo, hi + 1):
        n = 0; nf = 0; byh = {}; tot = {}; mr = None
        with gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt') as f:
            for line in f:
                rec = json.loads(line); r = rec['r']
                if len(set(r)) < 4 or 0 in r: continue
                for D in rec['tile_cells']:
                    S = set(map(tuple, D))
                    if any(u not in S for u in U): continue
                    A = [y for y in S if all(tuple(y[i] + U[a][i] for i in range(d)) not in S for a in range(d))]
                    w = sorted((sum(y) - 1 for y in A), reverse=True)
                    lhs = sum(wi * (m - 1 - i) for i, wi in enumerate(w)); nN = m - len(A)
                    rhs = (d + 1) * nN * (nN - 1) // 2
                    h = max(sum(x) for x in S); n += 1; tot[h] = tot.get(h, 0) + 1
                    rat = rhs / lhs if lhs > 0 else float('inf')
                    if mr is None or rat < mr[0]: mr = (round(rat, 4), tuple(r), h)
                    if lhs > rhs: nf += 1; byh[h] = byh.get(h, 0) + 1
        print(f"m {m}: tiles {n} CR-fail {nf} ({100*nf/max(1,n):.1f}%) fail-by-height {dict(sorted(byh.items()))} of {dict(sorted(tot.items()))} min rhs/lhs {mr}", flush=True)
