# tophalf: falsification probe for TRUNC3 on the Q5 residual: A = e-1 random elements of (m/2, m) (plus local
# improvement toward covering), m ~ alpha*e^2.  For every exact Q5 residual hit print W_e(U) = e*l(U) - c_U, W, Delta3, mu,
# h_lo, h_hi, the A1 demand e*h_lo + h_hi, and the C>M quantities z, t, r.
import sys, random
from itertools import combinations_with_replacement as cwr
exec(open('rayU0.py').read().split('def covered')[0])
def extra(m, A):
    d = len(A); e = d + 1; best = {}
    for k in range(4):
        for c in cwr(A, k):
            s = sum(c); cl = s % m
            if cl not in best or (k * m + s, -k) < best[cl]: best[cl] = (k * m + s, -k)
    sg = {cl: best[cl][0] + best[cl][1] * m for cl in best}
    cU = max(sg.values()) - m + 1; lU = sum(1 for z in range(cU) if z >= sg[z % m])
    z = sum(1 for s in range(m) if sg[s] < m); t = sum(1 for s in range(m) if sg[s] >= 2 * m); r = max(sg.values()) - 2 * m
    return dict(WeU=e * lU - cU, z=z, t=t, r=r, cU=cU)
rng = random.Random(int(sys.argv[3])); found = 0; stat = __import__('collections').Counter()
for e in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    worst = None
    for alpha in (0.4, 0.6, 0.8, 1.0, 1.3, 1.7):
        m = int(alpha * e * e)
        for trial in range(int(sys.argv[4])):
            A = sorted(rng.sample(range(m // 2 + 1, m), e - 1))
            # local search: maximize coverage of Z/m by <= 3-sums
            def cov(A):
                S = {0}
                for _ in range(3): S = S | {(x + a) % m for x in S for a in A}
                return len(S)
            c0 = cov(A)
            for it in range(300):
                if c0 == m: break
                i = rng.randrange(e - 1); x = rng.randrange(m // 2 + 1, m)
                if x in A: continue
                B = sorted(A[:i] + A[i + 1:] + [x]); c1 = cov(B)
                if c1 >= c0: A, c0 = B, c1
            if c0 < m: stat['nocover', e] += 1; continue
            r = evalS(m, A)
            if not r: stat['notQ5', e] += 1; continue
            if r['h'] == 0: stat['U=T', e] += 1; continue
            x = extra(m, A); found += 1
            row = (x['WeU'], e, m, A, r, x)
            if worst is None or row[0] < worst[0]: worst = row
            if x['WeU'] < 0: print(f"TRUNC3 FAILS e={e} m={m} A={A} WeU={x['WeU']} W={r['W']} D3={r['D3']} mu={r['mu']} h={r['h']} z={x['z']} t={x['t']} r={x['r']}", flush=True)
            if r['W'] < 0: print('WILF FAILS !!!', e, m, A, flush=True)
    if worst: print(f"e={e}: worst W_e(U)={worst[0]} at m={worst[2]} A={worst[3]} (W={worst[4]['W']} D3={worst[4]['D3']} h={worst[4]['h']} mu={worst[4]['mu']})", flush=True)
print('residual Q5 hits:', found); print(sorted(stat.items()))
