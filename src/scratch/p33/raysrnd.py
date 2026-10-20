"""Universal DB certificate on random S and on stored hard examples (rays.py). Usage: python raysrnd.py NS SEED"""
import sys, random
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from rays import analyse
NS, SEED = int(sys.argv[1]), int(sys.argv[2]); random.seed(SEED)
hard = [(14, [22, 23], 56), (798, [1205, 1206, 1209, 1218, 1237, 1276, 1329], 3192), (30, [44, 48, 49], 118),
        (16, [27, 28, 31], 78), (9, [14, 15, 17], 26), (13, [20, 21, 23, 25], 38)]
for m, G, c in hard:
    R = analyse(m, G, c)
    if R in (None, 'notdown'): print("skip", m, G, c, R); continue
    print("m=%d G=%s c=%d: E=%d r=%d rj=%s cert=%.2f W=%d P=%.2f R=%d certR=%.2f" % (m, G, c, R['E'], R['r'], R['rj'], float(R['cert']), R['W'], float(R['P']), R['R'], float(R['certR'])))
cnt = 0; fails = 0; ex = []; p0 = 0; failR = 0; exR = []
while cnt < NS:
    n = random.randint(1, 5); m = random.randint(5, 50); c = random.randint(2 * m + 1, 8 * m)
    lo = m + 1; G = sorted(random.sample(range(lo, c), min(n, c - lo)))
    if any(g % m == 0 for g in G): continue
    R = analyse(m, G, c)
    if R in (None, 'notdown'): continue
    cnt += 1
    if R['P'] == 0 and n >= 2:
        p0 += 1
        if R['certR'] < -1:
            failR += 1
            if len(exR) < 8: exR.append((m, G, c, R['E'], R['r'], R['R'], float(R['certR']), R['W']))
    if R['cert'] < -1:
        fails += 1
        if len(ex) < 8: ex.append((m, G, c, R['E'], R['r'], R['rj'], float(R['cert']), R['W'], float(R['P']), float(R['L'])))
print("random S %d: universal DB certificate fails %d; P~=0 cases (n>=2) %d, R-certificate fails %d" % (cnt, fails, p0, failR))
for e in exR: print("   Rfail m=%d G=%s c=%d E=%d r=%d R=%d certR=%.2f W=%d" % e)
for e in ex: print("   m=%d G=%s c=%d E=%d r=%d rj=%s cert=%.2f W=%d P=%.2f L=%.2f" % e)
