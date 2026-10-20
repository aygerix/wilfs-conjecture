r"""Conjecture DEAD (lead, 2026-10-20): W(S) >= Lambda - O, where for w in Ap(S, m)
   mu_b(w) = max{j : w - j g_b in S},  o(w) = max length of a factorisation of w (m unused),
   Lambda = sum_w sum_b mu_b(w),  O = sum_w o(w).   (Lambda >= O always.)
Equivalent to: #power tokens whose target is not in Ap >= e * T_c.
usage: dead.py gens... | rnd mlo mhi kmin kmax N seed [p18|hiK] | ivl mlo mhi kmax | ap mlo mhi kmax dmax"""
import sys, random, heapq
def info(gens):
    m = min(gens); G = sorted(set(gens))
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in G:
            if x == m: continue
            v = d0 + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    c = max(w) - m + 1
    aps = set(w); srt = sorted(w)
    gen = [v for v in srt[1:] if not any((v - u) in aps for u in srt[1:] if u < v and (v - u) in aps)]
    e = len(gen) + 1
    if c <= 0: return None
    o = {0: 0}
    for v in srt[1:]: o[v] = max(o[v - g] + 1 for g in gen if v - g >= 0 and (v - g) in aps)
    Lam = 0
    for v in w:
        for g in gen:
            j = 0
            while v - (j + 1) * g >= 0 and (v - (j + 1) * g) in aps: j += 1
            Lam += j
    O = sum(o.values()); gg = sum(v // m for v in w); W = e * (c - gg) - c
    return dict(m=m, e=e, c=c, g=gg, W=W, Lam=Lam, O=O, D=W - (Lam - O), gens=[m] + gen)
def run(it, label):
    n = bad = 0; worst = None; ratio = None
    for gens in it:
        r = info(gens)
        if r is None: continue
        n += 1; bad += r["D"] < 0
        if worst is None or r["D"] < worst["D"]: worst = r
    print(label, "S", n, "DEAD fails", bad, "min W-(Lam-O)", worst["D"] if worst else None)
    print("   worst", worst)
if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "rnd":
        mlo, mhi, kmin, kmax, N, seed = map(int, a[1:7]); random.seed(seed); mode = a[7] if len(a) > 7 else "hi4"
        def it():
            for _ in range(N):
                m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); hi = 2 * m if mode == "p18" else int(mode[2:]) * m
                if hi - m - 1 >= k: yield [m] + random.sample(range(m + 1, hi), k)
        run(it(), a)
    elif a[0] == "ivl":
        mlo, mhi, kmax = map(int, a[1:4])
        run(([m] + list(range(m + 1, m + k + 1)) for m in range(mlo, mhi + 1) for k in range(1, min(kmax, m - 1) + 1)), a)
    elif a[0] == "ap":
        mlo, mhi, kmax, dmax = map(int, a[1:5])
        run(([m] + [m + d * i for i in range(1, k + 1)] for m in range(mlo, mhi + 1) for k in range(1, kmax + 1) for d in range(1, dmax + 1)), a)
    else:
        print(info(list(map(int, a))))
