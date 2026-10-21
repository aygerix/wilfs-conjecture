r"""DEP-CARRY / S1 normalized slack in the open Wilf regime (lead, 2026-10-20): random S with 3e < m, c > 4m.
DEP slack (label units) = m (V + Dep), S1 slack = m (V + BD), V = s + sum kappa_s.  Reports min over S of
min_{phases, units} (V+Dep)/m and (V+BD)/m, and the values at the conductor phase.  Usage: python depopen.py NS SEED MMIN MMAX"""
import sys, random
from math import gcd
sys.path.insert(0, '.')
from tile import build
from depforms import forms
NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
cnt = 0; wa = wb = wc = None
while cnt < NS:
    m = rnd.randint(MMIN, MMAX); e = rnd.randint(3, max(3, m // 3 - 1)); c0 = rnd.randint(4 * m + 1, 10 * m)
    hi = rnd.choice([2 * m, 3 * m, c0])
    G = sorted(rnd.sample(range(m + 1, min(hi, c0 + m)), e - 1))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R
    if c <= 4 * m or 3 * (len(gens) + 1) >= m or len(gens) < 2: continue
    cnt += 1; D = list(M); delta0 = [g % m for g in gens]
    V, dep, BD, RA = forms(m, D, delta0, (-c) % m)
    if wc is None or (V + dep) / m < wc[0]: wc = ((V + dep) / m, (V + BD) / m, m, gens, c)
    us = [u for u in range(2, m) if gcd(u, m) == 1]
    for u in [1] + rnd.sample(us, min(3, len(us))):
        delta = [(u * g) % m for g in gens]
        for s in range(m):
            V, dep, BD, RA = forms(m, D, delta, s)
            if wa is None or (V + dep) / m < wa[0]: wa = ((V + dep) / m, u, s, m, gens, c)
            if wb is None or (V + BD) / m < wb[0]: wb = ((V + BD) / m, u, s, m, gens, c)
print("open-regime S: %d" % cnt)
print("  min (V+Dep)/m over phases/units:", wa)
print("  min (V+BD)/m  over phases/units:", wb)
print("  min (V+Dep)/m at the conductor phase:", wc)
