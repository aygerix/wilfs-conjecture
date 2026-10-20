"""Z12 on local fakes (lead, 2026-10-20).  A = {0} u B subset [0, m), S_3 = 3A_{<m} u (2A_{>=m} - m), T = 3A n [0,h).
Z12: |3A n [h,2h)| <= |T| + #{(t,b) in T x B : t + b >= h}.  Hypotheses per mode:
  W  : [h, 2h) subset S_3, 2h <= m
  WG : W and h - 1 not in S_3
  H  : only the half window [h, h + ceil(h/2)) subset S_3 (2h <= m)
  WGL: WG and [0, h) subset S_3 u (4A n [0,h)) u (3A n [m, m+h)) - m   (all residues of [0,h) at level <= 4)
usage: z12loc.py mode k mlo mhi N seed"""
import sys, random
mode = sys.argv[1]; k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
n = bad = 0; worst = None
for _ in range(N):
    m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k)); A = [0] + B
    X2 = set(a + b for i, a in enumerate(A) for b in A[i:]); X3 = set(s + a for s in X2 for a in A)
    S3 = set(v for v in X3 if v < m) | set(v - m for v in X2 if v >= m)
    X4 = set(s + a for s in X3 for a in A)
    for h in range(1, m // 2 + 1):
        win = range(h, h + (h + 1) // 2) if mode == "H" else (range(0) if mode == "N" else range(h, 2 * h))
        if not all(v in S3 for v in win): continue
        if mode in ("WG", "WGL") and (h - 1) in S3: continue
        if mode == "WGL" and not all(r in S3 or r in X4 or (r + m) in X3 for r in range(h)): continue
        n += 1
        T = [t for t in X3 if t < h]
        ovf = sum(1 for t in T for b in B if t + b >= h)
        lhs = sum(1 for v in X3 if h <= v < 2 * h)
        z = len(T) + ovf - lhs
        if z < 0:
            bad += 1
            if worst is None or z < worst[0]: worst = (z, m, B, h)
            if bad <= 5: print("FAIL", z, m, B, h, flush=True)
print(sys.argv[1:], "instances", n, "failures", bad, "worst", worst)
