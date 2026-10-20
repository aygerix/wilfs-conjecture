"""Who pays the top loss Lam on negative-Eliahou Delgado truncations <mu, g, g+1> u [p mu, inf) (E < 0 only):
ray identity E = rho r/m + G + Ptil - Lam (rays.py). Reports, over E<0 cases: Lam/(G+Ptil) range, the crude
sufficient condition r*(|M_<| - 1) >= sum_Y (|y| - 1), and min of [r (k-q) + G + Ptil + rho r/m - Lam] = W.
Usage: python raysdelg.py PMAX MUMAX"""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from rays import analyse
PMAX, MUMAX = int(sys.argv[1]), int(sys.argv[2])
rows = []
for p in range(4, PMAX + 1):
    for mu in range(3, MUMAX + 1):
        for g in range(mu + 1, 2 * mu - 1):
            c = p * mu
            # quick Apery for E sign
            res = analyse(mu, [g, g + 1], c)
            if res is None or res == 'notdown' or res['E'] >= 0: continue
            rows.append((p, mu, g, res))
print("E<0 cases:", len(rows))
crude_ok = 0; worst = None
for p, mu, g, R in rows:
    # recompute |M_<| - 1 and sum_Y(|y|-1) cheaply from definitions via kq bound is not exact; use k-q >= |M_<|-1
    tot = R['r'] * R['kq'] + R['G'] + R['P'] - R['L']
    frac = float(R['L'] / (R['G'] + R['P'])) if R['G'] + R['P'] > 0 else 99
    if worst is None or frac > worst[0]: worst = (frac, p, mu, g, float(R['L']), float(R['G']), float(R['P']), R['r'], R['kq'], R['E'])
print("max Lam/(G+Ptil) = %.3f at p=%d mu=%d g=%d (Lam %.2f G %.2f Ptil %.2f r %d k-q %d E %d)" % worst)
import collections
pt = sum(1 for _, _, _, R in rows if R['P'] > 0)
print("E<0 cases with Ptil > 0: %d of %d" % (pt, len(rows)))
uR = [(p, mu, g, R) for p, mu, g, R in rows if R['P'] == 0 and R['certR'] < -1]
print("P~=0 E<0 cases: %d; R-certificate (r := max(1, sum_Y(|supp y|-1))) fails on %d" % (sum(1 for _, _, _, R in rows if R['P'] == 0), len(uR)))
for p, mu, g, R in uR[:6]: print("   Rfail p=%d mu=%d g=%d r=%d R=%d certR=%.2f W=%d" % (p, mu, g, R['r'], R['R'], float(R['certR']), R['W']))
unc = [(p, mu, g, R) for p, mu, g, R in rows if R['cert'] < -1]
print("universal DB certificate (r replaced by max_j |M_j - Delta_j| - |M|) fails on %d of %d E<0 cases" % (len(unc), len(rows)))
for p, mu, g, R in unc[:8]: print("   p=%d mu=%d g=%d r=%d rj=%s cert=%.2f W=%d" % (p, mu, g, R['r'], R['rj'], float(R['cert']), R['W']))
