"""Residue-free P_i on full simplices {|x| <= t} in N^k with equal weights n > q: find failures with the largest M/q.
Conjecture H_i: P_i holds residue-free once M >= (2i-2)q - 1.  fejer only."""
from math import comb
import sys
best = {}
for i in range(3, 9):
    worst = None
    for k in range(2, 9):
        for t in range(2, 14):
            cnt = [comb(j + k - 1, k - 1) for j in range(t + 1)]
            for q in range(2, 61):
                for n in range(q + 1, 3 * q + 1):
                    M = t * n
                    L = sum(cnt[j] * min(i, (j * n) // q) for j in range(t + 1))
                    R = k * sum(cnt[j] * min(i, ((t - j) * n) // q) for j in range(t + 1))
                    if L > R:
                        r = (M + 1) / q
                        if worst is None or r > worst[0]: worst = (r, dict(k=k, t=t, q=q, n=n, M=M, L=L, R=R))
    best[i] = worst
    thr = (2 * i - 2)
    print(f"i={i}: largest (M+1)/q among simplex failures = {worst[0]:.4f}  (conjectured threshold 2i-2 = {thr})  {worst[1]}", flush=True)
