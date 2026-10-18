# Per-direction decomposition of TOP'':  TOP'' <=> sum_a B_a <= m(m-1)/2, where
#   B_a := sum_{u in X} pi(u) n_a(u) - sum_{j in Pi^c} j   (n = grlex-least factorization, Pi^c = left positions in last layer)
import sys, itertools
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS, all_by_genus
from cl import factorizations_down_set
def Bvec(s):
    m, c = s.m, s.c; d = s.e - 1
    ap = sorted(s.apery()); X = [u for u in ap if c <= u < c + m]
    _, best = factorizations_down_set(s, 'grlex')
    Pi = set(u - c + 1 for u in X); spc = sum(j for j in range(1, m + 1) if j not in Pi)
    B = [sum((u - c + 1)*best[u][a] for u in X) - spc for a in range(d)]
    return m, d, B
if __name__ == '__main__':
    G = int(sys.argv[1]); worst = {}
    for g, s in all_by_genus(G):
        if g == 0 or s.e < 3: continue
        m, d, B = Bvec(s); assert sum(B) <= m*(m - 1)//2
        r = max(B)/(m - 1); key = d
        if key not in worst or r > worst[key][0]: worst[key] = (r, s.P, B, m)
    for d in sorted(worst): print('d', d, 'max_a B_a/(m-1) =', round(worst[d][0], 3), worst[d][1:])
