"""SIG on P18 fakes (lead, 2026-10-20).  A = {0} u B subset [0, m); levels via <m, m+B>.  For h in [1, m] with every
residue below h of level <= 4 (and h - 1 of level 4), test SIG(h): k (L3 + u2) + 2 Pu - 3|T| - 4 d4 >= 0, where
L3 = #{r < h: lev <= 3}, d4 = #{r < h: lev = 4}, T = level-3 residues that are unwrapped triples.  Modes:
  N : no condition on [h, m)          C : [h, m) all of level <= 3 (the real depth-four case, any c)
  W : [h, min(2h, m)) of level <= 3   R : residues >= h may have any level, but none of level 4
usage: sigfake.py mode k mlo mhi N seed"""
import sys, random, heapq
mode = sys.argv[1]; k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
n = bad = 0; worst = None
for _ in range(N):
    m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k))
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in B:
            v = d0 + m + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): continue
    lv = [x // m for x in w]
    pairs = [B[i] + B[j] for i in range(k) for j in range(i, k)]; Pu = sum(1 for s in pairs if s < m)
    u2 = sum(1 for r in range(m) if lv[r] == 2)
    trip = set(B[i] + B[j] + B[l] for i in range(k) for j in range(i, k) for l in range(j, k))
    T = sum(1 for r in range(m) if lv[r] == 3 and r in trip)
    base = k * u2 + 2 * Pu - 3 * T
    for h in range(1, m + 1):
        if any(lv[r] > 4 for r in range(h)) or lv[h - 1] != 4: continue
        if mode == "C" and any(lv[r] > 3 for r in range(h, m)): continue
        if mode == "W" and any(lv[r] > 3 for r in range(h, min(2 * h, m))): continue
        if mode == "H" and any(lv[r] > 3 for r in range(h, min(h + (h + 1) // 2, m))): continue
        if mode == "R" and any(lv[r] == 4 for r in range(h, m)): continue
        L3 = sum(1 for r in range(h) if lv[r] <= 3); d4 = h - L3
        n += 1; s = k * L3 + base - 4 * d4
        if s < 0:
            bad += 1
            if worst is None or s < worst[0]: worst = (s, m, B, h)
            if bad <= 4: print("FAIL", s, m, B, h, flush=True)
print(sys.argv[1:], "instances", n, "failures", bad, "worst", worst)
