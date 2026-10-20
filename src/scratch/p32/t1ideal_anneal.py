"""Adversarial search for the combinatorial T1 (T1-ideal): maximize V = sum_M (j - c) - rho - (m - |M|) over
(m, rho, B, M), M a divisor-closed family of multisets with rho + alpha.b distinct mod m. Moves: add an addable
multiset at a free position, remove a removable leaf, perturb B / rho (then rebuild M greedily, preferring wrapped
multisets with large j). V > 0 refutes T1-ideal. Usage: python t1ideal_anneal.py ITERS SEED MMAX KMAX"""
import sys, random, math
IT, SEED, MMAX, KMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
def evalM(m, rho, B, M):
    K = len(B); V = 0
    for a in M:
        s = rho + sum(x * b for x, b in zip(a, B)); j = s // m
        V += j - sum(a[i] * (j - (s - B[i]) // m) for i in range(K) if a[i] > 0)
    return V - rho - (m - len(M))
def addables(m, rho, B, M, pos):
    K = len(B); out = []
    for a in M:
        for i in range(K):
            b2 = tuple(a[k] + (k == i) for k in range(K))
            if b2 in M: continue
            s = rho + sum(x * b for x, b in zip(b2, B))
            if s % m in pos: continue
            if all(b2[k] == 0 or tuple(b2[l] - (l == k) for l in range(K)) in M for k in range(K)): out.append(b2)
    return list(set(out))
def removables(M, K):
    out = []
    for a in M:
        if sum(a) == 0: continue
        if all(tuple(a[k] + (k == i) for k in range(K)) not in M for i in range(K)): out.append(a)
    return out
def greedy(m, rho, B, bias):
    K = len(B); M = {(0,) * K}; pos = {rho % m}
    while True:
        ad = addables(m, rho, B, M, pos)
        if not ad: break
        if rnd.random() < bias: ad.sort(key=lambda a: -((rho + sum(x * b for x, b in zip(a, B))) // m)); a = ad[0]
        else: a = rnd.choice(ad)
        M.add(a); pos.add((rho + sum(x * b for x, b in zip(a, B))) % m)
        if rnd.random() < 0.01: break
    return M
best = -10**9; bestst = None
for restart in range(10**9):
    m = rnd.randint(5, MMAX); rho = rnd.randint(0, m - 1); K = rnd.randint(2, KMAX)
    B = sorted(rnd.sample(range(1, m), min(K, m - 1))) if rnd.random() < 0.6 else sorted(rnd.sample(range(1, 2 * m), K))
    M = greedy(m, rho, B, rnd.random()); v = evalM(m, rho, B, M); T = 2.0
    for it in range(IT):
        pos = {(rho + sum(x * b for x, b in zip(a, B))) % m for a in M}
        r = rnd.random(); M2 = set(M)
        if r < 0.45:
            ad = addables(m, rho, B, M2, pos)
            if not ad: continue
            M2.add(rnd.choice(ad))
        elif r < 0.9:
            rm = removables(M2, len(B))
            if not rm: continue
            M2.discard(rnd.choice(rm))
        else:
            continue
        v2 = evalM(m, rho, B, M2)
        if v2 >= v or rnd.random() < math.exp((v2 - v) / T):
            M, v = M2, v2
            if v > best:
                best = v; bestst = (m, rho, B, sorted(M)); print("best V=%d" % v, m, rho, B, len(M), flush=True)
                if v > 0: print("REFUTED T1-ideal:", bestst, flush=True)
        T = max(0.2, T * 0.999)
    if restart % 50 == 0: print("restart", restart, "best", best, flush=True)
