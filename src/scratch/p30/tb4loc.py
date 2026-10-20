"""TB4 under LOCAL conditions only, split by a = |B n [1,h)| (lead, 2026-10-20).
Fake: random A c [0,m) with 0 in A, h in [2, m].  Conditions: window [h, min(2h, m)) c S3 := 3A_{<m} u (2A_{>=m} - m);
defining gap h-1 not in S3; low covering [0,h) c 4A u (3A n [m, m+h) - m).  (No covering of [2h, m).)
Reports TB4 = e*y0 + E1 - h - 3*N4 failures by a.  usage: N seed mmax kmax"""
import sys, random
N, seed, mmax, kmax = map(int, sys.argv[1:5]); random.seed(seed)
half = len(sys.argv) > 5 and sys.argv[5] == "half"   # restrict to 2h <= m (genuinely local fakes)
struct = len(sys.argv) > 6 and sys.argv[6] == "struct"  # few small elements, the rest large
tot = {}; fail = {}; worst = {}
for _ in range(N):
    m = random.randint(8, mmax); k = random.randint(2, min(kmax, m - 1))
    h = random.randint(2, m // 2) if half else random.randint(2, m)
    if struct:
        a0 = random.randint(0, min(3, h - 1)); nb = max(1, k - a0)
        Bs = random.sample(range(1, h), a0) if a0 else []
        Bl = random.sample(range(h, m), min(nb, m - h)); B = sorted(set(Bs + Bl))
    else:
        B = random.sample(range(1, m), k)
    A = [0] + B; e = len(A)
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A)
    S3 = set(v for v in X3 if v < m) | set(v - m for v in X2 if v >= m)
    if (h - 1) in S3: continue
    if any(v not in S3 for v in range(h, min(2 * h, m))): continue
    X4 = set(s + p for s in X3 if s < m for p in A)
    if any(not (r in X4 or (r + m) in X3) for r in range(h)): continue
    a = sum(1 for b in B if b < h)
    tot[a] = tot.get(a, 0) + 1
    E1 = e * (e + 1) - 2 * len(X2); y0 = sum(1 for s in X3 if s < h)
    N4 = sum(1 for s in X4 if s < h and s not in X3)
    sl = e * y0 + E1 - h - 3 * N4
    if sl < 0:
        fail[a] = fail.get(a, 0) + 1
        if a not in worst or sl < worst[a][0]: worst[a] = (sl, m, sorted(B), h)
print(sys.argv[1:], "local fakes by a:", sorted(tot.items()))
print("  TB4 failures by a:", sorted(fail.items()))
for a in sorted(worst): print("   a =", a, "worst", worst[a])
