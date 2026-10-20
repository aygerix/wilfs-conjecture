"""Ray mass at maximal elements (lead, 2026-10-21). For the full lex tile M^ of random S (N = e-1):
R = sum_{y in Max} (|y| + N); crude TM holds if R <= (N+1) m / 2; shape-only REARR: sum_k w_(k)(m-k) <= (N+1) C(m,2).
Reports both ratios, split by m >= 3e vs m < 3e. Usage: python rcount.py NS SEED MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED)
st = {True: [0, 0, 0, 0.0, 0.0, None], False: [0, 0, 0, 0.0, 0.0, None]}
for _ in range(NS):
    m = rnd.randint(4, MMAX); G = [rnd.randint(m + 1, rnd.choice([2, 3, 5, 8]) * m) for _ in range(rnd.randint(1, 8))]
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; N = len(gens)
    if N < 2: continue
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
    w = sorted((sum(a) + N for a in M if all(up(a, i) not in M for i in range(N))), reverse=True)
    Rm = sum(w); r1 = Rm / ((N + 1) * m / 2)
    r2 = sum(wk * (m - k) for k, wk in enumerate(w, 1)) / ((N + 1) * m * (m - 1) / 2)
    key = m >= 3 * (N + 1); s = st[key]
    s[0] += 1; s[1] += r1 > 1; s[2] += r2 > 1; s[3] = max(s[3], r1)
    if r2 > s[4]: s[4] = r2; s[5] = (m, c, gens, N)
for key in (True, False):
    s = st[key]
    print("m >= 3e" if key else "m < 3e ", ": S", s[0], " crude R>(N+1)m/2:", s[1], " REARR fails:", s[2], " max crude ratio %.3f max REARR ratio %.3f at %s" % (s[3], s[4], s[5]))
