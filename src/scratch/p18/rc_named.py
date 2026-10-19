"""RC and CHAIN-WILF ratios on named hard semigroups (W_0 < 0 examples, E47, Eliahou-Fromentin B_3 family)."""
import heapq, math
def apery(m, gens):
    w = [None]*m; w[0] = 0; pq = [(0, 0)]
    while pq:
        dd, r = heapq.heappop(pq)
        if dd > w[r]: continue
        for n in gens:
            r2 = (r+n) % m
            if w[r2] is None or dd+n < w[r2]:
                w[r2] = dd+n; heapq.heappush(pq, (dd+n, r2))
    return w
def rep(name, m, gens):
    w = apery(m, [m]+gens); ap = set(w); M = max(w); c = M - m + 1; q = -(-c//m)
    inS = lambda x: x >= 0 and x >= w[x % m]
    n = [x for x in sorted(ap) if x > 0 and not any(inS(y) and inS(x-y) for y in range(m, x-m+1))]
    d = len(n); need2 = (d-1)*m*(m-1)
    R = sum((M-x) % g for x in w for g in n)
    Bc = 0
    for g in n:
        for x in w:
            t = x
            while t + g in ap: t += g
            Bc += M - t
    ell = sum(1 for x in range(c) if inS(x)); W = (d+1)*ell - c
    print('%-28s m=%d e=%d c=%d q=%d W=%d  RC=%.4f  CHAIN=%.4f  3e>=m:%s' % (name, m, d+1, c, q, W, 2*R/need2, 2*Bc/need2, 3*(d+1) >= m))
rep('<14,22,23>_56 (E47)', 14, [22, 23] + list(range(56, 70)))
rep('<16,25,26>_64', 16, [25, 26] + list(range(64, 80)))
rep('<17,26,28>_68', 17, [26, 28] + list(range(68, 85)))
rep('<17,27,28>_68', 17, [27, 28] + list(range(68, 85)))
rep('<18,28,29>_72', 18, [28, 29] + list(range(72, 90)))
rep('<30,44,48,49>_118', 30, [44, 48, 49] + list(range(118, 148)))
# Eliahou-Fromentin: S = <m, A>_{4m}, A a B_3-set mod m inside [(3m+1)/2, (5m-1)/3]
def b3_family(m, k):
    lo, hi = (3*m + 1 + 1)//2, (5*m - 1)//3
    A = []
    for x in range(lo, hi + 1):
        T = A + [x]
        sums = {}
        ok = True
        import itertools
        for comb in itertools.combinations_with_replacement(T, 3):
            s_ = sum(comb) % m
            if s_ in sums and sums[s_] != comb: ok = False; break
            sums[s_] = comb
        if ok: A = T
        if len(A) >= k: break
    return A
for m_, k_ in ((60, 4), (120, 5), (250, 6), (400, 7)):
    A = b3_family(m_, k_)
    rep('EF B3 m=%d |A|=%d' % (m_, len(A)), m_, A + list(range(4*m_, 5*m_)))
