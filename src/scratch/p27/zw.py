r"""Identity W = E1 + E3_L + T - P_hi - e*delta + 3*delta_hi + 3*omega (L = m+h) and Conjecture ZW (lead, 2026-10-20).
E3_L = (e-1)|2A_{<L}| - 3|(3A\2A)_{<L}| >= 3|Z| (RTCM with Q = 2A_{>=L}), Z = {v in 3A\2A : v >= L, v not in 2A_{>=L} + A}.
ZW: E1 + T + 3|Z| + 3*omega + 3*delta_hi - P_hi - e*delta >= 0.
Runs on real depth-four P18 semigroups ('real') and on local fakes ((C1),(C3) only, m replaced by m_eff; 'fake').
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random
def configs(m, B):
    A = [0] + list(B); e = len(A)
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    R2 = [s for s in X2 if s < m]
    R3 = set(s for s in X3 if s < m) | set(s - m for s in X2 if s >= m)
    E1 = e * (e + 1) - 2 * len(X2)
    for h in range(1, m + 1):
        if not all((r in X4) or (r + m in X3) for r in range(h)): break
        if (h - 1) in X3 or (h - 1 + m) in X2: continue
        L = m + h
        meff = h + sum(1 for r in range(h, m) if r in R3); real = (meff == m)
        x = sum(1 for r in range(h) if r in R3)
        W = e * (1 + e + len(R2) + x) - 3 * meff - h
        E3 = (e - 1) * sum(1 for s in X2 if s < L) - 3 * sum(1 for s in X3 - X2 if s < L)
        Qh = [s for s in X2 if s >= L]; QA = set(q + a for q in Qh for a in A)
        Z = sum(1 for v in X3 - X2 if v >= L and v not in QA)
        y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3); T = e * y0 - 3 * N4 - h
        Phs = [s for s in X2 if L <= s < 2 * m]; Phi = len(Phs); dhi = sum(1 for s in Phs if (s - m) in X3)
        delta = sum(1 for s in X2 if m <= s < L and (s - m) in X3)
        omega = sum(1 for v in X3 if m <= v < L and (v - m) in X4)
        ident = E1 + E3 + T - Phi - e * delta + 3 * dhi + 3 * omega
        zw = E1 + T + 3 * Z + 3 * omega + 3 * dhi - Phi - e * delta
        a = sum(1 for b in B if b < h)
        yield dict(real=real, W=W, ok=(W == ident), zw=zw, h=h, a=a, e=e, m=m, B=tuple(B), Z=Z, E3=E3, T=T, Phi=Phi, E1=E1)
if __name__ != "__main__": pass
def _main():
    global best, neg, bad
    best = {}; neg = {}; bad = 0
    def rec(m, B):
        global bad
        for r in configs(m, B):
            if not r["ok"]: bad += 1
            for key in (("fake" if not r["real"] else "real"), ("all-zw")):
                v = r["zw"]
                if r["real"]: k2 = "real"
                else: k2 = "fake"
                kk = (k2, "a0" if r["a"] == 0 else "a>0")
                if kk not in best or v < best[kk][0]: best[kk] = (v, {x: r[x] for x in ("m", "B", "h", "e", "W", "Z", "E3", "T", "Phi", "E1")})
                if v < 0: neg[kk] = neg.get(kk, 0) + 1
                break
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k): rec(m, B)
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); rec(m, sorted(random.sample(range(1, m), k)))
    print(sys.argv[1:], "identity mismatches (real only meaningful):", bad, "ZW negatives:", neg)
    for kk in sorted(best): print("  ", kk, "min ZW", best[kk])
if __name__ == "__main__": _main()
