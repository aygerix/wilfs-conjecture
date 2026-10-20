r"""Layer inequalities (lead, 2026-10-20).  For a numerical semigroup S with multiplicity m and embedding dimension e,
s_j = |S n [jm, (j+1)m)|.  LAYER(j): j * s_j <= e * (s_0 + ... + s_{j-1}).  Tight (equality, all j) for free P18 sets.
Proved for P18 at j = 3 (Theorem Q3); j = 1, 2 trivial for P18.
usage: layer.py [j3] p18 kmin kmax mlo mhi N seed | gen mlo mhi nmin nmax hi N seed  (generators random in (m, hi*m))"""
import sys, random, heapq
def apery(gens):
    m = min(gens); w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in gens:
            if x == m: continue
            v = d0 + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    return None if any(x is None for x in w) else w
def check(gens):
    w = apery(gens)
    if w is None: return None
    m = min(gens); aps = set(w); srt = sorted(w)
    e = 1 + sum(1 for v in srt[1:] if not any((v - u) in aps for u in srt[1:] if u < v))
    lv = [x // m for x in w]; q = max(lv)
    s = [sum(1 for x in lv if x <= j) for j in range(q + 2)]
    worst = None
    if len(a3only) and q >= 3: return dict(m=m, e=e, q=q, s=s, worst=(e * sum(s[:3]) - 3 * s[3], 3), gens=sorted(gens))
    for j in range(1, q + 2):
        sl = e * sum(s[:j]) - j * s[j]
        if worst is None or sl < worst[0]: worst = (sl, j)
    return dict(m=m, e=e, q=q, s=s, worst=worst, gens=sorted(gens))
a3only = []
if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "j3": a3only.append(1); a = a[1:]; random.seed(int(a[-1])); n = bad = 0; mn = None; byj = {}
    if a[0] == "p18":
        kmin, kmax, mlo, mhi, N = map(int, a[1:6])
        gen = lambda: (lambda m: [m] + [m + b for b in random.sample(range(1, m), random.randint(kmin, min(kmax, m - 1)))])(random.randint(mlo, mhi))
    else:
        mlo, mhi, nmin, nmax, hi, N = map(int, a[1:7])
        gen = lambda: (lambda m: [m] + random.sample(range(m + 1, hi * m), random.randint(nmin, nmax)))(random.randint(mlo, mhi))
    for _ in range(N):
        r = check(gen())
        if r is None: continue
        n += 1; sl, j = r["worst"]; bad += sl < 0
        b = byj.setdefault(j, [0, 0]); b[0] += 1; b[1] += sl < 0
        if mn is None or sl < mn["worst"][0]: mn = r
    print(a, "S", n, "LAYER fails", bad, "worst-j histogram", byj, "\n  min", mn)
