r"""Order/level decomposition for P18 depth four (lead, 2026-10-20).
S = <m, m+B>, B subset [1,m-1], 3m < c = 3m+h <= 4m.  For w in Ap(S,m): level x = w // m, order o = max #generators in a
representation (no generator m, since w - m not in S).  H_j = #{w : o = j} is the Hilbert function of gr(R/t^m R).
Claimed exact identity:  W = E2 + E3 + (e-1)*y - 4*H4 - q - e*p, where
  E2 = e(e-1) - 2 H2,  E3 = (e-1)(e + H2) - 3 H3  (condensed Macaulay slacks, >= 0 by Eliahou Thm 5.11),
  y = #{r < h : level <= 3},  H4 = #{level 4, order 4},  q = #{level 4, order 3},  p = #{level 3, order 2}.
Also tests candidate inequalities I1: e*p <= E3,  I2: 4*H4 + q <= (e-1)*y + E2.
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
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
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m
    ap = set(w); order = {0: 0}
    for v in sorted(w)[1:]:
        best = -1
        for x in B:
            u = v - m - x
            if u >= 0 and u in ap and order.get(u, -1) >= 0: best = max(best, order[u] + 1)
        order[v] = best
    g = sum(v // m for v in w); W = e * (c - g) - c
    H = [0] * 6; p = q = H4 = y = qQ = 0
    carp = set(v for v in w if v // m == 3 and order[v] == 2)
    for r in range(m):
        v = w[r]; x = v // m; o = order[v]; H[o] += 1
        if x == 3 and o == 2: p += 1
        if x == 4 and o == 3:
            q += 1
            if any((v - m - b) in carp for b in B): qQ += 1
        if x == 4 and o == 4: H4 += 1
        if r < h and x <= 3: y += 1
    E2 = e * (e - 1) - 2 * H[2]; E3 = (e - 1) * (e + H[2]) - 3 * H[3]
    a = sum(1 for b in B if b < h); beta = e - 1 - a
    plo = sum(1 for r in range(h) if w[r] // m == 3 and order[w[r]] == 2); phi = p - plo; y0 = y - plo
    F = E2 + E3 + (e - 1) * y - 4 * H4 - q - e * p
    return dict(m=m, B=tuple(B), e=e, h=h, W=W, F=F, E2=E2, E3=E3, y=y, H4=H4, q=q, p=p, H=tuple(H[:5]),
                I1=E3 - e * p, I2=(e - 1) * y + E2 - 4 * H4 - q, qQ=qQ,
                J=E2 + (e - 1) * y - 4 * H4 - q - 3 * qQ - p, J0=E2 + (e - 1) * y - 4 * H4 - 4 * q - p,
                sig=E3 - (e - 1) * p + 3 * qQ, K=E2 + beta * y0 + (e - 2) * plo - phi - q - 3 * qQ, a=a,
                Jh=(E2 + (e - 1) * y - 4 * H4 - q - 3 * qQ - p) if h > e else 10 ** 9,
                Kh=(E2 + beta * y0 + (e - 2) * plo - phi - q - 3 * qQ) if h > e else 10 ** 9)
def _main():
    recs = []
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = analyse(m, B)
                if r: recs.append(r)
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k))
            r = analyse(m, B)
            if r: recs.append(r)
    print(sys.argv[1:], "S:", len(recs), "identity mismatches:", sum(1 for r in recs if r["W"] != r["F"]))
    for key in ("J", "sig", "K", "Jh", "Kh"):
        bad = [r for r in recs if r[key] < 0]
        print(" ", key, "failures", len(bad), "min", min((r[key] for r in recs), default=None))
        if bad: print("   e.g.", min(bad, key=lambda r: r[key]))
    print("  min W", min(recs, key=lambda r: r["W"]) if recs else None)
if __name__ == "__main__":
    _main()
