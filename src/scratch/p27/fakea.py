r"""Local fakes ((C1), gap; m -> m_eff) with optional first window C2w = [h, min(2h,m)) subset R3 and second window
C2w2 = [h, min(3h,m)) subset R3 (lead, 2026-10-20).  Reports min of TB4 = T+E1, reda = RED-A RHS, SP0, by a-class.
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random
def configs(m, B):
    A = [0] + list(B); e = len(A)
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    R3 = set(s for s in X3 if s < m) | set(s - m for s in X2 if s >= m)
    E1 = e * (e + 1) - 2 * len(X2)
    for h in range(1, m + 1):
        if not all((r in X4) or (r + m in X3) for r in range(h)): break
        if (h - 1) in X3 or (h - 1 + m) in X2: continue
        L = m + h
        real = all(r in R3 for r in range(h, m))
        w1 = all(r in R3 for r in range(h, min(m, 2 * h))); w2 = all(r in R3 for r in range(h, min(m, 3 * h)))
        As = [x for x in A if x < h]; a = len(As) - 1; beta = e - 1 - a
        As2 = set(p + q for p in As for q in As); As3 = set(s + p for s in As2 for p in As)
        y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3); T = e * y0 - 3 * N4 - h
        OP = sum(1 for x in B for y in B if x + y >= L); Phs = [s for s in X2 if s >= L]; Phi = len(Phs)
        dhi = sum(1 for s in Phs if (s - m) in X3)
        Plo = sum(1 for s in X2 if m <= s < L); delta = sum(1 for s in X2 if m <= s < L and (s - m) in X3)
        reda = T + E1 + (OP - Phi) + 2 * delta + beta * (Plo - delta) + 3 * dhi
        t = sum(1 for s in As3 if h <= s < 2 * h)
        SP0 = (a + 1) * y0 - 3 * N4 - t + E1
        yield dict(real=real, w1=w1, w2=w2, a=a, TB4=T + E1, reda=reda, SP0=SP0, m=m, B=tuple(B), h=h)
st = {}
def rec(m, B):
    for r in configs(m, B):
        if r["real"]: continue
        lev = "w2" if r["w2"] else ("w1" if r["w1"] else "loc")
        for lv in ("loc", "w1", "w2"):
            if lv == "w1" and lev == "loc": continue
            if lv == "w2" and lev != "w2": continue
            key = (lv, "a0" if r["a"] == 0 else ("a1-2" if r["a"] <= 2 else "a3+"))
            d = st.setdefault(key, {"n": 0}); d["n"] += 1
            for f in ("TB4", "reda", "SP0"):
                if f not in d or r[f] < d[f][0]: d[f] = (r[f], r["m"], r["B"], r["h"])
                if r[f] < 0: d["neg_" + f] = d.get("neg_" + f, 0) + 1
if sys.argv[1] == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5])
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k): rec(m, B)
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    for _ in range(N):
        m = random.randint(mlo, mhi); rec(m, sorted(random.sample(range(1, m), k)))
print(sys.argv[1:])
for key in sorted(st):
    d = st[key]; print("  ", key, "n", d["n"], {f: d[f][0] for f in ("TB4", "reda", "SP0")}, {k2: v for k2, v in d.items() if k2.startswith("neg")}, "reda@", d["reda"][1:], "SP0@", d["SP0"][1:])
