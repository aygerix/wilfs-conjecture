r"""Independent check of one S (lead, 2026-10-20): brute-force S membership by DP up to a bound, Apery set,
levels, orders, X(u), lambda(u,b), T_c, XDEAD, XWILF, DEAD, W.  usage: verify_xd.py gens..."""
import sys
G = list(map(int, sys.argv[1:])); m = min(G); N = 60 * max(G)
inS = [False] * (N + 1); inS[0] = True
for n in range(1, N + 1): inS[n] = any(n >= g and inS[n - g] for g in G)
F = max(n for n in range(N + 1) if not inS[n]); c = F + 1
Ap = [min(n for n in range(r, N + 1, m) if inS[n]) for r in range(m)]
apset = set(Ap)
gens = sorted(n for n in apset if n > 0 and not any(0 < a < n and (n - a) in apset and (n - a) > 0 for a in apset))
e = len(gens) + 1
o = {}
for v in sorted(Ap): o[v] = 0 if v == 0 else max(o[v - g] + 1 for g in gens if v - g >= 0 and (v - g) in apset)
g_ = sum(v // m for v in Ap); ell = c - g_; W = e * ell - c
Tc = sum(v // m - o[v] for v in Ap)
lam = {(u, b): max(j for j in range(m + 1) if all((u + i * b) in apset for i in range(j + 1))) for u in Ap for b in gens}
X = {u: max((z - u) // m for z in Ap if (z - u) >= 0 and (z - u) in apset) for u in Ap}
Lu = {u: sum(1 for j in range(0, N // m) if u + j * m < c) for u in Ap}
assert sum(Lu.values()) == ell
XD = sum(X[u] - lam[u, b] for u in Ap for b in gens) - Tc
DEAD = sum(Lu[u] - lam[u, b] for u in Ap for b in gens) - Tc
mu = {(z, b): max(j for j in range(m + 1) if (z - j * b) >= 0 and inS[z - j * b]) for z in Ap for b in gens}
Lam = sum(mu.values()); O = sum(o.values())
print(dict(m=m, gens=gens, e=e, c=c, g=g_, ell=ell, W=W, Tc=Tc, sumX=sum(X.values()), XWILF=(e - 1) * sum(X.values()) - g_,
           XDEAD=XD, DEAD_slots_minus_Tc=DEAD, W_minus_LamO=W - (Lam - O)))
