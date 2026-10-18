# Exhaustive CR: every S = <m, m+s1, ..., m+s_{e-1}> (generators < 2m), embedding dimension e, c > 3m.
# Reports CR failures split by two-face; any NON-two-face failure refutes CR-NTF.
import sys, itertools, time; sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0]); sys.path.insert(0, 'src')
from ns import NS
from cr_test import cr
e, m = int(sys.argv[1]), int(sys.argv[2]); t0 = time.time(); n = {False: 0, True: 0}; bad = {False: 0, True: 0}; worst = {False: None, True: None}
for S in itertools.combinations(range(1, m), e - 1):
    try: s = NS.from_generators([m] + [m + x for x in S])
    except ValueError: continue
    if s.e != e or s.c <= 3 * m: continue
    r, two = cr(s); n[two] += 1
    if r > 1 + 1e-12:
        bad[two] += 1
        if not two: print('NTF-FAIL', s.P, 'c', s.c, f'{r:.4f}', flush=True)
    if worst[two] is None or r > worst[two][0]: worst[two] = (round(r, 4), s.P, s.c)
print(f'e={e} m={m}: non-two-face {n[False]} S, CR fails {bad[False]}, worst {worst[False]} | two-face {n[True]}, fails {bad[True]}, worst {worst[True]} | {time.time()-t0:.0f}s', flush=True)
