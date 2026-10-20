r"""DK (LASTWIN at depth four) on random general S with 3m < c <= 4m (lead, 2026-10-20).
usage: dk4.py seed N mlo mhi nmin nmax hi   (generators random in (m, hi*m))"""
import sys, random
from layer import apery
seed, N, mlo, mhi, nmin, nmax, hi = map(int, sys.argv[1:8]); random.seed(seed)
n = bad = 0; worst = None; byq = {}
for _ in range(N):
    m = random.randint(mlo, mhi); gens = [m] + random.sample(range(m + 1, hi * m), random.randint(nmin, nmax))
    w = apery(gens)
    if w is None: continue
    c = max(w) - m + 1; q = -(-c // m)
    if q != 4: continue
    aps = set(w); srt = sorted(w)
    e = 1 + sum(1 for v in srt[1:] if not any((v - u) in aps for u in srt[1:] if u < v))
    h = c - 3 * m; lv = [x // m for x in w]
    X = sum(1 for r in range(h) if lv[r] <= 3); sl = e * X - h
    n += 1; bad += sl < 0
    if worst is None or sl < worst[0]: worst = (sl, m, e, h, X, sorted(gens))
print(sys.argv[1:], "depth-four S", n, "DK fails", bad, "worst (slack, m, e, h, L3, gens)", worst)
