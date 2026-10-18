# Variants of the plateau bound over the complete enumeration (non-two-face):
#   LB2 = sum_a max(B_{a|b}, B_{a|c});  LBavg = sum_a (B_{a|b}+B_{a|c})/2;  LBcyc = max(sum_a B_{a|a+1}, sum_a B_{a|a-1}).
# usage: plateau_var.py m...    (prints min (bound - (m-1)) per variant, and #fails)
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
from plateau_lb import B
for m in map(int, sys.argv[1:]):
    res = {}
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        D = set(D)
        Bt = {(a, b): B(D, a, b) for a in range(3) for b in range(3) if a != b}
        vals = {'LB2': sum(max(Bt[a, (a+1) % 3], Bt[a, (a+2) % 3]) for a in range(3)),
                'LBavg': sum(Bt[a, (a+1) % 3] + Bt[a, (a+2) % 3] for a in range(3)) / 2,
                'LBcyc': max(sum(Bt[a, (a+1) % 3] for a in range(3)), sum(Bt[a, (a+2) % 3] for a in range(3)))}
        for k, v in vals.items():
            v -= m - 1
            n, f, w = res.get(k, (0, 0, None))
            res[k] = (n + 1, f + (v < 0), w if (w is not None and w[0] <= v) else (v, r))
    print(f'm={m}:', {k: (f, w) for k, (n, f, w) in res.items()}, flush=True)
