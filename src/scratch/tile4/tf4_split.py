# Two-face 4-D tiles (e=5 domain): split the HCR numerator into
#   X = (m+1) * sum over cross-face singletons (x in N1 for dir b, x in N2 for dir a) of ht(x),
#   Y = (m+1) * (rest of H),   R = sum_i T_(i) i.   Target Tg = 3 m (m-1)/2.
# Report per m: min HCR, min (X+R)/Tg, min X/Tg, and the tile minimizing (X+R)/Tg.
import gzip, json, sys
lo, hi = int(sys.argv[1]), int(sys.argv[2])
U = [tuple(int(i == a) for i in range(4)) for a in range(4)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y))
for m in range(lo, hi + 1):
    Tg = 3 * m * (m - 1) / 2; best = {'hcr': (9, None), 'xr': (9, None), 'x': (9, None)}; n = 0
    with gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r = rec['r']
            if len(set(r)) < 4 or 0 in r: continue
            for Dl in rec['tile_cells']:
                D = set(map(tuple, Dl))
                if any(u not in D for u in U): continue
                two = [(a, b) for a in range(4) for b in range(a + 1, 4) if add(U[a], U[b]) not in D]
                if not two: continue
                n += 1; a, b = two[0]
                ht = {}
                for x in sorted(D, key=lambda x: -sum(x)):
                    ht[x] = max([ht[add(x, u)] + 1 for u in U if add(x, u) in D], default=0)
                X = 0; Hn = 0
                for x in D:
                    for c in range(4):
                        t = x
                        while add(t, U[c]) in D: t = add(t, U[c])
                        Hn += ht[t]
                        if t == x and ((c == b and x[a] >= 1) or (c == a and x[b] >= 1)): X += ht[x]
                A = [y for y in D if ht[y] == 0]
                T = sorted((4 + sum(y) for y in A), reverse=True); R = sum(i * t for i, t in enumerate(T))
                vals = {'hcr': ((m + 1) * Hn + R) / Tg, 'xr': ((m + 1) * X + R) / Tg, 'x': (m + 1) * X / Tg}
                for k, v in vals.items():
                    if v < best[k][0]: best[k] = (v, (tuple(r), round(vals['hcr'], 3), round(vals['xr'], 3), len(A), max(map(sum, D))))
    print(f"m {m} TF n={n} minHCR {best['hcr'][0]:.3f} min(X+R)/Tg {best['xr'][0]:.3f} {best['xr'][1]} min X/Tg {best['x'][0]:.3f}", flush=True)
