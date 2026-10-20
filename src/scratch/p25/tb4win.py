r"""Is TB4 (h + 3N4 <= e*y0 + E1) a consequence of the WINDOW condition alone? (lead, 2026-10-20)
Random A c [0,m), 0 in A, 1 <= h <= m.  Window condition: W1 = [h, 3h') c 3A u ((2A n [m+h, 2m)) - m) u (m + 4A_{<h}).
Optionally also require h-1 notin 3A u (2A - m) (the defining gap).  Reports TB4 failures among window-covered instances.
usage: python tb4win.py N seed mmax kmax gapflag [lowflag]  (lowflag: also require [0,h) c 4A u (3A n [m,m+h) - m))"""
import sys, random
N, seed, mmax, kmax, gapflag = map(int, sys.argv[1:6]); random.seed(seed)
lowflag = int(sys.argv[6]) if len(sys.argv) > 6 else 0
tot = fail = 0; worst = None
for _ in range(N):
    m = random.randint(6, mmax); k = random.randint(2, min(kmax, m - 1))
    B = random.sample(range(1, m), k); A = [0] + B; e = len(A)
    h = random.randint(2, m); hp = (h + 1) // 2
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    A4h = set(s for s in X4 if s < h)
    R1 = set(s - m for s in X2 if m + h <= s < 2 * m); R2 = set(m + s for s in A4h)
    if any(not (v in X3 or v in R1 or v in R2) for v in range(h, 3 * hp)): continue
    if gapflag and ((h - 1) in X3 or (h - 1 + m) in X2): continue
    if lowflag and any(not (r in A4h or (r + m) in X3) for r in range(h)): continue
    tot += 1
    E1 = e * (e + 1) - 2 * len(X2); y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in A4h if s not in X3)
    sl = e * y0 + E1 - h - 3 * N4
    if sl < 0:
        fail += 1
        if worst is None or sl < worst[0]: worst = (sl, m, sorted(B), h, e, y0, N4, E1)
print("window-covered instances:", tot, "TB4 failures:", fail, "worst:", worst)
