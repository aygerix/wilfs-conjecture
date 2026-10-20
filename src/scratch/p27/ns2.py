r"""Constructed near-simplex instances (lead, 2026-10-20): B = x + U with U a set whose 3-fold sumset covers an initial
interval; x ~ m/3.  Tests the exact NS formula from ns.run on every NS hit and reports min W, min W/e^2.
usage: ns2.py k Dlo Dhi N seed"""
import sys, random
from ns import run
k, Dlo, Dhi, N, seed = map(int, sys.argv[1:6]); random.seed(seed)
recs = []; seen = set()
for _ in range(N):
    D = random.randint(Dlo, Dhi)
    U = sorted({0, D} | set(random.sample(range(1, D), k - 2)))
    if len(U) != k: continue
    S3 = sorted(set(a + b + c for a in U for b in U for c in U))
    K = 0
    while K in S3: K += 1          # 3U covers [0, K)
    for m in range(3 * K - 6, 3 * K + 7):
        for x in range(m // 3 - 1, m // 3 + 3):
            B = [x + u for u in U]
            if m < 4 or B[0] < 1 or B[-1] >= m or (m, tuple(B)) in seen: continue
            seen.add((m, tuple(B)))
            r = run(m, B)
            if r: recs.append(r)
print(sys.argv[1:], "NS S:", len(recs), "formula mismatches:", sum(1 for r in recs if r["W"] != r["F"]))
if recs:
    mn = min(recs, key=lambda r: r["W"]); print("  min W", mn)
    mr = min(recs, key=lambda r: r["W"] / r["e"] ** 2); print("  min W/e^2", round(mr["W"] / mr["e"] ** 2, 3), mr)
