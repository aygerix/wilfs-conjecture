# verifyF0: independent check of an F0 example (brute force, no Dijkstra): enumerate S = <m, m+A> up to 7m by
# dynamic programming over values, recording ALL factorization lengths of every element; then Apery set, height,
# q, conductor, genus, W; T = <m, A> and U = 3A' + mN directly as sets; c_T, U cap [0,c_T), P1, Qa, theta.
import sys
m = int(sys.argv[1]); A = list(map(int, sys.argv[2].split(','))); e = len(A) + 1; mu = min(A)
G = [m] + [m + a for a in A]; LIM = 7 * m
lens = [set() for _ in range(LIM)]; lens[0].add(0)
for v in range(1, LIM):
    for g in G:
        if g <= v and lens[v - g]: lens[v] |= {k + 1 for k in lens[v - g]}
inS = [bool(x) for x in lens]
ap = [min(v for v in range(s, LIM, m) if inS[v]) for s in range(m)]
# lengths counted in generators m+a only (an Apery element has no factorization using m)
assert all(not inS[w - m] for w in ap if w >= m)
height = max(max(lens[w]) for w in ap); q = max(ap) // m
c = max(ap) - m + 1; g = sum(1 for v in range(c) if not inS[v]); W = e * (c - g) - c
inT = [False] * LIM; inT[0] = True
for v in range(1, LIM): inT[v] = any(x <= v and inT[v - x] for x in [m] + A)
cT = max(v for v in range(LIM) if not inT[v]) + 1
Ap3 = {0}
for _ in range(3): Ap3 = Ap3 | {x + a for x in Ap3 for a in A}
inU = [any((v - k * m) in Ap3 for k in range(v // m + 1)) for v in range(LIM)]
Ulo = sum(1 for v in range(cT) if inU[v]); P1 = e * Ulo - cT
TmU = [v for v in range(LIM) if inT[v] and not inU[v]]
lmu = -(-cT // mu); th = mu * lmu - cT
Umu = sum(1 for v in range(0, cT, mu) if inU[v]); Up = sum(1 for v in range(cT) if v % mu and inU[v])
hlo_mu = sum(1 for v in range(0, cT, mu) if inT[v] and not inU[v])
Qa = (e - mu) * Umu + e * Up - mu * hlo_mu
print(f"m={m} A={A} e={e}: height={height} q={q} (Q5 needs height<=3, q=5; level 1: all a<m: {max(A)<m})")
print(f"  c(S)={c} g(S)={g} W(S)={W}; c_T={cT}; U cap [0,c_T)={[v for v in range(cT) if inU[v]]}; P1={P1}; Qa={Qa} theta={th}")
print(f"  T minus U = {TmU}")
