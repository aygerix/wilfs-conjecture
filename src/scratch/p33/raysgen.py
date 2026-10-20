"""General one-step DB certificate on random S at all depths (rays.py): certG = W with r replaced by
max(R_gen, [r>=1]), R_gen = sum_{z in boundary}(deg^-_{interior}(z) - 1) <= r (proved). Usage: python raysgen.py NS SEED QMIN"""
import sys, random
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from rays import analyse
NS, SEED, QMIN = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); random.seed(SEED)
z0 = 0; z0f = 0; z0ex = []; cnt = 0; fails = 0; ex = []; r0 = 0; minc = None; cf = 0; cex = []; ppos = 0; cnp = 0; npex = []; gf = [0, 0, 0, 0]; gex = [[], [], [], []]
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
    if R['P'] > 0: ppos += 1
    if R['r'] == 0:
        z0 += 1
        if R['crudeG'] < 0:
            z0f += 1
            if len(z0ex) < 6: z0ex.append((m, G, c, R['E'], float(R['P']), float(R['crudeG']), R['W']))
    if R['crudeG'] < 0 and R['r'] >= 1:
        cf += 1
        if len(cex) < 8: cex.append((m, G, c, R['E'], R['r'], R['Rgen'], float(R['crudeG']), float(R['P']), R['kq'], R['W']))
    if R['r'] >= 1 and n >= 2:
        for j in range(4):
            if not R['gsteps'][j]:
                gf[j] += 1
                if len(gex[j]) < 3: gex[j].append((m, G, c, R['r'], R['Rgen'], R['kq']))
    if R['crudeNP'] < 0 and R['r'] >= 1:
        cnp += 1
        if len(npex) < 8: npex.append((m, G, c, R['r'], R['Rgen'], float(R['crudeNP']), float(R['P']), R['kq'], R['nBl'], R['nsink']))
    if R['certG'] < -1:
        fails += 1
        if len(ex) < 10: ex.append((m, G, c, R['E'], R['r'], R['Rgen'], v, R['W'], float(R['P']), float(R['L'])))
print("S %d (r = 0: %d), q >= %d: general certificate fails %d; min %s" % (cnt, r0, QMIN, fails, minc))
for e in ex: print("   FAIL m=%d G=%s c=%d E=%d r=%d Rgen=%d certG=%.2f W=%d P=%.2f L=%.2f" % e)
print("P~>0: %d; crude general inequality (r>=1) fails %d" % (ppos, cf))
for e in cex: print("   CRUDE m=%d G=%s c=%d E=%d r=%d Rgen=%d crudeG=%.2f P=%.2f k-q=%d W=%d" % e)
print("crude WITHOUT P~ (r>=1) fails %d" % cnp)
for e in npex: print("   NOP m=%d G=%s c=%d r=%d Rgen=%d crudeNP=%.2f P=%.2f k-q=%d |B<|=%d sinks=%d" % e)
print("generalized P0 step failures (r>=1, n>=2): G1 %d, G2 %d, G3 %d, Ysupp<=Rg %d" % tuple(gf))
for j in range(4):
    for e in gex[j]: print("   step%d fails: m=%d G=%s c=%d r=%d Rgen=%d k-q=%d" % ((j + 1,) + e))
print("r = 0 cases %d: crude (sum_Y(|y|-1) <= P~) fails %d" % (z0, z0f))
for e in z0ex: print("   R0 m=%d G=%s c=%d E=%d P=%.2f crude=%.2f W=%d" % e)
