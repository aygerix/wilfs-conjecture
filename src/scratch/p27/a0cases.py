r"""a = 0 (B subset [h, m)) at depth four, real P18 semigroups: check the case bounds (lead, 2026-10-20)
  3h <= m      : claim W >= 1 + E1 ;  h >= m/2 : claim W >= (e-2)(h-1);
  m/3 < h < m/2: report min of W, of K1 = (T+E1) + (OP - P_hi) and of Wlow = T + E1 + OP - P_hi + 2*delta + (e-1)(P_lo-delta).
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
def run(m, B):
    A = [0] + sorted(B); e = len(A)
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in B:
            v = d0 + m + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    c = max(w) - m + 1
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m
    if min(B) < h: return None
    g = sum(x // m for x in w); W = e * (c - g) - c; L = m + h
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A)
    E1 = e * (e + 1) - 2 * len(X2)
    OP = sum(1 for x in B for y in B if x + y >= L); Phi = sum(1 for s in X2 if s >= L)
    Plo = sum(1 for s in X2 if m <= s < L); delta = 1 if m in X2 else 0
    T = e - h
    return dict(m=m, B=tuple(B), h=h, e=e, W=W, E1=E1, K1=T + E1 + OP - Phi, Wlow=T + E1 + OP - Phi + 2 * delta + (e - 1) * (Plo - delta),
                case=("third" if 3 * h <= m else ("half" if 2 * h >= m else "mid")))
st = {}
def rec(r):
    if r is None: return
    cs = r["case"]
    if cs == "third": bad = r["W"] < 1 + r["E1"]
    elif cs == "half": bad = r["W"] < (r["e"] - 2) * (r["h"] - 1)
    else: bad = False
    d = st.setdefault(cs, dict(n=0, bad=0, minW=None, minK1=None, minWlow=None))
    d["n"] += 1; d["bad"] += bad
    for key, f in (("minW", "W"), ("minK1", "K1"), ("minWlow", "Wlow")):
        if d[key] is None or r[f] < d[key][0]: d[key] = (r[f], r["m"], r["B"], r["h"], r["e"])
if sys.argv[1] == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5])
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k): rec(run(m, B))
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    for _ in range(N):
        m = random.randint(mlo, mhi); rec(run(m, sorted(random.sample(range(1, m), k))))
print(sys.argv[1:])
for cs in st: print("  ", cs, st[cs])
