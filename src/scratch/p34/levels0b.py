r"""Values of gamma_j (levels0.py) and tests of candidate pairings (lead, 2026-10-21):
PAIR: gamma_j + gamma_{J+1-j} >= 0;  PREFIX-SUFFIX: suffix sums sum_{i>=j} gamma_i >= 0 for every j.
Usage: python levels0b.py NS SEED MMAX"""
import sys, random
from math import gcd
sys.path.insert(0, '.')
from tile import build
from levels0 import levels
NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED)
cnt = 0; fpair = 0; fsuf = 0; fmono = 0; shown = 0
while cnt < NS:
    m = rnd.randint(8, MMAX); G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 4]) * m), rnd.randint(2, min(7, m - 2))))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; N = len(gens); D = list(M)
    if N < 2: continue
    for u in [u for u in range(1, m) if gcd(u, m) == 1][:6]:
        delta = [(u * g) % m for g in gens]
        gam, L = levels(m, D, delta); cnt += 1; J = len(gam)
        if any(gam[j] + gam[J - 1 - j] < 0 for j in range(J)): fpair += 1
        if any(sum(gam[j:]) < 0 for j in range(J)): fsuf += 1
        neg = [j for j in range(J) if gam[j] < 0]; pos = [j for j in range(J) if gam[j] > 0]
        if neg and pos and max(neg) > min(pos): fmono += 1
        if shown < 12 and any(g < 0 for g in gam) and J >= 3: shown += 1; print(m, gens, u, "gam", gam, "Lnm/m %.2f" % float(L), flush=True)
print("instances %d  PAIR fails %d  SUFFIX fails %d  sign-pattern (neg after pos) %d" % (cnt, fpair, fsuf, fmono))
