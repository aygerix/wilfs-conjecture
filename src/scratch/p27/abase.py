r"""a >= 1: tightness of the RED-A2 lower bound and of the first-window small-part bound (lead, 2026-10-20).
For real P18 depth-four S:
  base = (T+E1) + (OP-P_hi) + (2-a)delta + beta(P_lo-delta) + 3(omega-delta) + 3 delta_hi      (RED-A2 RHS; W >= base)
  SP   = (a+1) y0 - 3 N4 - t + E1 + (2-a) delta,  t = |3A_s n [h, 2h)|, A_s = A n [0, h)      (small part)
  HP   = beta*y0 - beta1*y0'' - eta,  y0'' = |2A_s n [0,h)|                                    (high part; >= 0 if 3h <= m)
  (for 2h <= m: W >= base >= SP + HP + rest, PROVED chain)
Reports min by (a, regime) where regime = 'third' (3h<=m), 'mid' (m/3<h<m/2), 'half' (2h>=m).
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
    h = c - 3 * m; L = m + h
    g = sum(x // m for x in w); W = e * (c - g) - c
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    As = [x for x in A if x < h]; a = len(As) - 1; beta = e - 1 - a
    As2 = set(p + q for p in As for q in As); As3 = set(s + p for s in As2 for p in As)
    E1 = e * (e + 1) - 2 * len(X2)
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3); T = e * y0 - 3 * N4 - h
    OP = sum(1 for x in B for y in B if x + y >= L); Phs = [s for s in X2 if s >= L]; Phi = len(Phs)
    dhi = sum(1 for s in Phs if (s - m) in X3)
    Plo = sum(1 for s in X2 if m <= s < L); delta = sum(1 for s in X2 if m <= s < L and (s - m) in X3)
    omega = sum(1 for v in X3 if m <= v < L and (v - m) in X4)
    base = T + E1 + (OP - Phi) + (2 - a) * delta + beta * (Plo - delta) + 3 * (omega - delta) + 3 * dhi
    t = sum(1 for s in As3 if h <= s < 2 * h)
    SP = (a + 1) * y0 - 3 * N4 - t + E1 + (2 - a) * delta
    y0pp = sum(1 for s in As2 if s < h); beta1 = sum(1 for x in B if h <= x < 2 * h); eta = sum(1 for x in B if 2 * x >= L)
    HP = beta * y0 - beta1 * y0pp - eta
    reg = "third" if 3 * h <= m else ("half" if 2 * h >= m else "mid")
    return dict(m=m, B=tuple(B), h=h, e=e, a=a, W=W, base=base, SP=SP, HP=HP, reg=reg, TB4=T + E1)
st = {}
def rec(r):
    if r is None or r["a"] == 0: return
    key = (min(r["a"], 6), r["reg"], "allA" if r["a"] == r["e"] - 1 else "mixed")
    d = st.setdefault(key, {})
    d["n"] = d.get("n", 0) + 1
    if r["W"] < r["base"]: d["chain_fail"] = d.get("chain_fail", 0) + 1
    for f in ("W", "base", "SP", "HP", "TB4"):
        if f not in d or r[f] < d[f][0]: d[f] = (r[f], r["m"], r["B"], r["h"])
        if r[f] < 0: d["neg_" + f] = d.get("neg_" + f, 0) + 1
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
    d = st[key]; print("  ", key, "n", d["n"], {f: d[f][0] for f in ("W", "base", "SP", "HP", "TB4")}, {k2: v for k2, v in d.items() if k2.startswith("neg") or k2 == "chain_fail"}, "SPmin@", d["SP"][1:], "basemin@", d["base"][1:])
