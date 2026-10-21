r"""Level form of MaxCL at sigma = phi(0) (lead, 2026-10-20). For a tile (D, delta), v(x) = x.delta (canonical lift,
delta_a = <p_a> in [1, m-1]), U_j = {x : v(x) >= j m}, gamma_j = sum_b |B_b(U_j)| - |U_j| (B_b = cells outside U whose
b-column meets U), Lnm = sum over non-maximal column tops t of |C| r(t).  MaxCL(0) <=> sum_j gamma_j + Lnm/m >= 0.
Reports the sign pattern of gamma_j on lex Apery tiles of random S (all units u).  Usage: python levels0.py NS SEED MMAX"""
import sys, random
from math import gcd
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from tile import build
def levels(m, D, delta):
    N = len(delta); Ds = set(D)
    v = {x: sum(a * b for a, b in zip(x, delta)) for x in D}
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    top = {}
    for b in range(N):
        for x in D:
            y = x
            while up(y, b) in Ds: y = up(y, b)
            top[(x, b)] = y
    Lnm = 0
    for b in range(N):
        for x in D:
            if x[b] == 0:
                t = top[(x, b)]
                if t not in mx: Lnm += (t[b] + 1) * (v[t] % m)
    J = max(v.values()) // m; gam = []
    for j in range(1, J + 1):
        U = {x for x in D if v[x] >= j * m}
        sh = sum(1 for b in range(N) for x in D if x not in U and top[(x, b)] in U)
        gam.append(sh - len(U))
    return gam, Fr(Lnm, m)
if __name__ == '__main__':
    NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED)
    cnt = 0; neg1 = 0; negany = 0; worst = None; fail = 0; pat = {}
    while cnt < NS:
        m = rnd.randint(8, MMAX); G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 4]) * m), rnd.randint(2, min(7, m - 2))))
        R = build(m, G)
        if R is None: continue
        c, gens, M = R; N = len(gens); D = list(M)
        if N < 2: continue
        for u in [u for u in range(1, m) if gcd(u, m) == 1][:6]:
            delta = [(u * g) % m for g in gens]
            gam, L = levels(m, D, delta); cnt += 1
            tot = sum(gam) + L
            if tot < 0: fail += 1; print("FAIL", m, gens, u, gam, L, flush=True)
            if gam and gam[0] < 0: neg1 += 1
            if any(g < 0 for g in gam): negany += 1
            key = tuple(1 if g > 0 else (0 if g == 0 else -1) for g in gam)
            pat[key] = pat.get(key, 0) + 1
            nrm = float(tot) / m
            if worst is None or nrm < worst[0]: worst = (nrm, m, gens, u, gam, float(L))
    print("instances %d  MaxCL(0) fails %d  gamma_1<0: %d  some gamma_j<0: %d" % (cnt, fail, neg1, negany))
    print("worst (sum gamma + Lnm/m)/m:", worst)
    for k, v in sorted(pat.items(), key=lambda t: -t[1])[:15]: print("  pattern", k, v)
