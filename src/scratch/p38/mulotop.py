# mulotop: top MU-LO ratios per e with shape data. (from c1test.py) C1 := Delta3 >= (c_T - 3mu)^+ + h_hi (implies MU-LO for mu <= e); also CU := Delta3 >= c_U - 3mu.
# (analyse() from p1qb.py) p1qb: the split W(S) = P1 + Qb (every mu), P1 = e|U cap [0,c_T)| - c_T = Qa + theta, Qb = Delta3 + (e-1)u' - h_hi.
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
    cU_ = cU
    return dict(cU=cU_, P1=P1, D1hi=D3 - hhi, hlo=hlo, Ulo=Ulo, m=m, e=e, mu=mu, Qa=Qa, Qb=Qb, WS=WS, Umu=Umu, Up=Up, hlo_mu=hlo_mu, cT=cT, hhi=hhi, up=up, D3=D3)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:]))); r['A'] = list(map(int, t[15:]))
            if r['mu'] > r['e']: continue
            r['ML'] = (r['mu'] * r['hlo_mu'] + r['hhi']) / r['D3']; rows.append(r)
rows.sort(key=lambda r: -r['ML'])
print(f"{sys.argv[1]}: e = {rows[0]['e']}, top MU-LO ratios (mu <= e):")
for r in rows[:8]:
    print(f"  {r['ML']:.3f} m={r['m']} A={r['A']} mu={r['mu']} cT={r['cT']} cU={r['cU']} hlo_mu={r['hlo_mu']} hhi={r['hhi']} D3={r['D3']}")
