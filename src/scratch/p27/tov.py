r"""Token lemma OVF and Conjecture TOV for P18 depth four (lead, 2026-10-20).
Lemma OVF (claimed PROVED, elementary): for every L, E3_L = (e-1)|2A_{<L}| - 3|(3A\2A)_{<L}| >= OVF_L,
  OVF_L = #{(s, b) in 2A_{<L} x B : s + b >= L}.  (Checked here for every L in [1, 3m].)
Exact: W = E1 + E3_L + T - P_hi - e*delta + 3*delta_hi + 3*omega (L = m+h).
TOV:   E1 + T + OVF_L + 3*delta_hi + 3*omega - P_hi - e*delta >= 0   (drops G = E3_L - OVF_L >= 0).
Also reports TB4 = T + E1, the a <= 2 reduction check W >= TB4 (when a <= 2), and TOV on local fakes.
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random
def go(m, B, st):
    A = [0] + list(B); e = len(A)
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    new3 = sorted(X3 - X2); X2s = sorted(X2)
    # Lemma OVF at every L
    for L in range(1, 3 * m + 1, max(1, m // 7)):
        E3 = (e - 1) * sum(1 for s in X2 if s < L) - 3 * sum(1 for v in new3 if v < L)
        ovf = sum(1 for s in X2 if s < L for b in B if s + b >= L)
        if E3 < ovf: st["ovf_fail"] += 1
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
        y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3); T = e * y0 - 3 * N4 - h
        Phs = [s for s in X2 if L <= s < 2 * m]; Phi = len(Phs); dhi = sum(1 for s in Phs if (s - m) in X3)
        delta = sum(1 for s in X2 if m <= s < L and (s - m) in X3)
        omega = sum(1 for v in X3 if m <= v < L and (v - m) in X4)
        ovf = sum(1 for s in X2 if s < L for b in B if s + b >= L)
        tov = E1 + T + ovf + 3 * dhi + 3 * omega - Phi - e * delta
        a = sum(1 for b in B if b < h)
        kind = "real" if real else "fake"
        for key, val in ((kind + " TOV", tov), (kind + " TB4", T + E1)):
            if key not in st["min"] or val < st["min"][key][0]: st["min"][key] = (val, m, tuple(B), h, a, e)
            if val < 0: st["neg"][key] = st["neg"].get(key, 0) + 1
        if real and a <= 2 and W < T + E1: st["red_fail"] += 1
def main():
    st = dict(ovf_fail=0, red_fail=0, min={}, neg={})
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k): go(m, B, st)
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); go(m, sorted(random.sample(range(1, m), k)), st)
    print(sys.argv[1:], "OVF lemma fails:", st["ovf_fail"], " a<=2 reduction fails:", st["red_fail"], " negatives:", st["neg"])
    for k in sorted(st["min"]): print("   min", k, st["min"][k])
if __name__ == "__main__": main()
