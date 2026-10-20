r"""Phase walk of DEP-CARRY (lead, 2026-10-21). Label weights om~(lam) = omega(r^{-1}(lam)) at phase 0, f(rho) =
sum_t omega(t) r_rho(t) - d M'. Exact: f(rho) - f(rho-1) = m (d - om~(-rho)), sum_rho f = 0.  DEP-CARRY at phase rho
<=> f(rho) <= M' + m Dep.  Sufficient (ID): for every cyclic label interval J, sum_J (d - om~) <= (m-1)/2 + Dep.
Reports per S: DEP at conductor phase, DEP at every phase (max f), ID margin.  Usage: python idisc.py NS SEED MMIN MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
def analyse(m, gens, M, c):
    N = len(gens); D = list(M); Ds = set(D); delta = [g % m for g in gens]
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    om = {x: 0 for x in D}
    for b in range(N):
        for x in D:
            if up(x, b) not in Ds: om[x] += x[b] + 1
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    dep = sum(v for x, v in om.items() if x not in mx)
    lab0 = {x: sum(a * b for a, b in zip(x, delta)) % m for x in D}
    wt = [0] * m
    for x in D: wt[lab0[x]] += om[x]
    Mp = m * (m - 1) // 2
    f = [sum(wt[l] * ((l + rho) % m) for l in range(m)) - N * Mp for rho in range(m)]
    rho0 = (-c) % m
    s = [N - wt[l] for l in range(m)]
    best = 0
    for i in range(m):   # max cyclic interval sum
        acc = 0
        for k in range(m):
            acc += s[(i + k) % m]; best = max(best, acc)
    return f[rho0], max(f), Mp + m * dep, best, (m - 1) / 2 + dep, dep
if __name__ == '__main__':
    NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
    cnt = 0; fc = fa = fi = 0; wc = wa = wi = None; byop = [0, 0]
    while cnt < NS:
        m = rnd.randint(MMIN, MMAX); c0 = rnd.randint(m + 1, 9 * m)
        G = sorted(rnd.sample(range(m + 1, c0 + m), rnd.randint(2, min(12, c0 - 2))))
        R = build(m, G)
        if R is None: continue
        c, gens, M = R; N = len(gens)
        if N < 2 or c <= m: continue
        cnt += 1; op = int(3 * (N + 1) < m and c > 4 * m); byop[op] += 1
        fc0, fmax, rhs, idv, idr, dep = analyse(m, gens, M, c)
        assert fc0 <= rhs, (m, gens, c)
        if fmax > rhs:
            fa += 1
            if wa is None or (fmax - rhs) / m / m > wa[0]: wa = ((fmax - rhs) / m / m, m, gens, c, op)
        if idv > idr:
            fi += 1
            if wi is None or (idv - idr) / m > wi[0]: wi = ((idv - idr) / m, m, gens, c, op)
    print("S %d (open %d): DEP at conductor phase fails 0; DEP at some phase fails %d worst %s; ID fails %d worst %s" % (cnt, byop[1], fa, wa, fi, wi))
    print("failing tile phases:", analyse(19, [39, 41, 50, 52, 53], build(19, [39, 41, 50, 52, 53])[2], 88))
