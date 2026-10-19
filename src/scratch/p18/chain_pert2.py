"""Two-generator perturbations of failing interval cores (lead): S = <m, 2m+[a..b], x, y>, x, y in (m,2m) u (3m,4m).
Reports failures by height and the min ratio among height >= 3.  usage: python chain_pert2.py m a b stride"""
import sys
from chain_interval import chain_stats
from chain_height import minlen_profile
m, a, b, st = map(int, sys.argv[1:5])
base = list(range(2*m + a, 2*m + b + 1))
cand = list(range(m + 1, 2*m, st)) + list(range(3*m + 1, 4*m, st))
f2 = f3 = tot3 = 0; best3 = None
for i, x in enumerate(cand):
    for y in cand[i + 1:]:
        r = chain_stats(m, base + [x, y])
        if not r or r['q'] < 4: continue
        h, n3 = minlen_profile(m, r['gens'])
        if h >= 3:
            tot3 += 1
            if best3 is None or r['ratio'] < best3[0]: best3 = (round(r['ratio'], 4), x, y, r['e'], r['q'], h, n3)
            if r['ratio'] < 1: f3 += 1; print('H3FAIL', m, x, y, r['ratio'], h, n3, r['gens'], flush=True)
        elif r['ratio'] < 1: f2 += 1
print('m=%d core=[%d,%d]: failures height2=%d height>=3=%d (of %d height>=3); min height>=3: %s' % (m, a, b, f2, f3, tot3, best3), flush=True)
