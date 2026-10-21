# zttest: ZT-RED  W >= D3 + e z - c_U + e|T cap [0, c_U - m)|   (m + T subset U by J1), asserted on every S;
# ZM (mu <= e): D3 + e z >= m suffices.  Reports min slacks of ZT, ZM (mu <= e), Z1 (e z >= m) split by mu <= e / mu > e.
import sys, heapq
src = open('zwtest.py').read(); exec(src.split('rows = []')[0])
def tcount(m, A, x):
    tau = [None] * m; tau[0] = 0; pq = [(0, 0)]; done = [False] * m
    while pq:
        t, c = heapq.heappop(pq)
        if done[c]: continue
        done[c] = True
        for a in A:
            u = t + a; cc = u % m
            if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
    return sum(1 for y in range(x) if y >= tau[y % m])
best = {}
n = 0
for fn in sys.argv[1:]:
    for L in open(fn):
        t = L.split()
        if t[0] != 'DUMP': continue
        m = int(t[1]); A = list(map(int, t[15:])); r = analyse(m, A); e = r['e']; n += 1
        x = r['cU'] - m; assert x >= 1
        tc = tcount(m, A, x)
        zt = r['D3'] + e * r['z'] - r['cU'] + e * tc
        assert r['WS'] >= zt, (m, A, r['WS'], zt)
        side = 'le' if r['mu'] <= e else 'gt'
        for key, val in (('ZT_' + side, zt), ('Z1_' + side, e * r['z'] - m), ('ZM_' + side, r['D3'] + e * r['z'] - m), ('W_' + side, r['WS'])):
            if key not in best or val < best[key][0]: best[key] = (val, m, A, r['D3'], r['z'], r['cU'], tc)
print(sys.argv[1], n, 'S')
for k in sorted(best): v = best[k]; print(f"  min {k} = {v[0]}  at m={v[1]} A={v[2]} D3={v[3]} z={v[4]} cU={v[5]} |T<cU-m|={v[6]}")
