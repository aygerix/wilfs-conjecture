# Where does the d-dimensional height criterion fail for fixed e? (all c; record m of failures and min ratio by m band)
import sys, random, time
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from math import comb, gcd
from functools import reduce
from ns import NS
from shape_d import shape
e, mlo, mhi, seed, budget = map(int, sys.argv[1:6])
rnd = random.Random(seed); t0 = time.time(); fails = {}; band = {}; n = 0
while time.time() - t0 < budget:
    m = rnd.randint(mlo, mhi); K = rnd.choice((2, 3, 4, 6, 10))
    g = sorted(rnd.sample(range(m + 1, K * m), e - 1))
    if reduce(gcd, [m] + g) != 1: continue
    s = NS.from_generators([m] + g)
    if s.e != e or s.m != m: continue
    d, H, MS, ok, sl = shape(s); n += 1
    b = 10 * (m // 10); r = (m + 1) * H / max(1, (d - 1) * comb(m, 2) - m)
    if b not in band or r < band[b][0]: band[b] = (round(r, 3), [m] + g, s.c)
    if not ok: fails[m] = fails.get(m, 0) + 1
print(f'e={e} m in [{mlo},{mhi}] seed {seed}: {n} S, {time.time()-t0:.0f}s; HT_d failures by m: {dict(sorted(fails.items()))}')
for b in sorted(band): print('  m band', b, 'min ratio', band[b])
