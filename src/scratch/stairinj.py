# Inj-TOP (A) on 2D staircases Delta_k = {x1+x2 <= k-1} with injective phi in Z/m, m in [|Delta_k|, |Delta_k|+6]
import sys
for k in range(3, 10):
    D = [(i, j) for i in range(k) for j in range(k - i)]
    A = [(i, k - 1 - i) for i in range(k)]
    N = [z for z in D if z not in A]
    n0 = len(D)
    for m in range(n0, n0 + 7):
        best = None; cnt = 0
        for p1 in range(1, m):
            for p2 in range(1, m):
                res = {y: (y[0]*p1 + y[1]*p2) % m for y in D}
                if len(set(res.values())) != n0: continue
                cnt += 1
                for s in range(m):
                    pi = {y: m - (s - res[y]) % m for y in D}
                    sl = m*m + sum(pi[z] for z in N) - sum((sum(y)+1)*pi[y] for y in A)
                    if best is None or sl < best[0]: best = (sl, p1, p2, s)
        print('k', k, '|D|', n0, 'm', m, 'injective p', cnt, 'min slack', best, flush=True)
