"""wm_suff check on one semigroup (grlex tile).  usage: python wm_suff_one.py m g1 g2 ..."""
import sys
sys.path.insert(0, '../nowrap')
from pmin_tile import apery, minimal_gens, tile
from wm_suff import check
m = int(sys.argv[1]); n, ap = minimal_gens(m, list(map(int, sys.argv[2:]))); d = len(n); P = [g % m for g in n]
D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values())
for t in check(m, P, D): print("theta %d |V_th| %d  H1'-slack %d  Out-|V| %d  Ex-|V| %d" % (t[3], t[4], t[0], t[1], t[2]))
