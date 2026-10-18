# d = 3 tiles: per-direction excess E_a(s) = X_a(s) - M' (X_a = sum_x r(t_a x)), pair sums, and total.
# Tile-CL: E_1+E_2+E_3 <= M'.  Question: is every pair E_a+E_b <= M' (pairwise 2-D Tile-CL inside a 3-D tile)?
import sys
import numpy as np
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    M = m*(m - 1)//2
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    K = np.arange(m)
    worst_pair = -10**9; worst_single = -10**9; worst_tot = -10**9; nt = 0; pair_fail = 0; ex = None
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.all(np.sort(pos, axis=1) == K, axis=1)
        if not ok.any(): continue
        tau = tops(D, d)
        Tidx = []
        for a in range(d):
            Tidx.append([Dl.index(tuple(x[:a]) + (tau[x][a],) + tuple(x[a+1:])) for x in Dl])
        for row in pos[ok]:
            nt += 1
            R = (row[None, :] - K[:, None]) % m          # (s, cell) r values
            E = [R[:, Tidx[a]].sum(axis=1) - M for a in range(d)]
            pairs = [E[0] + E[1], E[0] + E[2], E[1] + E[2]]
            pm = max(p.max() for p in pairs)
            if pm > M:
                pair_fail += 1
                if ex is None: ex = (Dl, row.tolist())
            worst_pair = max(worst_pair, pm / M); worst_single = max(worst_single, max(e.max() for e in E) / M)
            worst_tot = max(worst_tot, (E[0] + E[1] + E[2]).max() / M)
    print(f'm={m}: tiles {nt}, max pair excess/M\' {worst_pair:.3f} (pair > M\' in {pair_fail}), max single {worst_single:.3f}, max total {worst_tot:.3f}', ex if ex and m < 9 else '', flush=True)
