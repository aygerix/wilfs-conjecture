# p1qb: the split W(S) = P1 + Qb (every mu), P1 = e|U cap [0,c_T)| - c_T = Qa + theta, Qb = Delta3 + (e-1)u' - h_hi.
# (analyse() copied from qab.py:) split of the mu-identity (mu <= e):  W(S) = [Delta3 + (e-1)u' - h_hi] + [(e-mu)U_mu + e U' - mu hlo_mu] + theta.
#   Qa := (e-mu) U_mu + e U' - mu hlo_mu   (pure T-structure below c(T): "T is fat below c(T)")
#   Qb := Delta3 + (e-1) u' - h_hi
import sys, heapq, collections
from itertools import combinations_with_replacement as cwr
from fractions import Fraction as F
def analyse(m, A):
    d = len(A); e = d + 1; mu = A[0]
    best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
            if cl not in best or key < best[cl]: best[cl] = key
    w = {c: best[c][0] for c in best}; hS = {c: -best[c][1] for c in best}; sg = {c: w[c] - hS[c] * m for c in w}
    tau = [None] * m; tau[0] = 0; pq = [(0, 0)]; done = [False] * m
    while pq:
        t, c = heapq.heappop(pq)
        if done[c]: continue
        done[c] = True
        for a in A:
            u = t + a; cc = u % m
            if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
    cT = max(tau) - m + 1; cU = max(sg.values()) - m + 1; cS = max(w.values()) - m + 1
    inU = lambda x: x >= sg[x % m]; inT = lambda x: x >= tau[x % m]
    Umu = sum(1 for x in range(0, cT, mu) if inU(x)); Up = sum(1 for x in range(cT) if x % mu and inU(x))
    hlo_mu = sum(1 for x in range(0, cT, mu) if not inU(x)); up = sum(1 for x in range(cT, cU) if inU(x))
    hhi = sum(1 for x in range(cT, cU) if not inU(x))
    D3 = 3 * (e - 1) * m - e * sum(hS.values()); theta = mu * (-(-cT // mu)) - cT
    gS = sum(x // m for x in w.values()); WS = e * (cS - gS) - cS
    Qa = (e - mu) * Umu + e * Up - mu * hlo_mu; Qb = D3 + (e - 1) * up - hhi
    assert WS == Qa + Qb + theta, (m, A, WS, Qa, Qb, theta)
    ray = all(not inU(x) == (x % mu == 0 and x >= 4 * mu and inT(x) and not inU(x)) for x in range(cU) if inT(x) and not inU(x))
    Ulo = sum(1 for x in range(cT) if inU(x)); P1 = e * Ulo - cT; assert P1 == Qa + theta
    hlo = sum(1 for x in range(cT) if inT(x) and not inU(x))
    return dict(P1=P1, D1hi=D3 - hhi, hlo=hlo, Ulo=Ulo, m=m, e=e, mu=mu, Qa=Qa, Qb=Qb, WS=WS, Umu=Umu, Up=Up, hlo_mu=hlo_mu, cT=cT, hhi=hhi, up=up, D3=D3)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:]))); r['A'] = list(map(int, t[15:])); rows.append(r)
print(f"{sys.argv[1]}: {len(rows)} residual S, e = {rows[0]['e']}  (W = P1 + Qb asserted via Qa + Qb + theta)")
K = ('mu','cT','Ulo','hlo','hlo_mu','hhi','up','D3','P1','Qb')
for k in ('P1', 'Qb', 'D1hi'):
    w = min(rows, key=lambda r: r[k]); print(f"  min {k} = {w[k]} at m={w['m']} A={w['A']} {dict((q, w[q]) for q in K)}")
    print(f"    {k} < 0: {sum(1 for r in rows if r[k] < 0)}")
for lo, hi in ((1, 3), (4, 6), (7, 10**9)):
    R = [r for r in rows if lo <= r['mu'] - r['e'] + 3 <= hi] if False else [r for r in rows if lo <= r['mu'] <= hi]
    if R: w = min(R, key=lambda r: r['P1']); print(f"  mu in [{lo},{hi}]: n={len(R)} min P1={w['P1']} at m={w['m']} A={w['A']}")
R = [r for r in rows if r['mu'] > r['e']]
if R: w = min(R, key=lambda r: r['P1']); print(f"  mu > e: n={len(R)} min P1={w['P1']} at m={w['m']} A={w['A']} {dict((q, w[q]) for q in K)}")
