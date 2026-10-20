"""Per-direction ray-end depths (lead, 2026-10-21). For the lex tile Mhat of S and direction i,
B^i = sum_{beta in Mhat} (c + m - 1 - phi(end_i(beta))).  CH': Wilf <=> sum_i B^i >= (N-1) m (m-1)/2.
Test ALL-BUT-ONE: #{i : B^i < m(m-1)/2} <= 1.  Usage: python perdir.py NS SEED MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
def perdir(m, G):
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; N = len(gens); top = c + m - 1
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
    B = [0] * N
    for a, x in M.items():
        for i in range(N):
            if up(a, i) not in M: B[i] += (a[i] + 1) * (top - x)
    return c, gens, B
NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED)
from collections import Counter
hist = Counter(); worst = None; nb = 0
for _ in range(NS):
    m = rnd.randint(4, MMAX); k = rnd.randint(2, 7); G = [rnd.randint(m + 1, rnd.choice([2, 3, 5, 8]) * m + 1) for _ in range(k)]
    v = perdir(m, G)
    if v is None: continue
    c, gens, B = v; N = len(gens)
    if c <= 4 * m or N < 2: continue
    h = m * (m - 1) / 2; low = [i for i in range(N) if B[i] < h]
    hist[len(low)] += 1; nb += 1
    ratio = min(sorted(b / h for b in B)[1:]) if N >= 2 else None
    if worst is None or ratio < worst[0]: worst = (ratio, m, gens, c, [round(b / h, 3) for b in B])
    if len(low) >= 2 and hist[len(low)] <= 5: print("TWO LOW:", m, gens, c, [round(b / h, 3) for b in B], flush=True)
print("S tested", nb, "histogram #low directions", dict(hist)); print("worst second-smallest ratio", worst)
