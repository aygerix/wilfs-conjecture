# Number of minimal non-elements (outer corners) of 3-D tiles, by support type; is it bounded?
import sys
import numpy as np
from collections import Counter
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
d = int(sys.argv[1])
for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m); hist = Counter(); supp = Counter(); worst = None; nmax = 0
    for D in downsets(m, d):
        Dl = sorted(D); C = np.array(Dl)
        if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
        pos = (P @ C.T) % m
        if not np.all(np.sort(pos, axis=1) == Kr, axis=1).any(): continue
        cand = set()
        for x in Dl:
            for a in range(d):
                y = list(x); y[a] += 1; y = tuple(y)
                if y not in D and all(y[b] == 0 or tuple(y[:b] + (y[b]-1,) + y[b+1:]) in D for b in range(d)): cand.add(y)
        n = len(cand); hist[n] += 1
        sc = Counter(tuple(b for b in range(d) if y[b]) for y in cand)
        for k, v in sc.items(): supp[(len(k), v)] += 1
        if n > nmax: nmax = n; worst = Dl
    print(f'd={d} m={m}: #outer corners histogram {dict(sorted(hist.items()))}; (|support|, count) {dict(sorted(supp.items()))}', flush=True)
    print('   max example', worst)
