# flowdiv: max-flow test of local charging rules for MU-LO (mu <= e) / A1 (mu > e) on the exhaustive Q5 residual.
# Supply: every standard square x (level 2) with capacity P(x) = sum_{i: x+e_i not in D} (x_i+1); every missing square
# q with capacity 4 (the 4*M2 part of Delta3 = 4 M2 + B2).  Demand: NE class s with tau_s < c_T and mu | tau_s: mu
# (mu <= e) [A1 for mu > e: every NE class below c_T demands e]; NE class with tau_s >= c_T: 1.
# Rule DIV (radius R): NE class s may draw from squares within distance R of its standard rep x_s in the monomial
# lattice (R = 1: square divisors of a level-3 rep, or the rep itself if level 2); missing squares adjacent likewise.
# Output: number of S where the max flow saturates the demand, and the worst deficit.
import sys, heapq, collections
from itertools import combinations_with_replacement as cwr
def maxflow(nn, edges, s, t):
    g = [[] for _ in range(nn)]
    for u, v, c in edges:
        g[u].append([v, c, len(g[v])]); g[v].append([u, 0, len(g[u]) - 1])
    flow = 0
    while True:
        lvl = [-1] * nn; lvl[s] = 0; q = collections.deque([s])
        while q:
            u = q.popleft()
            for v, c, r in g[u]:
                if c > 0 and lvl[v] < 0: lvl[v] = lvl[u] + 1; q.append(v)
        if lvl[t] < 0: return flow
        it = [0] * nn
        def dfs(u, f):
            if u == t: return f
            while it[u] < len(g[u]):
                v, c, r = g[u][it[u]]
                if c > 0 and lvl[v] == lvl[u] + 1:
                    d = dfs(v, min(f, c))
                    if d > 0:
                        g[u][it[u]][1] -= d; g[v][r][1] += d; return d
                it[u] += 1
            return 0
        while True:
            f = dfs(s, 10 ** 9)
            if f == 0: break
            flow += f
def analyse(m, A, R):
    d = len(A); e = d + 1; mu = A[0]; best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k, c)
            if cl not in best or key < best[cl]: best[cl] = key
    vec = lambda c: tuple(sum(1 for t in c if t == i) for i in range(d))
    rep = {cl: vec(best[cl][2]) for cl in best}; h = {cl: sum(rep[cl]) for cl in best}; sg = {cl: best[cl][0] - h[cl] * m for cl in best}
    D = set(rep.values())
    tau = [None] * m; tau[0] = 0; pq = [(0, 0)]; done = [False] * m
    while pq:
        t, c = heapq.heappop(pq)
        if done[c]: continue
        done[c] = True
        for a in A:
            u = t + a; cc = u % m
            if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
    cT = max(tau) - m + 1
    NE = [cl for cl in range(m) if tau[cl] < sg[cl]]
    dem = {}
    for cl in NE:
        if tau[cl] >= cT: dem[cl] = 1
        elif mu <= e: dem[cl] = mu if tau[cl] % mu == 0 else 0
        else: dem[cl] = e
    sq = [vec(c) for c in cwr(range(d), 2)]
    cap = {}
    for x in sq:
        if x in D: cap[x] = sum(x[i] + 1 for i in range(d) if tuple(x[j] + (j == i) for j in range(d)) not in D)
        else: cap[x] = 4
    D3 = 3 * (e - 1) * m - e * sum(h.values()); assert D3 == sum(cap.values())
    dist = lambda x, y: sum(abs(a - b) for a, b in zip(x, y)) // 2 if sum(x) == sum(y) else (sum(abs(a - b) for a, b in zip(x, y)) - 1) // 2 + (1 if sum(x) != sum(y) else 0)
    # distance between a square y and a rep x: number of moves; R=1 means y divides x (|x|=3) or y = x (|x|=2)
    def near(y, x):
        if sum(x) == 2: diff = sum(abs(a - b) for a, b in zip(x, y)); return diff <= 2 * (R - 1)
        over = sum(max(0, a - b) for a, b in zip(x, y)); under = sum(max(0, b - a) for a, b in zip(x, y))
        return under <= R - 1 and over == 1 + under
    nodes = {('S',): 0, ('T',): 1}; edges = []
    for x in sq:
        if cap[x] > 0: nodes[('q', x)] = len(nodes); edges.append((0, nodes[('q', x)], cap[x]))
    tot = 0
    for cl in NE:
        if dem[cl] == 0: continue
        nodes[('n', cl)] = len(nodes); edges.append((nodes[('n', cl)], 1, dem[cl])); tot += dem[cl]
        for x in sq:
            if cap[x] > 0 and near(x, rep[cl]): edges.append((nodes[('q', x)], nodes[('n', cl)], 10 ** 6))
    f = maxflow(len(nodes), edges, 0, 1)
    return dict(e=e, mu=mu, tot=tot, flow=f, D3=D3)
R = int(sys.argv[1]); rows = []
for fn in sys.argv[2:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:])), R); r['m'] = int(t[1]); r['A'] = list(map(int, t[15:])); rows.append(r)
bad = [r for r in rows if r['flow'] < r['tot']]
print(f"R={R} {sys.argv[2]}: {len(rows)} S; saturated {len(rows) - len(bad)}; total-budget fails {sum(1 for r in rows if r['D3'] < r['tot'])}")
for r in sorted(bad, key=lambda r: r['flow'] - r['tot'])[:5]:
    print(f"   deficit {r['tot'] - r['flow']} (demand {r['tot']}, flow {r['flow']}, D3 {r['D3']}) m={r['m']} A={r['A']} mu={r['mu']}")
