r"""Simulated annealing over genuine S = <m, m K_b + s_b> (d generators besides m) minimizing RT, or RT/q, or lead
(see h3rnd.py), subject to e = d+1 and c >= 4m+1 (lead, 2026-10-20).  Moves: change one residue s_b or one level K_b.
usage: /usr/bin/python3 rtanneal.py d m KMAX STEPS SEED [RT|RTq|lead|W]"""
import sys, random, math
sys.path.insert(0, '.')
from h3rnd import analyse
d, m, KM, ST, seed = map(int, sys.argv[1:6]); obj = sys.argv[6] if len(sys.argv) > 6 else 'RT'
rng = random.Random(seed)
def val(R):
    if R['e'] != d + 1 or R['c'] < 4 * m + 1 or R['RT'] is None: return None
    return {'RT': R['RT'], 'RTq': R['RT'] / R['q'], 'lead': R['lead'], 'W': R['W']}[obj]
while True:
    s = rng.sample(range(1, m), d); K = [rng.randint(1, KM) for _ in range(d)]
    R = analyse([m] + [m * k + x for k, x in zip(K, s)]); v = val(R)
    if v is not None: break
best = (v, R); T0 = max(1.0, abs(v) / 10)
for it in range(ST):
    T = T0 * (1 - it / ST) + 1e-3
    s2, K2 = s[:], K[:]
    b = rng.randrange(d)
    if rng.random() < 0.7:
        x = rng.randrange(1, m)
        if x in s2: continue
        s2[b] = x
    else: K2[b] = rng.randint(1, KM)
    R2 = analyse([m] + [m * k + x for k, x in zip(K2, s2)]); v2 = val(R2)
    if v2 is None: continue
    if v2 <= v or rng.random() < math.exp(-(v2 - v) / T):
        s, K, v, R = s2, K2, v2, R2
        if v < best[0] - 1e-9: best = (v, R)
print("d=%d m=%d obj=%s best=%.3f %s" % (d, m, obj, best[0], best[1]), flush=True)
