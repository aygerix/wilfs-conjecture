import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from naw import split
fam = []
for a in range(4, 14): fam.append(('box', [a*a, a*a + 1, a*a + a, a*a + a + 1]))
for m in (20, 31, 50, 77, 101): fam.append(('AP', [m, m + 1, m + 2, m + 3]))
for m in (30, 60, 90):
    for k in (2, 3, 5, 7, 11):
        fam.append((f'mk{k}', [m, m + 1, m + k, m + k + 1]))
for n in (2, 3):     # Backelin: s = r(3n+2)+3, <s, s+3, s+3n+1, s+3n+2>
    for r in (3*n + 2, 3*n + 3):
        s0 = r*(3*n + 2) + 3; fam.append((f'Back{n},{r}', [s0, s0 + 3, s0 + 3*n + 1, s0 + 3*n + 2]))
rng = random.Random(7)
while len(fam) < 400:
    m = rng.randint(20, 200); k = rng.choice([2, 3, 4, 6])
    g = sorted(set([m] + [rng.randint(m + 1, k*m) for _ in range(3)]))
    if len(g) == 4 and reduce(gcd, g) == 1: fam.append(('rnd', g))
worst = {}
for name, g in fam:
    s = NS.from_generators(g)
    if s.e != 4: continue
    r = split(s); ratio = r['NA']/r['need']
    key = name if name in ('rnd',) else name.split(',')[0][:4]
    if key not in worst or ratio < worst[key][0]: worst[key] = (round(ratio, 3), g, r['N'], r['m'])
    if name != 'rnd': print(name, g, 'NA/need', round(ratio, 3), 'N', r['N'], 'W', s.W)
print('WORST by family:', worst)
