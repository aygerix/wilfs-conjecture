# LOW constructions (lead, 2026-10-20): S = <m, k m + B> with B u (B+B) covering [1, m-1]; report q, rho, Lambda, sumK, W, T1 slack.
import sys
sys.path.insert(0, '.')
from lowfam import analyze
for (m, B) in [(9, [1, 3, 4]), (13, [1, 2, 4, 9]), (16, [1, 3, 7, 4, 2]), (21, [1, 3, 4, 7, 9, 10]), (19, [1, 2, 4, 7, 11, 14])]:
    for k in [1, 2, 3, 4, 6, 10]:
        gens = [m] + [k * m + b for b in B]
        r = analyze(m, gens)
        if r is None: continue
        low = r['rho'] + r['Lam'] < m - r['e']
        print("m=%d B=%s k=%d: e=%d q=%d rho=%d Lam=%d sumK=%d W=%d T1slack=%d LOW=%s" % (m, B, k, r['e'], r['q'], r['rho'], r['Lam'], r['sumK'], r['W'], m - r['e'] - r['sumK'], low))
