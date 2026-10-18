# Exhaustive HCR: every S = <m, m+s1, ..., m+s_{e-1}> with generators < 2m, embedding dimension e, c > 3m.
import sys, itertools, time; sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0]); sys.path.insert(0, 'src')
from ns import NS
from hcr import parts
e, m = int(sys.argv[1]), int(sys.argv[2]); t0 = time.time(); n = {False: 0, True: 0}; bad = {False: 0, True: 0}; worst = {False: None, True: None}
for S in itertools.combinations(range(1, m), e - 1):
    try: s = NS.from_generators([m] + [m + x for x in S])
    except ValueError: continue
    if s.e != e or s.c <= 3 * m: continue
    h, ht, two, W = parts(s); n[two] += 1
    if h < 1 - 1e-12: bad[two] += 1; print('HCR-FAIL', 'two-face' if two else 'NON-TWO-FACE', s.P, 'c', s.c, 'W', W, f'{h:.4f}', flush=True)
    if worst[two] is None or h < worst[two][0]: worst[two] = (round(h, 4), s.P)
print(f'e={e} m={m}: non-two-face {n[False]} S, HCR fails {bad[False]}, worst {worst[False]} | two-face {n[True]}, fails {bad[True]}, worst {worst[True]} | {time.time()-t0:.0f}s', flush=True)
