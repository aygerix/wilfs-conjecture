import sys, itertools
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
import importlib.util
spec = importlib.util.spec_from_file_location('h3', 'src/scratch/height3.py')
src = open('src/scratch/height3.py').read().split('rng = random.Random')[0]
ns = {}; exec(src, ns); check = ns['check']
for d, mmax in [(2, 11), (3, 10), (4, 8), (5, 7)]:
    for m in range(3, mmax + 1):
        n = f = 0; ex = None
        for D in downsets(m, d):
            if max(sum(x) for x in D) > 3: continue
            if any(all(x[a] == 0 for x in D) for a in range(d)): continue
            for p in itertools.product(range(1, m), repeat=d):
                ph = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
                if len(set(ph.values())) != m: continue
                n += 1
                (sl, sg), ml = check(ph, d, m)
                if sl < 0:
                    f += 1
                    if ex is None: ex = (sorted(D), p, sg, sl)
        print('d', d, 'm', m, 'height<=3 tiles', n, 'scheme fails', f, ex, flush=True)
