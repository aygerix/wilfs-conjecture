"""Depth-q carried-position identity for strip-free P18 window models (lead, 2026-10-20).
Model (m, rho, O), O subset of [1, N), N = m - rho: T = <m, m+b : b in O> u [q m - rho, inf).
Position u in [0,m) carries element k m + u - rho; lam(u) = least level; lamY(u) = least t with u - rho in t*O' unwrapped
(u >= rho, s + rho < m), inf if none. h_t = #{u : lamY = t}; d_t = (K+t-1) h_{t-1} - t h_t.
Claim: W0 = (K+1) ell - q d + rho = rho + sum_{t=2}^q (q+1-t) d_t + sum_{u carried} c(u),
  c(u) = (K+1)(lamY - lam)            if lamY <= q,
         (K+1)(q - lam) - q           if lamY > q and lam <= q,   (0 if lam > q).
Also reports, by depth, the classes with negative cost and the share of the deficit by level.
Usage: python carryq.py NRAND SEED"""
import random, sys
from collections import Counter

def model(m, rho, O, q):
    INF = 10**9
    # least level per position: Dijkstra over elements; level of element v (>= -rho) is (v + rho)//m
    # generate all sums s of t offsets (t <= q) with level t + (s+rho)//m <= q
    lam = [INF] * m; lamY = [INF] * m
    cur = {0}
    for t in range(0, q + 1):
        if t > 0:
            cur = {s + b for s in cur for b in O if t + (s + b + rho) // m <= q}
        for s in cur:
            lev = t + (s + rho) // m
            u = (s + rho) % m
            if lev < lam[u]: lam[u] = lev
            if s + rho < m and t < lamY[u]: lamY[u] = t
        # sums with 0 padding are covered since cur at t includes only exact t-sums; lamY uses exact counts
    return lam, lamY

def check(m, rho, O, q):
    K = len(O)
    lam, lamY = model(m, rho, O, q)
    ell = sum(max(0, q - l) for l in lam if l < 10**9)
    d = sum(1 for l in lam if l <= q)
    W0 = (K + 1) * ell - q * d + rho
    h = Counter(t for t in lamY if t <= q)
    hh = [h.get(t, 0) for t in range(q + 1)]
    dt = {t: (K + t - 1) * hh[t - 1] - t * hh[t] for t in range(2, q + 1)}
    cost = 0; neg = Counter()
    for u in range(m):
        l, ly = lam[u], lamY[u]
        if l > q or l == ly: continue
        if ly <= q: c = (K + 1) * (ly - l)
        else: c = (K + 1) * (q - l) - q
        cost += c
        if c < 0: neg[q - l] += c
    rhs = rho + sum((q + 1 - t) * dt[t] for t in dt) + cost
    return W0, rhs, dt, neg, K

if __name__ == "__main__":
    NR, SEED = int(sys.argv[1]), int(sys.argv[2])
    rnd = random.Random(SEED)
    bad = 0; n = 0; negd = Counter(); dneg = 0; minW0 = {}
    for it in range(NR):
        q = rnd.randint(4, 7)
        m = rnd.randint(10, 70)
        rho = rnd.randint(0, m - 3)
        N = m - rho
        K = rnd.randint(1, min(9, N - 1))
        O = sorted(rnd.sample(range(1, N), K))
        W0, rhs, dt, neg, K = check(m, rho, O, q)
        n += 1
        if W0 != rhs: bad += 1; print("MISMATCH", m, rho, O, q, W0, rhs); break
        if any(v < 0 for v in dt.values()): dneg += 1
        for j, v in neg.items(): negd[(q, K >= q - 1, j)] += 1
        minW0[q] = min(minW0.get(q, 10**9), W0)
    print("checked", n, "mismatches", bad, "models with some d_t < 0:", dneg)
    print("negative-cost carried classes (q, K>=q-1, j = q - lam): count of models", dict(sorted(negd.items())))
    print("min W0 by q", minW0)
