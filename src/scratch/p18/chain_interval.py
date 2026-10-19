"""Independent check (lead, 2026-10-19): CHAIN-WILF on interval semigroups S = <m, km+a, km+a+1, ..., km+b>.
Computes Ap by Dijkstra from the generators, minimal generators by Apery decomposability, B_chain by walking chains,
need = (d-1)m(m-1)/2, W = e*ell - c.  Reports all S with ratio B_chain/need < 1 and the minimum per (m, k).
usage: python chain_interval.py mlo mhi kmax"""
import sys, heapq
def apery(m, gens):
    w = [None]*m; w[0] = 0; pq = [(0, 0)]
    while pq:
        dd, r = heapq.heappop(pq)
        if dd > w[r]: continue
        for n in gens:
            r2 = (r+n) % m
            if w[r2] is None or dd+n < w[r2]:
                w[r2] = dd+n; heapq.heappush(pq, (dd+n, r2))
    return w
def chain_stats(m, gens_in):
    w = apery(m, [m] + gens_in)
    if any(x is None for x in w): return None
    ap = set(w); M = max(w); c = M - m + 1; q = -(-c//m)
    gens = sorted(x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m))
    d = len(gens)
    if d < 2: return None
    Bc = 0
    for g in gens:
        for x in w:
            t = x
            while t + g in ap: t += g
            Bc += M - t
    need = (d - 1)*m*(m - 1)//2
    ell = sum((c - 1 - x)//m + 1 for x in w if x < c); W = (d + 1)*ell - c
    return dict(ratio=Bc/need, Bc=Bc, need=need, e=d+1, c=c, q=q, W=W, gens=gens)
if __name__ == '__main__':
    if sys.argv[1] == 'one':
        m = int(sys.argv[2]); g = [int(x) for x in sys.argv[3].split(',')]
        print(chain_stats(m, g)); sys.exit()
    mlo, mhi, kmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    fails = []; best = None
    for m in range(mlo, mhi + 1):
        for k in range(1, kmax + 1):
            for a in range(1, m):
                for b in range(a + 1, m):
                    r = chain_stats(m, list(range(k*m + a, k*m + b + 1)))
                    if not r or r['q'] < 4: continue
                    if best is None or r['ratio'] < best[0]: best = (r['ratio'], m, k, a, b, r['e'], r['c'], r['q'], r['W'])
                    if r['ratio'] < 1: fails.append((round(r['ratio'], 4), m, k, a, b, r['e'], r['c'], r['q'], r['W']))
    fails.sort()
    print('interval semigroups <m, km+a..km+b>, m in [%d,%d], k <= %d, q >= 4: CHAIN failures = %d' % (mlo, mhi, kmax, len(fails)))
    for f in fails[:25]: print('  FAIL ratio=%.4f m=%d k=%d [a,b]=[%d,%d] e=%d c=%d q=%d W=%d' % f)
    print('min:', best)
