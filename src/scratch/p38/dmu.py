# dmu: for mu <= e, W(S) >= Delta3 - mu*h_lo - h_hi + (e-1)u' + (e-mu)|U cap [0,c_T)|  (no induction; mu*l(T) >= c(T)).
# Report max (mu*h_lo + h_hi)/D3 and min D3/(mu*h) over residual S with mu <= e, by mu.
import sys, collections
from fractions import Fraction as F
best = {}; bestA = {}; cnt = collections.Counter(); bym = {}
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            v = list(map(int, t[1:15])); A = list(map(int, t[15:])); m, e, D3, h, hlo, hhi = v[0], v[1], v[2], v[4], v[5], v[6]
            mu = A[0]
            if mu > e: cnt['mu>e'] += 1; continue
            cnt['mu<=e'] += 1
            r = F(mu * hlo + hhi, D3); q = F(D3, mu * h)
            if r > best.get('A1mu', (F(-1),))[0]: best['A1mu'] = (r, m, A, D3, h, hlo)
            if q < best.get('Dmu', (F(10**9),))[0]: best['Dmu'] = (q, m, A, D3, h, hlo)
            bym[mu] = min(bym.get(mu, F(10**9)), q)
print(sys.argv[1], dict(cnt))
for k, (r, m, A, D3, h, hlo) in best.items(): print(f"  {k}: {float(r):.4f} at m={m} A={A} D3={D3} h={h} hlo={hlo}")
print('  min D3/(mu h) by mu:', {k: round(float(v), 3) for k, v in sorted(bym.items())})
