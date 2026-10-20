r"""Is P18 depth-four Wilf a consequence of LOCAL conditions plus COUNTING of the [h, m) covering? (lead, 2026-10-20)
Fake configurations: m, B subset [1, m), A = {0} u B, h in [1, m] with
  (C1) [0, h) subset 4A u ((3A n [m, m+h)) - m)      (layer-4 covering of the low residues)
  (C3) h-1 not in 3A and h-1+m not in 2A             (the defining gap)
  but NOT requiring (C2) [h, m) subset R3 = 3A_{<m} u ((2A n [m,2m)) - m).
m_eff = h + |R3 n [h, m)|  (= m exactly when (C2) holds);  W_eff = e(1 + e + |2A_{<m}| + |R3 n [0,h)|) - 3 m_eff - h.
Also reports the same with (C2) restricted to the first window [h, min(m, 2h)) ('C2w').
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random
def analyse(m, B):
    A = [0] + list(B); e = len(A); As = set(A)
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    R2 = [s for s in X2 if s < m]
    R3 = set(s for s in X3 if s < m) | set(s - m for s in X2 if s >= m)
    out = []
    for h in range(1, m + 1):
        if not all((r in X4) or (r + m in X3) for r in range(h)): break  # (C1) is monotone in h
        if (h - 1) in X3 or (h - 1 + m) in X2: continue
        meff = h + sum(1 for r in range(h, m) if r in R3)
        x = sum(1 for r in range(h) if r in R3)
        Weff = e * (1 + e + len(R2) + x) - 3 * meff - h
        c2 = (meff == m)
        c2w = all(r in R3 for r in range(h, min(m, 2 * h)))
        out.append((Weff, h, c2, c2w))
    return out
best = {}
def rec(m, B):
    for Weff, h, c2, c2w in analyse(m, B):
        for key in (("all",), ("C2w",) if c2w else None, ("C2",) if c2 else None):
            if key is None: continue
            if key not in best or Weff < best[key][0]: best[key] = (Weff, m, tuple(B), h)
            if Weff < 0: cnt[key] = cnt.get(key, 0) + 1
cnt = {}
if sys.argv[1] == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5])
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k): rec(m, B)
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    for _ in range(N):
        m = random.randint(mlo, mhi); rec(m, sorted(random.sample(range(1, m), k)))
print(sys.argv[1:], "min W_eff:", best, "negatives:", cnt)
