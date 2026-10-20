# FACE-WILF test at depth four (lead, 2026-10-20). Structured excess-regime S: high B_3/Sidon A-offsets in (h/2, h),
# B/C completions, truncation S u [3m+h, oo) (as in codex P14 structured.c, re-implemented). For q = 4 checks
#   Lam >= sum_{p in F} tau(p)                  (PROVED; F = distinct pair faces of critical cubics)
#   FACE-WILF:  R <= rho + sum_{p in F} tau(p) + Z     (sufficient for Wilf)
import random, heapq, sys
def sums_unique(x, r):
    import itertools
    s = [sum(c) for c in itertools.combinations_with_replacement(x, r)]
    return len(s) == len(set(s))
def build(m, h, T, Bs, Cs):
    cap = 3 * m + h; gens = [m] + [m + t for t in T] + Bs + Cs
    dist = {0: 0}; hq = [(0, 0)]
    while hq:
        d0, i = heapq.heappop(hq)
        if dist.get(i) != d0: continue
        for n in gens:
            j = (i + n) % m; nd = d0 + n
            if nd >= cap + m: continue
            if j not in dist or nd < dist[j]: dist[j] = nd; heapq.heappush(hq, (nd, j))
    w = []
    for i in range(m):
        tail = cap + ((i - cap) % m)
        w.append(min(dist.get(i, tail), tail))
    return w
def analyze(m, w):
    M = max(w); c = M - m + 1
    if not (3 * m < c <= 4 * m): return None
    q = 4; rho = 4 * m - c; aps = set(w)
    inS = lambda v: v >= 0 and w[v % m] <= v
    P = sorted(x for x in aps if x and not any(inS(y) and inS(x - y) for y in aps if 0 < y < x and y != x - y or (0 < y < x and y == x - y and inS(y))))
    # minimal generators: Apery elements not a sum of two nonzero Apery elements
    P = sorted(x for x in aps if x and not any(y != 0 and (x - y) in aps and x - y != 0 for y in aps if y < x))
    d = len(P); e = d + 1
    lam = {x: (M - x) // m for x in w}
    def nu(x, n):
        k = 0
        while inS(x - (k + 1) * n): k += 1
        return k
    K = {}; Lam = 0; Z = 0; R = 0
    U = {}
    for x in w:
        k = 4 - lam[x]; U[x] = []
        for n in P:
            j = nu(x, n)
            if j: U[x].append(n); k -= j * ((M - (x - n)) // m - lam[x])
            if (x + n) not in aps: Lam += (j + 1) * lam[x]
        K[x] = k
        if k < 0: Z -= k
        if k == 1: R += 1
    crit = [x for x in w if K[x] == 1 and lam[x] == 0 and sum(nu(x, n) for n in P) == 3]
    F = set()
    for x in crit:
        for n in U[x]: F.add(x - n)
    tauF = sum(sum(1 for n in P if (p + n) not in aps) for p in F)
    g = sum(x // m for x in w); W = e * (c - g) - c
    assert W == rho + Lam + Z - R
    assert Lam >= tauF
    return dict(m=m, e=e, h=c - 3 * m, rho=rho, W=W, R=R, crit=len(crit), F=len(F), tauF=tauF, Z=Z, Lam=Lam,
                slack=rho + tauF + Z - R)
def main():
    random.seed(int(sys.argv[1])); N = int(sys.argv[2])
    worst = None; cnt = 0; fails = 0; exc = 0
    for it in range(N):
        m = random.choice([61, 101, 151, 211]); h = random.randint(8, m - 1); k = random.randint(3, 9)
        mode = random.randint(0, 1); T = []
        for _ in range(3000):
            if len(T) >= k: break
            t = random.randint((h + 1) // 2, h - 1)
            if t in T: continue
            if sums_unique(T + [t], 3 if mode == 0 else 2): T.append(t)
        if len(T) < 3: continue
        nb = random.randint(0, 8); nc = random.randint(0, 4)
        Bs = [m + h + random.randrange(m) for _ in range(nb)]; Cs = [2 * m + h + random.randrange(m) for _ in range(nc)]
        w = build(m, h, T, Bs, Cs)
        r = analyze(m, w)
        if r is None: continue
        cnt += 1
        if r['crit'] > r['F']: exc += 1
        if r['slack'] < 0: fails += 1; print("FACEWILF FAIL", r, T, Bs, Cs)
        if r['crit'] > r['F'] and (worst is None or r['slack'] < worst[0]['slack']): worst = (r, T, Bs, Cs)
    print("depth-four S:", cnt, " with crit > |F|:", exc, " FACE-WILF failures:", fails)
    print("worst (excess regime):", worst)

if __name__ == "__main__":
    main()
