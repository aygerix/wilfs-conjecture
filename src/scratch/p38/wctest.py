# wctest: wrap count WC := #{(x, b) : x standard square (level 2 in D), b in A, v = sigma(x) + b, and
#   v - m in U or v - 2m in U}  (a slot whose cube wraps onto a smaller element of its class; WC <= B2 <= Delta3).
# Also WCw := sum of the slot weights (x_b + 1) over those slots.  Compares WC with the MU-LO demand
# mu*hlo_mu + h_hi (mu <= e), with the A1 demand e*h_lo + h_hi (mu > e), and with the TRUNC3 deficit max(0, c_U - e l(U)).
import sys, heapq
from itertools import combinations_with_replacement as cwr
def analyse(m, A):
    d = len(A); e = d + 1; mu = A[0]; best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k, c)
            if cl not in best or key < best[cl]: best[cl] = key
    vec = lambda c: tuple(sum(1 for t in c if t == i) for i in range(d))
    rep = {cl: vec(best[cl][2]) for cl in best}; h = {cl: sum(rep[cl]) for cl in best}; sg = {cl: best[cl][0] - h[cl] * m for cl in best}
    tau = [None] * m; tau[0] = 0; pq = [(0, 0)]; done = [False] * m
    while pq:
        t, c = heapq.heappop(pq)
        if done[c]: continue
        done[c] = True
        for a in A:
            u = t + a; cc = u % m
            if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
    cT = max(tau) - m + 1; cU = max(sg.values()) - m + 1
    inU = lambda x: x >= 0 and x >= sg[x % m]; inT = lambda x: x >= tau[x % m]
    D3 = 3 * (e - 1) * m - e * sum(h.values())
    WC = WCw = 0
    for cl in range(m):
        x = rep[cl]
        if sum(x) != 2: continue
        for i in range(d):
            v = sg[cl] + A[i]
            if inU(v - m) or inU(v - 2 * m): WC += 1; WCw += x[i] + 1
    assert WCw <= D3
    hlo = sum(1 for z in range(cT) if inT(z) and not inU(z)); hhi = sum(1 for z in range(cT, cU) if not inU(z))
    hlo_mu = sum(1 for z in range(0, cT, mu) if not inU(z))
    lU = sum(1 for z in range(cU) if inU(z)); deficit = max(0, cU - e * lU)
    dem = mu * hlo_mu + hhi if mu <= e else e * hlo + hhi
    return dict(e=e, mu=mu, D3=D3, WC=WC, WCw=WCw, dem=dem, deficit=deficit)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:]))); r['m'] = int(t[1]); r['A'] = list(map(int, t[15:])); rows.append(r)
print(f"{sys.argv[1]}: {len(rows)} residual S, e = {rows[0]['e']}")
for k in ('WC', 'WCw'):
    w = max(rows, key=lambda r: r['dem'] / max(r[k], 1))
    print(f"  demand vs {k}: fails {sum(1 for r in rows if r[k] < r['dem'])}; max demand/{k} {w['dem'] / max(w[k], 1):.3f} at m={w['m']} A={w['A']} ({k}={w[k]}, D3={w['D3']}, dem={w['dem']})")
    w = max(rows, key=lambda r: r['deficit'] / max(r[k], 1))
    print(f"  TRUNC3 deficit vs {k}: fails {sum(1 for r in rows if r[k] < r['deficit'])}; max deficit/{k} {w['deficit'] / max(w[k], 1):.3f} at m={w['m']} A={w['A']}")
print('  mean WCw/D3 =', round(sum(r['WCw'] / r['D3'] for r in rows) / len(rows), 3), ' min WCw/D3 =', round(min(r['WCw'] / r['D3'] for r in rows), 3))
