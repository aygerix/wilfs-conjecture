r"""All-depth order/level identity for S = <m, m+B> (all generators in (m, 2m)) (lead, 2026-10-20).
depth q = ceil(c/m) >= 2, h = c - (q-1)m in (0, m].  H_j = #{w in Ap : ord(w) = j} (Hilbert function of gr(R/t^m R)),
E_k = (e-1) sum_{i<k} H_i - k H_k (condensed Macaulay slack, >= 0 by Eliahou Thm 5.11), T_c = sum_w (level - ord) = g - sum ord.
Claim:  W = sum_{k=2}^{q-1} E_k + (e-1) h - (e+q-1) H_q - e T_c   (exact).
usage: rnd k mlo mhi N seed"""
import sys, random, heapq
def analyse(m, B):
    e = len(B) + 1
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in B:
            v = d0 + m + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    c = max(w) - m + 1
    if c <= m: return None
    q = -(-c // m); h = c - (q - 1) * m
    ap = set(w); order = {0: 0}
    for v in sorted(w)[1:]:
        order[v] = max(order[v - m - x] + 1 for x in B if v - m - x >= 0 and (v - m - x) in ap)
    g = sum(v // m for v in w); W = e * (c - g) - c
    H = [0] * (q + 2)
    for v in w: H[order[v]] += 1
    Tc = g - sum(order[v] for v in w)
    E = lambda k: (e - 1) * sum(H[:k]) - k * H[k]
    F = sum(E(k) for k in range(2, q)) + (e - 1) * h - (e + q - 1) * H[q] - e * Tc
    return q, W, F, Tc, min(E(k) for k in range(1, q + 1))
k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
st = {}
for _ in range(N):
    m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k))
    r = analyse(m, B)
    if r is None: continue
    q, W, F, Tc, mE = r
    s = st.setdefault(q, [0, 0, 0, 10 ** 9]); s[0] += 1; s[1] += (W != F); s[2] += (Tc == 0); s[3] = min(s[3], mE)
for q in sorted(st): print(sys.argv[1:], "depth", q, "S", st[q][0], "mismatches", st[q][1], "carry-free", st[q][2], "min E_k", st[q][3])
