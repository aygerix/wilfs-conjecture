r"""All-A (B subset [1,h)) and general small-part window bounds (lead, 2026-10-20).
For real P18 depth-four S compute, with W1 = [h, h + ceil(h/2)) (if inside [h,m)):
  SPh = e*y0 - 3*N4 - (2*|R3 n W1| - [h odd]) + E1     (T + E1 with h replaced by the half-window bound)
  SPf = e*y0 - 3*N4 - |R3 n [h,2h)| + E1                (first-window bound; needs 2h <= m)
  TB4 = T + E1 itself.  Report min of each and of max(SPh, SPf) by class (allA / mixed) and regime.
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
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    R3 = set(s for s in X3 if s < m) | set(s - m for s in X2 if s >= m)
    E1 = e * (e + 1) - 2 * len(X2)
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    a = sum(1 for x in B if x < h)
    hh = (h + 1) // 2
    SPh = None
    if h + hh <= m: SPh = e * y0 - 3 * N4 - (2 * sum(1 for r in range(h, h + hh) if r in R3) - (h % 2)) + E1
    SPf = None
    if 2 * h <= m: SPf = e * y0 - 3 * N4 - sum(1 for r in range(h, 2 * h) if r in R3) + E1
    reg = "third" if 3 * h <= m else ("half" if 2 * h >= m else "mid")
    return dict(m=m, B=tuple(B), h=h, e=e, a=a, TB4=e * y0 - 3 * N4 - h + E1, SPh=SPh, SPf=SPf, reg=reg, cls="allA" if a == e - 1 else ("a0" if a == 0 else "mixed"))
st = {}
def rec(r):
    if r is None: return
    key = (r["cls"], r["reg"]); d = st.setdefault(key, {"n": 0}); d["n"] += 1
    vals = {"TB4": r["TB4"], "SPh": r["SPh"], "SPf": r["SPf"]}
    cand = [v for v in (r["SPh"], r["SPf"]) if v is not None]
    vals["best"] = max(cand) if cand else None
    for f, v in vals.items():
        if v is None: continue
        if f not in d or v < d[f][0]: d[f] = (v, r["m"], r["B"], r["h"])
        if v < 0: d["neg_" + f] = d.get("neg_" + f, 0) + 1
if sys.argv[1] == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5])
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k): rec(run(m, B))
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    for _ in range(N):
        m = random.randint(mlo, mhi); rec(run(m, sorted(random.sample(range(1, m), k))))
print(sys.argv[1:])
for key in sorted(st):
    d = st[key]; print("  ", key, "n", d["n"], {f: d[f][0] for f in ("TB4", "SPh", "SPf", "best") if f in d}, {k2: v for k2, v in d.items() if k2.startswith("neg")}, "SPh@", d.get("SPh", (None,))[1:], "best@", d.get("best", (None,))[1:])
