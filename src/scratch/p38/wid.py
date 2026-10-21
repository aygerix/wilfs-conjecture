# wid: exact identity on Q5:  W(S) = Delta3 + (e-1) u' + e |U cap [0,c_T)| - c_T - h_hi.
# Split  P1 := e |U cap [0,c_T)| - c_T   and   P2 := Delta3 + (e-1) u' - h_hi.
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
    cT = max(tau) - m + 1; cS = max(w.values()) - m + 1; cU = max(sg.values()) - m + 1
    inU = lambda x: x >= sg[x % m]
    Ulo = sum(1 for x in range(cT) if inU(x)); up = sum(1 for x in range(cT, cU) if inU(x))
    NE = [tau[c] for c in range(m) if sg[c] > tau[c]]; hhi = sum(1 for t in NE if t >= cT)
    D3 = 3 * (e - 1) * m - e * sum(hS.values())
    gS = sum(x // m for x in w.values()); WS = e * (cS - gS) - cS
    P1 = e * Ulo - cT; P2 = D3 + (e - 1) * up - hhi
    assert WS == P1 + P2, (m, A, WS, P1, P2)
    return dict(m=m, e=e, mu=mu, P1=P1, P2=P2, WS=WS, cT=cT, Ulo=Ulo, hhi=hhi, up=up, D3=D3, h=len(NE))
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:]))); r['A'] = list(map(int, t[15:])); rows.append(r)
print(f"{sys.argv[1]}: {len(rows)} S, e = {rows[0]['e']}  (identity asserted on every S)")
for k in ('P1', 'P2', 'WS'):
    w = min(rows, key=lambda r: r[k]); print(f"  min {k} = {w[k]} at m={w['m']} A={w['A']} {dict((q, w[q]) for q in ('mu','cT','Ulo','hhi','up','D3','h','P1','P2'))}")
print('  P1 < 0 count:', sum(1 for r in rows if r['P1'] < 0), ' P2 < 0 count:', sum(1 for r in rows if r['P2'] < 0))
w = min(rows, key=lambda r: F(r['e'] * r['Ulo'], r['cT'])); print(f"  min e|U_lo|/c_T = {float(F(w['e'] * w['Ulo'], w['cT'])):.3f} at m={w['m']} A={w['A']} cT={w['cT']} Ulo={w['Ulo']}")
