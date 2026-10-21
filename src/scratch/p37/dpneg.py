r"""Inspect S with U = T but Delta' < 0 (lead, 2026-10-21): max-kappa factorization down-set D, column tops, and the
per-column terms |C| * (M_S - M_T - m kappa(top)).  usage: python dpneg.py g1 g2 ..."""
import sys, heapq
G = sorted(map(int, sys.argv[1:])); m = G[0]; P = G[1:]; d = len(P); e = d + 1
k = [g // m for g in P]; a = [g % m for g in P]
def apery(mod, gens):
    w = [None] * mod; w[0] = 0; h = [(0, 0)]; done = [False] * mod
    while h:
        v, s = heapq.heappop(h)
        if done[s]: continue
        done[s] = True
        for x in gens:
            t = (v + x) % mod
            if w[t] is None or v + x < w[t]: w[t] = v + x; heapq.heappush(h, (v + x, t))
    return w
w = apery(m, P); tau = apery(m, a)
# max-kappa factorization, ties by lex-least vector: DP in increasing w
order = sorted(range(m), key=lambda s: w[s]); n = {0: (0,) * d}
for s in order[1:]:
    best = None
    for i in range(d):
        t = (s - P[i]) % m
        if w[t] == w[s] - P[i] and t in n:
            cand = tuple(n[t][j] + (1 if j == i else 0) for j in range(d))
            key = (sum(cand[j] * k[j] for j in range(d)), tuple(-x for x in cand))
            if best is None or key > best[0]: best = (key, cand)
    n[s] = best[1]
D = set(n.values()); assert len(D) == m
kap = {s: sum(n[s][j] * k[j] for j in range(d)) for s in range(m)}
sig = {s: sum(n[s][j] * a[j] for j in range(d)) for s in range(m)}
print("S=%s m=%d e=%d levels=%s residues=%s" % (G, m, e, k, a))
print("U=T:", all(sig[s] == tau[s] for s in range(m)), " M_S=%d M_T=%d K*=%d sum kappa=%d" % (max(w), max(tau), max(kap.values()), sum(kap.values())))
MS, MT = max(w), max(tau)
Dp = (e - 1) * (MS - MT) - e * sum(kap.values()); print("Delta' =", Dp)
tot = 0
for i in range(d):
    for x in D:
        if x[i] == 0:
            L = 0
            while tuple(x[j] + (L if j == i else 0) for j in range(d)) in D: L += 1
            top = tuple(x[j] + ((L - 1) if j == i else 0) for j in range(d))
            kt = sum(top[j] * k[j] for j in range(d)); term = L * (MS - MT - m * kt); tot += term
            if term < 0: print("  dir %d column from %s length %d top %s kappa(top)=%d sigma(top)=%d term=%d" % (i, x, L, top, kt, sum(top[j] * a[j] for j in range(d)), term))
print("sum terms / m =", tot / m)
