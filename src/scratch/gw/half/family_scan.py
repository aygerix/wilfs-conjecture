# Families <m, k*m + a_1, ..., k*m + a_s>: minimize W/c over small offsets for growing m, within the hard class
# (#PF >= 3m > e-1). Pure python (fejer).  usage: family_scan.py k s amax mlist
import sys, itertools, heapq
def apery(m, gens):
    INF = 10**18; dist = [INF]*m; dist[0] = 0; pq = [(0,0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > dist[r]: continue
        for g in gens:
            r2 = (r+g) % m; v = d0+g
            if v < dist[r2]: dist[r2] = v; heapq.heappush(pq, (v, r2))
    return dist
def stats(m, gens):
    ap = apery(m, gens)
    if max(ap) >= 10**17: return None
    M = max(ap); c = M - m + 1; g = sum(a//m for a in ap); l = c - g
    S = set(ap)
    e = 1 + sum(1 for r in range(1,m) if not any(((r-s) % m) != 0 and ap[s] + ap[(r-s) % m] == ap[r] for s in range(1,m)))
    pf = [ap[r]-m for r in range(1,m) if not any(ap[(r+s) % m] == ap[r]+ap[s] for s in range(1,m))]
    h3 = sum(1 for f in pf if f >= 3*m)
    return dict(e=e, c=c, W=e*l-c, t=len(pf), h3=h3, K=M//m)
k=int(sys.argv[1]); s=int(sys.argv[2]); amax=int(sys.argv[3]); ms=[int(x) for x in sys.argv[4].split(',')]
for m in ms:
    best=None
    for offs in itertools.combinations(range(1, amax+1), s):
        gens=[k*m+a for a in offs]
        st=stats(m, gens)
        if st is None or st['h3'] <= st['e']-1: continue
        r=st['W']/st['c']
        if best is None or r < best[0]: best=(r, offs, st)
    print(m, best, flush=True)
