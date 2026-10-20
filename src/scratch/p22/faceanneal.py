# Anneal B/C fillers around a fixed dense high A-core to minimize FACE-WILF slack per excess (lead, 2026-10-20).
import random, sys, math
from faceup import build, analyze, sums_unique
random.seed(int(sys.argv[1])); m = int(sys.argv[2]); ITER = int(sys.argv[3])
best_overall = None
for restart in range(1000):
    h = random.randint(m // 3, m - 1); k = random.randint(3, 7); T = []
    for _ in range(4000):
        if len(T) >= k: break
        t = random.randint((h + 1) // 2, h - 1)
        if t not in T and sums_unique(T + [t], 3): T.append(t)
    if len(T) < 3: continue
    Bs = [m + h + random.randrange(m) for _ in range(random.randint(0, 6))]
    Cs = [2 * m + h + random.randrange(m) for _ in range(random.randint(0, 3))]
    def score(Bs, Cs):
        r = analyze(m, build(m, h, T, Bs, Cs))
        if r is None or r['crit'] <= r['F']: return None, r
        return r['slack'] / (r['crit'] - r['F']), r
    cur, r0 = score(Bs, Cs)
    if cur is None: continue
    for it in range(ITER):
        nB, nC = list(Bs), list(Cs); mv = random.randint(0, 5)
        if mv == 0 and nB: nB.pop(random.randrange(len(nB)))
        elif mv == 1 and nC: nC.pop(random.randrange(len(nC)))
        elif mv == 2: nB.append(m + h + random.randrange(m))
        elif mv == 3: nC.append(2 * m + h + random.randrange(m))
        elif mv == 4 and nB: i = random.randrange(len(nB)); nB[i] = m + h + random.randrange(m)
        elif nC: i = random.randrange(len(nC)); nC[i] = 2 * m + h + random.randrange(m)
        s, r = score(nB, nC)
        if s is None: continue
        if r['slack'] < 0: print("FACEWILF FAIL", r, T, nB, nC, flush=True)
        if s <= cur or random.random() < 0.05: Bs, Cs, cur = nB, nC, s
        if best_overall is None or s < best_overall[0]:
            best_overall = (s, r, T, list(nB), list(nC)); print("best", round(s, 3), r, T, nB, nC, flush=True)
