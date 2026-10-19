"""Print the WRAP-MAX payment split for one semigroup (grlex tile), every phase with F nonempty.
usage: python wm_one.py m g1 g2 ..."""
import sys
sys.path.insert(0, '../nowrap')
from pmin_tile import apery, minimal_gens, tile
from wm_pay import instances
m = int(sys.argv[1]); gens = list(map(int, sys.argv[2:]))
n, ap = minimal_gens(m, gens); d = len(n)
D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values())
res = instances(m, n, D)
if res is None: print("not WRAP-MAX"); sys.exit()
for R in res:
    print("rho0", R['r0'], "S", R['S'], "S/m", round(R['S']/m, 3), "|F|", len(R['F']), "beta_N", R['beta'], "tau+", R['tauplus'], "Lam/m", round(R['Lam']/m, 3), "A_W", R['AW'], "n_W", R['nW'], "F", R['F'], "r(F)", R['rF'])
