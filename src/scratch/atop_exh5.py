# Exhaustive: every S = <m, m+s1, ..., m+s4> with 0 < s1 < ... < s4 < m (generators < 2m), e = 5, m | c, c > 3m:
# ATOP with X = top layer, plus two-face flag.  Usage: atop_exh5.py m
import sys, itertools, time; sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0]); sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
from atop_shape import atop_shape
m = int(sys.argv[1]); t0 = time.time(); n = bad = 0; worst = None
for S in itertools.combinations(range(1, m), 4):
    try: s = NS.from_generators([m] + [m + x for x in S])
    except ValueError: continue
    if s.e != 5 or s.c % m or s.c <= 3 * m: continue
    Pp, best = factorizations_down_set(s, 'grlex'); T = sorted(best.values()); lam = {x: w for w, x in best.items()}
    X = [x for x in T if lam[x] >= s.c]
    lhs, rhs, *_ = atop_shape(T, X); n += 1; r = lhs / rhs
    if r > 1 + 1e-9: bad += 1; print('FAIL', s.P, 'c', s.c, f'{r:.4f}', flush=True)
    if worst is None or r > worst[0]: worst = (round(r, 4), s.P, s.c)
print(f'm={m}: {n} S (e=5, gens<2m, m|c, c>3m), ATOP fails {bad}, worst ratio {worst}, {time.time()-t0:.0f}s', flush=True)
