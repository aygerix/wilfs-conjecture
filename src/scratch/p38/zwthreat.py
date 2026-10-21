# zwthreat: falsification probe for ZW (Delta3 + e z >= c_U) on the residual: A = {mu} u B, B random-ish in (m/2, m)
# with 4mu + m = b + b' forced (so 4mu is NE2 when 4mu is not in 3A'), m ~ alpha e^3; local search for covering of Z/m.
# Prints ZW slack, exact Wilf, and the dropped term e(r+1-t).
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
    cU = max(sg.values()) - m + 1; z = sum(1 for s in range(m) if sg[s] < m); t = sum(1 for s in range(m) if sg[s] >= 2 * m); r = max(sg.values()) - 2 * m
    return dict(cU=cU, z=z, t=t, r=r)
def cov(m, A):
    S = {0}
    for _ in range(3): S = S | {(x + a) % m for x in S for a in A}
    return len(S)
rng = random.Random(int(sys.argv[3])); stat = __import__('collections').Counter()
for e in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    worst = None
    for alpha in (0.03, 0.05, 0.08, 0.12):
        m = max(4 * e, int(alpha * e ** 3))
        for trial in range(int(sys.argv[4])):
            mu = rng.randrange(2, max(3, m // 8))
            # choose b, b' in (m/2, m) with b + b' = m + 4mu
            tgt = m + 4 * mu; lo = max(m // 2 + 1, tgt - (m - 1)); hi = min(m - 1, tgt - (m // 2 + 1))
            if lo > hi: continue
            b1 = rng.randrange(lo, hi + 1); b2 = tgt - b1
            B = {b1, b2}
            while len(B) < e - 2: B.add(rng.randrange(m // 2 + 1, m))
            A = sorted({mu} | B)
            if len(A) != e - 1: continue
            c0 = cov(m, A)
            for it in range(400):
                if c0 == m: break
                i = rng.randrange(len(A)); x = rng.randrange(m // 2 + 1, m)
                if A[i] in (mu, b1, b2) or x in A: continue
                C = sorted(A[:i] + A[i + 1:] + [x]); c1 = cov(m, C)
                if c1 >= c0: A, c0 = C, c1
            if c0 < m: stat['nocover'] += 1; continue
            r = evalS(m, A)
            if not r: stat['notQ5'] += 1; continue
            if r['h'] == 0: stat['U=T'] += 1; continue
            stat['residual'] += 1; x = extra(m, A)
            zw = r['D3'] + e * x['z'] - x['cU']
            row = (zw, m, A, r, x)
            if worst is None or zw < worst[0]: worst = row
            if zw < 0: print(f"ZW FAILS e={e} m={m} A={A} slack={zw} D3={r['D3']} z={x['z']} cU={x['cU']} W={r['W']} dropped e(r+1-t)={e * (x['r'] + 1 - x['t'])} mu={mu}", flush=True)
            if r['W'] < 0: print('WILF FAILS !!!', e, m, A, flush=True)
    if worst: print(f"e={e}: min ZW slack {worst[0]} at m={worst[1]} A={worst[2]} (D3={worst[3]['D3']} z={worst[4]['z']} cU={worst[4]['cU']} W={worst[3]['W']})", flush=True)
print(sorted(stat.items()))
