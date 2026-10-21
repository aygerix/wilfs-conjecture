r"""Annealing over genuine S = <m, m K_b + s_b> minimizing RT2, UA2, RT2/W or UA2/W (lead, 2026-10-21).
Domain: e = d+1 >= 4, 3e < m, c >= 4m+1, Apery height >= HMIN.  Levels K_b in [1, KMAX] (unbalanced allowed); moves change
one residue or one level.  Prints the best S with all four relaxations and W.
usage: /usr/bin/python3 rt2anneal.py d m KMAX STEPS SEED OBJ HMIN"""
import sys, random, math
sys.path.insert(0, '.')
from rt2lib import data, relax
d, m, KM, ST, seed = map(int, sys.argv[1:6]); obj = sys.argv[6]; hmin = int(sys.argv[7])
rng = random.Random(seed); key = {'RT2': 'RT2', 'UA2': 'UA2', 'RT2W': 'RT2', 'UA2W': 'UA2'}[obj]
def ev(s, K):
    D = data([m] + [m * k + x for k, x in zip(K, s)])
    if D['e'] != d + 1 or D['c'] < 4 * m + 1 or D['h'] < hmin or 3 * D['e'] >= m: return None, None
    R = relax(D, (key,)); v = R[key]
    if v is None: return None, None
    return (v / D['W'] if obj.endswith('W') else v), (D, R)
while True:
    s = rng.sample(range(1, m), d); K = [rng.randint(1, KM) for _ in range(d)]
    v, info = ev(s, K)
    if v is not None: break
best = (v, s[:], K[:]); T0 = max(0.05, abs(v) / 10)
for it in range(ST):
    T = T0 * (1 - it / ST) + 1e-4
    s2, K2 = s[:], K[:]; b = rng.randrange(d)
    if rng.random() < 0.65:
        x = rng.randrange(1, m)
        if x in s2: continue
        s2[b] = x
    else: K2[b] = rng.randint(1, KM)
    v2, info2 = ev(s2, K2)
    if v2 is None: continue
    if v2 <= v or rng.random() < math.exp(-(v2 - v) / T):
        s, K, v = s2, K2, v2
        if v < best[0] - 1e-12: best = (v, s[:], K[:])
G = [m] + [m * k + x for k, x in zip(best[2], best[1])]
D = data(G); R = relax(D)
print("d=%d m=%d obj=%s best=%.4f | m=%d e=%d c=%d q=%d rho=%d h=%d W=%d RT=%.3f RT2=%.3f UA=%.3f UA2=%.3f RT2/W=%.4f UA2/W=%.4f G=%s" % (
    d, m, obj, best[0], D['m'], D['e'], D['c'], D['q'], D['rho'], D['h'], D['W'], R['RT'], R['RT2'], R['UA'], R['UA2'],
    R['RT2'] / D['W'], R['UA2'] / D['W'], sorted(G)), flush=True)
