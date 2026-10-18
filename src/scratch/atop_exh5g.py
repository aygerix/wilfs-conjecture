# Exhaustive ATOP_gamma: every S = <m, m+s1, ..., m+s_{e-1}> with generators < 2m, embedding dimension e, c > 3m (any c).
import sys, itertools, time; sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0]); sys.path.insert(0, 'src')
from ns import NS
from atop_g import atop_g
e, m = int(sys.argv[1]), int(sys.argv[2]); t0 = time.time(); n = bad = 0; worst = None; wmc = None
for S in itertools.combinations(range(1, m), e - 1):
    try: s = NS.from_generators([m] + [m + x for x in S])
    except ValueError: continue
    if s.e != e or s.c <= 3 * m: continue
    ra, rt = atop_g(s); n += 1
    if ra > 1 + 1e-9: bad += 1; print('FAIL', s.P, 'c', s.c, 'gamma', s.c % m, f'{ra:.4f}', flush=True)
    if worst is None or ra > worst[0]: worst = (round(ra, 4), s.P, s.c, s.c % m)
print(f'e={e} m={m}: {n} S (gens<2m, c>3m, any c), ATOP_gamma fails {bad}, worst {worst}, {time.time()-t0:.0f}s', flush=True)
