"""Is T1 combinatorial?  For an ARBITRARY order ideal M of multisets over offsets B (divisor-closed) with
sigma(alpha) = rho + alpha.b injective mod m, define j = floor(sigma/m), y = sigma mod m,
c(alpha) = sum_i alpha_i * (floor(sigma/m) - floor((sigma - b_i)/m)), r = m - |M|.
T1-ideal: sum_M (j - c) <= rho + r ?   Random greedy ideals (random insertion order of addable multisets),
optionally restricted by a level cap lambda = |alpha| + j <= q.  Usage: python t1ideal.py NR SEED"""
import sys, random
NR, SEED = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(SEED)
fails = 0; worst = None; n = 0
for it in range(NR):
    m = rnd.randint(6, 60); rho = rnd.randint(0, m - 1); K = rnd.randint(2, 5)
    B = sorted(rnd.sample(range(1, m), K)) if rnd.random() < 0.7 else sorted(rnd.sample(range(1, 3 * m), K))
    q = rnd.randint(3, 9) if rnd.random() < 0.5 else 99
    zero = (0,) * K
    M = {zero: rho}; pos = {rho % m}
    def sig(a): return rho + sum(x * b for x, b in zip(a, B))
    def lev(a): return sum(a) + sig(a) // m
    frontier = set()
    def addables(a):
        for i in range(K):
            b2 = tuple(a[k] + (k == i) for k in range(K))
            if b2 in M: continue
            if all((b2[k] == 0) or (tuple(b2[l] - (l == k) for l in range(K)) in M) for k in range(K)): yield b2
    for a in [zero]: frontier.update(addables(a))
    stop = rnd.random()
    while frontier:
        b2 = rnd.choice(sorted(frontier)); frontier.discard(b2)
        if b2 in M: continue
        s = sig(b2)
        if s % m in pos or lev(b2) > q: continue
        if rnd.random() < 0.02 * stop: continue
        M[b2] = s; pos.add(s % m); frontier.update(addables(b2))
    r = m - len(M); JC = 0
    for a, s in M.items():
        j = s // m
        c = sum(a[i] * (j - (s - B[i]) // m) for i in range(K) if a[i] > 0)
        JC += j - c
    n += 1
    if JC > rho + r:
        fails += 1
        if worst is None or rho + r - JC < worst[0]: worst = (rho + r - JC, m, rho, B, q, len(M), sorted(M)[:12])
print("ideals", n, "T1-ideal failures", fails, "worst", worst)
