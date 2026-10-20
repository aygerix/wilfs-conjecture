r"""RED-A (all a): W >= (T+E1) + (OP-P_hi) + 2 delta + beta (P_lo - delta) + 3 delta_hi  (lead, 2026-10-20; claimed PROVED).
Also, for 3h <= m, the small-part bound W >= SP0 + (beta-beta1)(y0-1) + 2 delta, SP0 = (a+1) y0 - 3 N4 - t + E1,
t = |3A_s n [h,2h)|; reports min SP0 and min of the combined bound by regime/a.
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
sys.path.insert(0, '.')
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
    reda = T + E1 + (OP - Phi) + 2 * delta + beta * (Plo - delta) + 3 * dhi
    t = sum(1 for s in As3 if h <= s < 2 * h); beta1 = sum(1 for x in B if h <= x < 2 * h)
    SP0 = (a + 1) * y0 - 3 * N4 - t + E1
    comb = SP0 + (beta - beta1) * (y0 - 1) + 2 * delta
    reg = "third" if 3 * h <= m else ("half" if 2 * h >= m else "mid")
    return dict(m=m, B=tuple(B), h=h, e=e, a=a, W=W, reda=reda, SP0=SP0, comb=comb, reg=reg)
def _main():
    global st, fails, combfail
    st = {}; fails = 0; combfail = 0
    def rec(r):
        global fails, combfail
        if r is None: return
        if r["W"] < r["reda"]: fails += 1
        if r["reg"] == "third" and r["W"] < r["comb"]: combfail += 1
        key = (min(r["a"], 6), r["reg"])
        d = st.setdefault(key, {"n": 0})
        d["n"] += 1
        for f in ("W", "reda", "SP0", "comb"):
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
    print(sys.argv[1:], "RED-A violations:", fails, " third-regime chain violations:", combfail)
    for key in sorted(st):
        d = st[key]; print("  ", key, "n", d["n"], {f: d[f][0] for f in ("W", "reda", "SP0", "comb")}, {k2: v for k2, v in d.items() if k2.startswith("neg")}, "SP0min@", d["SP0"][1:])
if __name__ == '__main__': _main()
