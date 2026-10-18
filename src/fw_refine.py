"""Sharper bounds from the exact line identity m W = C(m,2) + sum_l sigma_l (src/fw.py), on FW failures.
  FW   : m(P - d tau) - (m-1)E(Z)                                   [kseth p:6, all d]
  FWx  : C(m,2) + sum_deep (m + C(L,2)) - sum_final R_j(L)            [exact residues on final lines]
  FW2  : d m + (m-1)(P + sum_j (L_j - 1)) - m(sum_Z |z| + d tau)        [all lines' R bounded together]
  orders: grlex, lex and lex over every generator permutation (best taken)."""
import sys, itertools
from math import comb
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def bounds(s, order='grlex', perm=None):
    m, c = s.m, s.c
    Pp, best = factorizations_down_set(s, order, perm)
    d = len(Pp); T = set(best.values()); lam = {x: w for w, x in best.items()}
    M = max(lam.values()); W = (d + 1) * (c - s.g) - c
    Z = [x for x in T if lam[x] >= c]; tau = len(Z)
    nl = 0; fwx = comb(m, 2); fwy = comb(m, 2)
    for j in range(d):
        a = Pp[j]
        for x in T:
            if tuple(x[i] + (i == j) for i in range(d)) in T: continue
            L = x[j] + 1; nl += 1
            R = sum((r * a) % m for r in range(L))
            if lam[x] >= c:
                fwx -= R; u = M - lam[x]
                fwy += sum(u - (u + r * a) % m for r in range(L))
            else: fwx += m + comb(L, 2); fwy += m + comb(L, 2)
    E = sum(sum(z) for z in Z) - sum(max(z[j] for z in Z) for j in range(d))
    Lj = [max(x[j] for x in T) + 1 for j in range(d)]
    fw = m * (nl - d * tau) - (m - 1) * E
    fw2 = d * m + (m - 1) * (nl + sum(l - 1 for l in Lj)) - m * (sum(sum(z) for z in Z) + d * tau)
    assert m * W >= max(fw, fwx, fw2, fwy) and fwy >= fwx, (s.P, m * W, fw, fwx, fw2, fwy)
    return dict(mW=m * W, FW=fw, FWx=fwx, FW2=fw2, FWy=fwy)
def best_over_orders(s):
    d = len(s.P) - 1
    res = {'grlex': bounds(s, 'grlex'), 'lex': bounds(s, 'lex')}
    for perm in itertools.permutations(range(d)):
        res['lex' + ''.join(map(str, perm))] = bounds(s, 'lex', perm)
    return res
if __name__ == '__main__':
    import re
    for line in open(sys.argv[1]):
        mm = re.match(r'\s*\(\[([\d, ]+)\]', line)
        if not mm: continue
        gens = [int(v) for v in mm.group(1).split(',')]
        s = NS.from_generators(gens)
        res = best_over_orders(s)
        g = res['grlex']
        bfw = max(r['FW'] for r in res.values()); bfwx = max(r['FWx'] for r in res.values()); bfw2 = max(r['FW2'] for r in res.values())
        print(gens, 'mW', g['mW'], '| grlex FW', g['FW'], 'FWx', g['FWx'], 'FW2', g['FW2'], '| best-order FW', bfw, 'FWx', bfwx, 'FW2', bfw2)
