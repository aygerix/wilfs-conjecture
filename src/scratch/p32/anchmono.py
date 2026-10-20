"""Is the ANCHOR slack monotone in the cutoff q for a fixed model (m, rho, B)? (lead, 2026-10-20)
Reports, per q, the number of models with slack(q) < slack(q-1) and the minimum of slack(q) - slack(q-1).
Usage: python anchmono.py NRAND SEED"""
import random, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from anchq import parts
NR, SEED = int(sys.argv[1]), int(sys.argv[2])
rnd = random.Random(SEED)
neg = {}; mind = {}; ex = {}
for it in range(NR):
    m = rnd.randint(10, 50); rho = rnd.randint(0, m - 3); N = m - rho
    K = rnd.randint(2, min(7, N - 1))
    lo = rnd.choice([1, N // 3, N // 2])
    pool = list(range(max(1, lo), N))
    if len(pool) < K: continue
    B = sorted(rnd.sample(pool, K))
    prev = None
    for q in range(2, 8):
        r = parts(m, rho, B, q)
        if prev is not None:
            dlt = r['slack'] - prev['slack']
            if dlt < 0: neg[q] = neg.get(q, 0) + 1
            if q not in mind or dlt < mind[q]: mind[q] = dlt; ex[q] = (m, rho, B, prev['slack'], r['slack'])
        prev = r
print("models with slack(q) < slack(q-1):", neg)
print("min delta:", mind)
print("examples:", ex)
