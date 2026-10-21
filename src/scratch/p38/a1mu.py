# a1mu: for mu <= e,  W(S) >= Delta3 - mu*hlo_mu - h_hi  (+ nonneg terms), where hlo_mu = #{tau in T\U, tau < c(T), mu | tau}.
# (from W(S) = Delta3 - e h + (e-1) dc + e l(T) - c(T) and c(T) <= mu * ceil(c(T)/mu)).  Report max ratio, and check
# the exact lower bound against the true W(S).
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
    cT = max(tau) - m + 1; cS = max(w.values()) - m + 1
    NE = [tau[c] for c in range(m) if sg[c] > tau[c]]
    hlo_mu = sum(1 for t in NE if t < cT and t % mu == 0); R0 = sum(1 for t in NE if t % mu == 0); hlo = sum(1 for t in NE if t < cT); hhi = len(NE) - hlo
    D3 = 3 * (e - 1) * m - e * sum(hS.values())
    gS = sum(x // m for x in w.values()); WS = e * (cS - gS) - cS
    lb = D3 - mu * hlo_mu - hhi
    Uset = [c for c in range(m)]
    inU = lambda x: x >= sg[x % m]
    Umu = sum(1 for x in range(0, cT, mu) if inU(x)); Up = sum(1 for x in range(cT) if x % mu and inU(x))
    up = sum(1 for x in range(cT, max(sg.values()) - m + 1) if inU(x))
    full = D3 - mu * hlo_mu - hhi + (e - 1) * up + (e - mu) * Umu + e * Up
    if mu <= e: assert WS >= full >= lb, (m, A, WS, full, lb)
    return dict(m=m, e=e, mu=mu, D3=D3, h=len(NE), hlo=hlo, hlo_mu=hlo_mu, hhi=hhi, WS=WS, lb=lb, Up=Up, Umu=Umu, up=up, cT=cT, full=full, R0=R0)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:]))); r['A'] = list(map(int, t[15:])); rows.append(r)
R = [r for r in rows if r['mu'] <= r['e']]
print(f"{sys.argv[1]}: {len(rows)} S (mu <= e: {len(R)}), e = {rows[0]['e']}")
w = max(R, key=lambda r: F(r['mu'] * r['hlo_mu'] + r['hhi'], r['D3']))
print(f"  max (mu hlo_mu + hhi)/D3 = {float(F(w['mu'] * w['hlo_mu'] + w['hhi'], w['D3'])):.4f} at m={w['m']} A={w['A']} {dict((k, w[k]) for k in ('mu','D3','h','hlo','hlo_mu','hhi','WS','lb'))}")
w = min(R, key=lambda r: r['lb']); print(f"  min lower bound D3 - mu hlo_mu - hhi = {w['lb']} at m={w['m']} A={w['A']} (W(S) = {w['WS']})")
w = min(R, key=lambda r: r['e'] * r['Up'] - r['mu'] * r['hlo_mu']); print(f"  min e*U' - mu*hlo_mu = {w['e'] * w['Up'] - w['mu'] * w['hlo_mu']} at m={w['m']} A={w['A']} Up={w['Up']} hlo_mu={w['hlo_mu']} cT={w['cT']}")
w = min(R, key=lambda r: r['Up'] - r['hlo_mu']); print(f"  min U' - hlo_mu = {w['Up'] - w['hlo_mu']} at m={w['m']} A={w['A']} Up={w['Up']} hlo_mu={w['hlo_mu']} cT={w['cT']}")
w = min(rows, key=lambda r: r['D3'] - r['hhi']); print(f"  min D3 - hhi (all mu) = {w['D3'] - w['hhi']} at m={w['m']} A={w['A']}")
w = min(R, key=lambda r: r['full']); print(f"  min full bound = {w['full']} at m={w['m']} A={w['A']} W={w['WS']}")
w = max(rows, key=lambda r: F(r['mu'] * r['R0'] + r['h'], r['D3'])); print(f"  max (mu R0 + h)/D3 (all mu) = {float(F(w['mu'] * w['R0'] + w['h'], w['D3'])):.4f} at m={w['m']} A={w['A']} mu={w['mu']} R0={w['R0']} h={w['h']} D3={w['D3']}")
w = max(R, key=lambda r: F(r['mu'] * r['R0'] + r['h'], r['D3'])); print(f"  max (mu R0 + h)/D3 (mu<=e) = {float(F(w['mu'] * w['R0'] + w['h'], w['D3'])):.4f} at m={w['m']} A={w['A']} mu={w['mu']} R0={w['R0']} h={w['h']} D3={w['D3']}")
w = max(rows, key=lambda r: F(r['mu'] * r['R0'], r['D3'])); print(f"  max mu R0/D3 (all mu) = {float(F(w['mu'] * w['R0'], w['D3'])):.4f} at m={w['m']} A={w['A']} mu={w['mu']} R0={w['R0']} h={w['h']} D3={w['D3']}")
print('  hlo_mu histogram:', sorted(collections.Counter(r['hlo_mu'] for r in R).items()))
