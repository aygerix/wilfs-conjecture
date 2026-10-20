# B*, B_1, B_h on structured families (lead, 2026-10-20). W = e - h + Lam + sum_x J(x)k(x) - S_h (identity);
# T1(p) <=> sum J k >= S_p.  B_h = e - h + Lam (T1 at p*), B_1 = B_h - S_h (T1 at p = 1), B* = B_h + max_p S_p - S_h.
import sys, random
sys.path.insert(0, '.')
from lowfam import apery
def full(m, gens):
    w = apery(m, gens); W = set(w)
    inS = lambda v: v >= 0 and w[v % m] <= v
    Aps = sorted(w)
    P = [x for x in Aps if x and not any(y and (x - y) in W and y in W for y in Aps if 0 < y < x)]
    d = len(P); e = d + 1; M = max(w); c = M - m + 1; q = -(-c // m); h = c - (q - 1) * m
    lam = lambda v: (M - v) // m
    def nu(a, x):
        k = 0
        while inS(x - (k + 1) * a): k += 1
        return k
    J = {}; Lam = 0
    for x in w:
        s = 0
        for a in P:
            if (x + a) not in W: s += nu(a, x) + 1
            t = x
            while (t + a) in W: t += a
            Lam += lam(t)
        J[x] = s - e
    Sp = [0] * (m + 1); S = 0
    for p in range(1, m + 1):
        Sp[p] = S
        if p < m: S += J[w[p]]
    SJk = sum(J[x] * (x // m) for x in w)
    ell = sum(lam(x) for x in w); Wv = e * ell - c
    assert Wv == e - h + Lam + SJk - Sp[h], (m, gens)
    Bh = e - h + Lam; B1 = Bh - Sp[h]; Bs = Bh + max(Sp[1:]) - Sp[h]
    return dict(m=m, e=e, q=q, h=h, Lam=Lam, W=Wv, Bh=Bh, B1=B1, Bstar=Bs, T1all=SJk >= max(Sp[1:]))
if __name__ == "__main__":
    random.seed(7); bad = 0; n = 0
    for it in range(int(sys.argv[1])):
        m = random.randint(8, 70); mode = it % 3
        if mode == 0: B = random.sample(range(1, m), random.randint(2, max(2, m // 5))); k = random.randint(1, 6); gens = [m] + [k * m + b for b in B]
        elif mode == 1: gens = [m] + random.sample(range(m + 1, 2 * m), random.randint(2, max(2, m // 4)))
        else: gens = [m] + random.sample(range(m + 1, 5 * m), random.randint(2, 6))
        r = full(m, gens)
        if r['e'] < 3: continue
        n += 1
        if not r['T1all']: print("T1-ALL FAIL", gens, r)
        if max(r['Bh'], r['B1']) < 0 or r['Bstar'] < 0:
            bad += 1; print("OMEGA FAIL", gens, r)
    print("tested", n, "OMEGA2/B* failures", bad)
