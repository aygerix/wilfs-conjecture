"""Truncations of a leaf (lead, 2026-10-21). Every S with gcd(L(S)) = 1 is S_c = T u [c, inf) for the leaf
T = <L(S)> (Delgado Remark 5.15: leaves are exactly S = <L(S)>, i.e. r = 0) and c = c(S).
Test LEAF-MIN: W(S_c) >= W(T) for every valid truncation level c (c - 1 not in T, m < c <= c(T)).
Usage: python leaftrunc.py NS SEED MMAX"""
import sys, random
def wilf(Sset_upto, c, m):
    # S = T u [c, inf); Sset_upto: bytearray membership of T up to c + 2m
    g = sum(1 for x in range(c) if not Sset_upto[x])
    ell = c - g
    gens = 0
    for x in range(1, c + m):
        xin = Sset_upto[x] or x >= c
        if not xin: continue
        dec = any((Sset_upto[a] or a >= c) and (Sset_upto[x - a] or x - a >= c) for a in range(1, x // 2 + 1))
        if not dec: gens += 1
    return gens * ell - c, gens
NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED)
tests = fails = 0; worst = None
for _ in range(NS):
    m = rnd.randint(4, MMAX); k = rnd.randint(2, 5)
    G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 4]) * m), k))
    # T = <m, G>; membership up to a bound
    B = 40 * m * m // max(1, k) + 200
    T = bytearray(B); T[0] = 1
    for x in range(1, B):
        if (x >= m and T[x - m]) or any(g <= x and T[x - g] for g in G): T[x] = 1
    if not all(T[B - m - 1: B]): continue
    F = max(x for x in range(B) if not T[x]); cT = F + 1
    if cT + 3 * m > B: continue
    WT, eT = wilf(T, cT, m)
    for c in range(m + 1, cT):
        if T[c - 1]: continue
        Wc, ec = wilf(T, c, m); tests += 1
        if Wc < WT:
            fails += 1
            if fails <= 8: print("LEAF-MIN FAIL m=%d G=%s c=%d W(S_c)=%d e=%d   leaf c(T)=%d W(T)=%d e(T)=%d" % (m, G, c, Wc, ec, cT, WT, eT), flush=True)
print("truncations tested", tests, "LEAF-MIN failures", fails)
