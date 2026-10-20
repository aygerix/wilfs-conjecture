"""Targeted search for S with P~ = 0 (no Apery ray ends below c), generators at several heights.
For random Gamma (n = 2..6, gamma in (m, HM*m)), scan c and keep S with P~ = 0; test
  r >= R = sum_{top y}(|supp y| - 1)  (proved) and the R-certificate W(r := max(1,R)) >= 0 (conjecture RC0).
Usage: python raysp0.py NS SEED HM"""
import sys, random
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from rays import analyse
NS, SEED, HM = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]); CMIN = int(sys.argv[4]) if len(sys.argv) > 4 else 0; random.seed(SEED)
hits = 0; fails = 0; ex = []; cfail = 0; cex = []; regular = 0; tried = 0; Eneg = 0; minslack = None
while hits < NS:
    n = random.randint(2, 6); m = random.randint(6, 80)
    if int(HM * m) - m - 1 < n: continue
    G = sorted(random.sample(range(m + 1, int(HM * m)), n))
    if any(g % m == 0 for g in G): continue
    for c in range(max(G[-1] + 1, CMIN * m + 1), 14 * m):
        tried += 1
        # cheap necessary condition for P~ = 0: some gap of length gamma_max - m below c in the values of <Gamma>
        R = analyse(m, G, c)
        if R in (None, 'notdown') or R['P'] != 0: continue
        hits += 1
        h_reg = max(G) * 1.0 / min(G)
        if R['E'] < 0: Eneg += 1
        sl = float(R['certR'])
        if minslack is None or sl < minslack[0]: minslack = (sl, m, G, c, R['E'], R['r'], R['R'], R['W'])
        if R['crude'] is not None and R['crude'] < 0:
            cfail += 1
            if len(cex) < 6: cex.append((m, G, c, R['E'], R['r'], R['R'], R['kq'], R['crude'], R['W']))
        if R['certR'] < -1:
            fails += 1
            if len(ex) < 10: ex.append((m, G, c, R['E'], R['r'], R['R'], sl, R['W']))
        if hits >= NS: break
print("tried %d (m,G,c); P~=0 S: %d (E<0: %d); R-certificate fails %d; min certR %s" % (tried, hits, Eneg, fails, minslack))
for e in ex: print("   FAIL m=%d G=%s c=%d E=%d r=%d R=%d certR=%.2f W=%d" % e)
print("crude inequality sum_Y(|y|-1) <= max(1,R)(k-q) fails %d" % cfail)
for e in cex: print("   CRUDE m=%d G=%s c=%d E=%d r=%d R=%d k-q=%d crude=%d W=%d" % e)
