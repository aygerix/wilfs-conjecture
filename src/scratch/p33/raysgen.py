"""General one-step DB certificate on random S at all depths (rays.py): certG = W with r replaced by
max(R_gen, [r>=1]), R_gen = sum_{z in boundary}(deg^-_{interior}(z) - 1) <= r (proved). Usage: python raysgen.py NS SEED QMIN"""
import sys, random
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from rays import analyse
NS, SEED, QMIN = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); random.seed(SEED)
cnt = 0; fails = 0; ex = []; r0 = 0; minc = None
while cnt < NS:
    n = random.randint(2, 6); m = random.randint(5, 60); c = random.randint((QMIN - 1) * m + 1, 10 * m)
    hi = random.choice([2 * m, 3 * m, c])
    if hi - m - 1 < n: continue
    G = sorted(random.sample(range(m + 1, min(hi, c)), n)) if min(hi, c) - m - 1 >= n else None
    if G is None or any(g % m == 0 for g in G): continue
    R = analyse(m, G, c)
    if R in (None, 'notdown'): continue
    cnt += 1
    if R['r'] == 0: r0 += 1
    v = float(R['certG'])
    if minc is None or v < minc[0]: minc = (v, m, G, c, R['r'], R['Rgen'], R['W'], float(R['P']))
    if R['certG'] < -1:
        fails += 1
        if len(ex) < 10: ex.append((m, G, c, R['E'], R['r'], R['Rgen'], v, R['W'], float(R['P']), float(R['L'])))
print("S %d (r = 0: %d), q >= %d: general certificate fails %d; min %s" % (cnt, r0, QMIN, fails, minc))
for e in ex: print("   FAIL m=%d G=%s c=%d E=%d r=%d Rgen=%d certG=%.2f W=%d P=%.2f L=%.2f" % e)
