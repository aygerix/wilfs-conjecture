r"""Brute force over Kunz vectors k in [1,K]^(m-1) (lead, 2026-10-20): min W per (e, r). Cross-check for kunz_milp.py.
usage: python3 brute_kunz.py m K"""
import sys, itertools
m, K = int(sys.argv[1]), int(sys.argv[2]); best = {}
for k in itertools.product(range(1, K + 1), repeat=m - 1):
    k = (0,) + k
    if not all(k[i] + k[j] + (1 if i + j > m else 0) >= k[(i + j) % m] for i in range(1, m) for j in range(i, m) if i + j != m): continue
    w = [0] + [m * k[i] + i for i in range(1, m)]; Ws = set(w)
    e = 1 + sum(1 for s in range(1, m) if not any(w[s] - w[i] in Ws and w[s] - w[i] > 0 for i in range(1, m) if w[i] < w[s]))
    r = max(range(1, m), key=lambda i: w[i]); c = w[r] - m + 1; g = sum(k)
    W = e * (c - g) - c
    if (e, r) not in best or W < best[e, r]: best[e, r] = W
for key in sorted(best): print(f"e={key[0]} r={key[1]} minW={best[key]}")
