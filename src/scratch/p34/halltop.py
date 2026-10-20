r"""HALL-TOP test on leaves (r = 0) (lead, 2026-10-21).
Leaf S = <m, Gamma>, lex tile M (n = e-1 dirs), Y = Apery elements >= c, h(y) = phi(y) - c, eps(b) = (phi(b) - c) mod m.
TOP0 (aggregate): sum_Y (|y|-1) h(y) <= (n+1) sum_{M \ Y} eps.
HALL-TOP (local): a transport exists: y needs (|y|-1) h(y), may draw only from b in B(y) \ {0, y}, each b supplies
at most (n+1) eps(b).  Checked by max-flow.  Usage: python halltop.py NS SEED MMAX DMIN"""
import sys, random
from collections import deque
sys.path.insert(0, '.')
from tile import build
def maxflow(nv, edges, s, t):
    g = [[] for _ in range(nv)]
    for u, v, cap in edges:
        g[u].append([v, cap, len(g[v])]); g[v].append([u, 0, len(g[u]) - 1])
    flow = 0
    while True:
        lvl = [-1] * nv; lvl[s] = 0; dq = deque([s])
        while dq:
            u = dq.popleft()
            for v, cap, _ in g[u]:
                if cap > 0 and lvl[v] < 0: lvl[v] = lvl[u] + 1; dq.append(v)
        if lvl[t] < 0: return flow
        it = [0] * nv
        def dfs(u, f):
            if u == t: return f
            while it[u] < len(g[u]):
                e = g[u][it[u]]; v, cap, rev = e
                if cap > 0 and lvl[v] == lvl[u] + 1:
                    d = dfs(v, min(f, cap))
                    if d > 0:
                        e[1] -= d; g[v][rev][1] += d; return d
                it[u] += 1
            return 0
        while True:
            f = dfs(s, 1 << 60)
            if f == 0: break
            flow += f
def test(m, G):
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; n = len(gens)
    if n < 2 or any(g >= c for g in gens): return None      # leaves only
    Y = [a for a, x in M.items() if x >= c]
    low = [a for a, x in M.items() if x < c and any(a)]
    idx = {a: i for i, a in enumerate(low)}
    eps = {a: (M[a] - c) % m for a in M}
    dem = {y: (sum(y) - 1) * (M[y] - c) for y in Y}
    top0 = (n + 1) * sum(eps[a] for a in M if M[a] < c) - sum(dem.values())
    s = 0; t = 1; base = 2; yi = {y: base + len(low) + j for j, y in enumerate(Y)}
    edges = [(s, yi[y], dem[y]) for y in Y]
    for a in low: edges.append((base + idx[a], t, (n + 1) * eps[a]))
    for y in Y:
        for a in low:
            if all(a[i] <= y[i] for i in range(n)): edges.append((yi[y], base + idx[a], 1 << 40))
    f = maxflow(base + len(low) + len(Y), edges, s, t)
    return sum(dem.values()) - f, top0, c, gens, (-c) % m
if __name__ == '__main__':
    NS, SEED, MMAX, DMIN = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
    tot = fH = fT = 0; mn = None; byrho = {}
    for _ in range(NS):
        m = rnd.randint(4, MMAX); G = [rnd.randint(m + 1, rnd.choice([2, 3, 4]) * m) for _ in range(rnd.randint(2, 6))]
        v = test(m, G)
        if v is None or v[2] <= DMIN * m: continue
        tot += 1; short, top0, c, gens, rho = v
        if top0 < 0: fT += 1; print("TOP0 FAIL", m, gens, c, top0, flush=True)
        key = 'rho=0' if rho == 0 else 'rho>0'; byrho.setdefault(key, [0, 0]); byrho[key][0] += 1
        if short > 0:
            byrho[key][1] += 1
            fH += 1
            if fH <= 8: print("HALL-TOP FAIL m=%d c=%d rho=%d gens=%s shortfall=%d top0slack=%d" % (m, c, rho, gens, short, top0), flush=True)
    print("leaves tested", tot, "TOP0 fails", fT, "HALL-TOP fails", fH, "by rho [tested, fails]:", byrho)
def load(m, G):
    """Load condition (sufficient for HALL-TOP when rho = 0): for every b in M_< \\ {0},
    sum_{y in Y, y >= b} s_y <= n+1, s_y = 2(|y|-1)/(prod(y_i+1) - 2). Returns (max load - (n+1), c, gens, rho)."""
    from fractions import Fraction as Fr
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; n = len(gens)
    if n < 2 or any(g >= c for g in gens): return None
    Y = [a for a, x in M.items() if x >= c]
    sy = {}
    for y in Y:
        P = 1
        for v in y: P *= v + 1
        sy[y] = Fr(2 * (sum(y) - 1), P - 2)
    worst = None
    for a, x in M.items():
        if x >= c or not any(a): continue
        L = sum(sy[y] for y in Y if all(a[i] <= y[i] for i in range(n)))
        if worst is None or L > worst: worst = L
    return (worst if worst is not None else 0) - (n + 1), c, gens, (-c) % m
