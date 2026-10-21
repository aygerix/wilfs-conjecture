r"""SUPP-WILF with the Apery set of any minimal generator n (lead, 2026-10-21).  For n in the minimal generators, tile
D_n ⊂ N^{e-1} (lex-least factorizations over the other generators), labels r = (w - c) mod n, and
    nW = e*N' - sum_{(x,b)} (w(t_b x) - c)  (exact, N' = n(n-1)/2),
    w(t) - c <= r(t) always;  <= r(t) - n if t has a witness a (t + e_a in D) with g_a >= n or r(t) >= n - g_a.
So W >= Dep'_n - kappa0_n + N_n with Dep'_n = #{(x,b): t_b(x) has such a witness}.  Asserts the exact identity and
the bound against brute-force W; reports, per n, Dep'_n - Ssupp_n and Dep'_n - kappa0_n + N_n.  Usage: python multin.py g1 .. ge"""
import sys
G = sorted(map(int, sys.argv[1:]))
T = 30 * max(G) + 100
S = bytearray(T); S[0] = 1
for x in range(1, T): S[x] = any(x >= g and S[x - g] for g in G)
gaps = [x for x in range(T) if not S[x]]; c = max(gaps) + 1; g = len(gaps); e = len(G); W = e * (c - g) - c
print("S=%s c=%d g=%d e=%d W=%d" % (G, c, g, e, W))
for n in G:
    oth = [x for x in G if x != n]; d = len(oth)
    ap = sorted(min(x for x in range(T) if S[x] and x % n == i) for i in range(n))
    fac = {0: (0,) * d}
    for x in ap[1:]:
        best = None
        for i, gi in enumerate(oth):
            if x - gi in fac:
                a = list(fac[x - gi]); a[i] += 1; a = tuple(a)
                if best is None or a[::-1] < best[::-1]: best = a
        fac[x] = best
    D = {a: x for x, a in fac.items()}; Ds = set(D)
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(d))
    r = {x: (D[x] - c) % n for x in D}
    lhs = 0; dep = 0; Nn = 0; tot = 0
    for b in range(d):
        for x in D:
            y = x; k = 0
            while up(y, b) in Ds: y = up(y, b); k += 1
            lhs += D[y] - c
            wit = [a for a in range(d) if up(y, a) in Ds and (oth[a] >= n or r[y] >= n - oth[a])]
            if wit: dep += 1
            if k and r[x] > r[y]: Nn += 1
    Np = n * (n - 1) // 2
    assert n * W == e * Np - lhs, (n, n * W, e * Np - lhs)
    delta = [x % n for x in oth]
    k0 = sum(sum((x[a] * delta[a]) % n for a in range(d)) // n for x in D)
    ss = sum(max(0, sum(1 for t in x if t) - 1) for x in D)
    assert W >= dep - k0 + Nn
    print("  n=%3d d=%d h=%d: Dep'=%d Ssupp=%d kappa0=%d N=%d  bound Dep'-Ss=%d  Dep'-k0+N=%d" % (n, d, max(sum(x) for x in D), dep, ss, k0, Nn, dep - ss, dep - k0 + Nn))
