# Hunt TL failures with e >= 5 and m | c (generators in (m, 2m) to create relations p_a + p_b = m + p_c), plus two-face check.
import sys, random, time
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from cl import factorizations_down_set
from topload import topload
e0, e1, seed, budget = map(int, sys.argv[1:5])
rnd = random.Random(seed); t0 = time.time(); n = 0; fails = []; worst = {}
while time.time() - t0 < budget:
    e = rnd.randint(e0, e1); m = rnd.randint(3 * e + 1, 48); q = rnd.randint(4, 6)
    gens = [m] + rnd.sample(range(m + 1, 2 * m), e - 1)
    try: s = NS.from_generators(gens + list(range(q * m, q * m + m + 1)))
    except ValueError: continue
    if s.e < e0 or s.c % s.m or s.c <= 3 * s.m or 3 * s.e >= s.m: continue
    L, d, tau = topload(s); n += 1
    r = L / (d + 1)
    if s.e not in worst or r > worst[s.e][0]: worst[s.e] = (round(r, 3), s.P, s.m, s.c, tau)
    if L > d + 1 + 1e-9: fails.append((s.P, s.m, s.c, d, tau, round(L, 3)))
print(f'e in [{e0},{e1}], m|c, c>3m, 3e<m, gens<2m, seed {seed}: {n} S, TL fails {len(fails)}; {time.time()-t0:.0f}s')
for e in sorted(worst): print('  e', e, 'worst L*/(d+1)', worst[e])
for f in fails[:8]: print('  FAIL', f)
