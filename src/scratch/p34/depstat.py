r"""Open-regime statistics for DEP-CARRY (lead, 2026-10-20): how often the crude bound Dep >= (d-1)(m-1)/2 already
gives DEP-CARRY, and the profile of the remaining S (type, height, Dep ratio, slack).  Usage: python depstat.py NS SEED MMIN MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
from depforms import forms
NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
cnt = crude = 0; rest = []
while cnt < NS:
    m = rnd.randint(MMIN, MMAX); k = rnd.randint(3, max(3, m // 3 - 2)); c0 = rnd.randint(4 * m + 1, 10 * m)
    hi = rnd.choice([2 * m, 3 * m, c0])
    G = sorted(rnd.sample(range(m + 1, min(hi, c0 + m)), k))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; d = len(gens)
    if c <= 4 * m or 3 * (d + 1) >= m or d < 3: continue
    cnt += 1; D = list(M); V, dep, BD, RA = forms(m, D, [g % m for g in gens], (-c) % m)
    Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(d))
    A = [x for x in D if all(up(x, b) not in Ds for b in range(d))]
    h = max(sum(x) for x in D)
    if 2 * dep >= (d - 1) * (m - 1): crude += 1
    else: rest.append((round(2 * dep / ((d - 1) * (m - 1)), 3), round((V + dep) / m, 3), m, d, len(A), h, gens, c))
print("open-regime S (d >= 3): %d   crude bound suffices: %d" % (cnt, crude))
rest.sort()
for z in rest[:10]: print("  Dep ratio %.3f  (V+Dep)/m %.3f  m=%d d=%d |A|=%d height=%d gens=%s c=%d" % z)
