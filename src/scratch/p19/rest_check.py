"""Independent REST check (lead, 2026-10-19): REST = sum_{w in Ap, w != 0} sum_a ((M-w) mod m - (M - top_a(w))),
computed in the 'N_a' form  REST = sum_a n_a * #{(w,j): w in Ap\\{0}, j>=1, w + j n_a in Ap} - m*d*ell',
ell' = #{x in S cap (0,c) : m does not divide x}.  Apery set by Dijkstra, generators by decomposability.
usage: python rest_check.py m g1,g2,...   (or no args: built-in list)"""
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
def rest(m, g):
    w = apery(m, [m] + g); ap = set(w); M = max(w); c = M - m + 1
    gens = sorted(x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m))
    d = len(gens)
    inS = lambda x: x >= 0 and x >= w[x % m]
    ellp = sum(1 for x in range(1, c) if x % m and inS(x))
    N = 0
    for n in gens:
        for x in w:
            if x == 0: continue
            j = 1
            while x + j*n in ap: N += n; j += 1
    R = N - m*d*ellp
    C2 = m*(m-1)//2
    return R, R/C2, M, gens[0], M >= 3*gens[0]
ex = [(6, [7, 16]), (14, [15, 23, 24, 26]), (13, [16, 17, 18]), (18, [25, 26, 27, 28, 29, 30, 31]), (19, [21, 22, 26, 27, 29]), (13, [18, 19, 20, 21, 22])]
if len(sys.argv) > 2: ex = [(int(sys.argv[1]), [int(x) for x in sys.argv[2].split(',')])]
for m, g in ex: print(m, g, '-> REST, REST/C2, M, n1, M>=3n1 =', rest(m, g))
