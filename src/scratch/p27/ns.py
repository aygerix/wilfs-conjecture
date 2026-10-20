r"""Near-simplex class NS (lead, 2026-10-20): P18 depth four with B subset [1,h), 2B subset [0,m), 3B subset [m, m+h).
Claim (exact): W = 3e^2 + e + 2e*n2 - (e+3)*rho - 4h,  n2 = |2B \ A|, rho = m - h.  Also reports min W, min W/e^2.
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
def run(m, B):
    A = [0] + sorted(B); e = len(A)
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
    if max(B) >= h: return None
    S2 = set(x + y for x in B for y in B); S3 = set(x + y + z for x in B for y in B for z in B)
    if max(S2) >= m or min(S3) < m or max(S3) >= m + h: return None
    g = sum(x // m for x in w); W = e * (c - g) - c
    n2 = len(S2 - set(A)); rho = m - h
    F = 3 * e * e + e + 2 * e * n2 - (e + 3) * rho - 4 * h
    return dict(m=m, B=tuple(B), h=h, e=e, W=W, F=F)
def _main():
    recs = []
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = run(m, B)
                if r: recs.append(r)
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); lo = m // 3
            B = sorted(random.sample(range(lo, min(m, lo + m // 3 + 2)), k))
            r = run(m, B)
            if r: recs.append(r)
    print(sys.argv[1:], "NS S:", len(recs), "formula mismatches:", sum(1 for r in recs if r["W"] != r["F"]))
    if recs:
        mn = min(recs, key=lambda r: r["W"]); print("  min W", mn)
        mr = min(recs, key=lambda r: r["W"] / r["e"] ** 2); print("  min W/e^2", round(mr["W"] / mr["e"] ** 2, 3), mr)
if __name__ == "__main__":
    _main()
