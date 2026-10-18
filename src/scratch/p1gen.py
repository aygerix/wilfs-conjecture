# Generalized P1: for a tile in d dims and a split of directions [d] = S ⊔ S' (both nonempty), let
#   tau_S(x) = x with coordinates in S replaced by their tops (corner of the S-section), similarly tau_S'.
# P1(S,S'):  Y = sum_x [ r(tau_S x) + r(tau_S' x) ] <= 3M'.   (d=3, S={a,b}, S'={c} is the observed P1.)
import sys, itertools
import numpy as np
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = int(sys.argv[1])
splits = []
for k in range(1, d):
    for S in itertools.combinations(range(d), k):
        Sp = tuple(i for i in range(d) if i not in S)
        if S < Sp: splits.append((S, Sp))
for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    M = m*(m-1)//2
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    K = np.arange(m)
    worst = {sp: -10**9 for sp in splits}; nt = 0
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.all(np.sort(pos, axis=1) == K, axis=1)
        if not ok.any(): continue
        # section corner: replace coords in S by tops of the S-section through x (iteratively = coordinatewise tops in
        # the section; for a down-set section the corner is (t_a(x))_{a in S} with x's other coords fixed)
        tau = tops(D, d); Tau = np.array([tau[x] for x in Dl])
        mats = {}
        for S, Sp in splits:
            V1 = C.copy(); V1[:, list(S)] = Tau[:, list(S)]
            V2 = C.copy(); V2[:, list(Sp)] = Tau[:, list(Sp)]
            mats[(S, Sp)] = (V1, V2)
        for pv in P[ok]:
            nt += 1
            for (S, Sp), (V1, V2) in mats.items():
                y1 = (V1 @ pv) % m; y2 = (V2 @ pv) % m
                for s in range(m):
                    Y = int(((y1 - s) % m).sum() + ((y2 - s) % m).sum())
                    worst[(S, Sp)] = max(worst[(S, Sp)], (Y - 3*M) / m)
    print(f'd={d} m={m} tiles {nt}: max (Y-3M\')/m per split:', {f'{S}|{Sp}': w for (S, Sp), w in worst.items()}, flush=True)
