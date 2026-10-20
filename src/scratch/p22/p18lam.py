# Where does Lambda come from in pure P18 at depth four? (lead, 2026-10-20). Exhaustive k-subsets for given m,k;
# keep the S with smallest margin Lam + Z - (h - e); print per-direction Lambda_a, blocked counts by reason.
import itertools, sys, heapq
def apery(m, gens):
    dist = {0: 0}; hq = [(0, 0)]
    while hq:
        d0, i = heapq.heappop(hq)
        if dist.get(i) != d0: continue
        for n in gens:
            j = (i + n) % m; nd = d0 + n
            if j not in dist or nd < dist[j]: dist[j] = nd; heapq.heappush(hq, (nd, j))
    return [dist.get(i) for i in range(m)]
def analyze(m, Bst):
    gens = [m + b for b in Bst]; w = apery(m, gens)
    if any(x is None for x in w): return None
    M = max(w); c = M - m + 1
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m; e = len(gens) + 1; aps = set(w)
    inS = lambda v: v >= 0 and w[v % m] <= v
    lam = {x: (M - x) // m for x in w}
    def nu(x, n):
        k = 0
        while inS(x - (k + 1) * n): k += 1
        return k
    Lam = 0; Z = 0; per = []; size_block = 0; coll_block = 0
    for n in gens:
        La = 0
        for x in w:
            if (x + n) not in aps:
                La += (nu(x, n) + 1) * lam[x]
                if lam[x] > 0:
                    if x + n > M: size_block += 1
                    else: coll_block += 1
        per.append(La); Lam += La
    for x in w:
        k = 4 - lam[x]
        for n in gens:
            j = nu(x, n)
            if j: k -= j * ((M - (x - n)) // m - lam[x])
        if k < 0: Z -= k
    lev = [sum(1 for x in w if lam[x] == j) for j in range(5)]
    return dict(B=Bst, m=m, c=c, h=h, e=e, Lam=Lam, Z=Z, margin=Lam + Z - (h - e), per=per, size_block=size_block, coll_block=coll_block, levels=lev,
                W=e * (c - sum(x // m for x in w)) - c)
m, k = int(sys.argv[1]), int(sys.argv[2]); res = []
for Bst in itertools.combinations(range(1, m), k):
    r = analyze(m, list(Bst))
    if r: res.append(r)
res.sort(key=lambda r: r['margin'])
print(len(res), "depth-four S")
for r in res[:6]: print(r)
