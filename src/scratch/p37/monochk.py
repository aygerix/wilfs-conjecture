# independent check of a MONO*-Q5 counterexample (membership DP and explicit 3-fold sumset; no code shared with q5d)
import sys
G = list(map(int, sys.argv[1:])); m = min(G); A = sorted(g - m for g in G if g != m); e = len(G)
N = 10 * m
inS = [False] * (N + 1); inS[0] = True
for x in range(1, N + 1): inS[x] = any(x >= g and inS[x - g] for g in G)
gaps = [x for x in range(N + 1) if not inS[x]]; c = gaps[-1] + 1; W = e * (c - len(gaps)) - c
A0 = [0] + A
S3 = sorted({x + y + z for x in A0 for y in A0 for z in A0})
U = [False] * (N + 1)
for t in S3:
    for z in range(t, N + 1, m): U[z] = True
ug = [x for x in range(N + 1) if not U[x]]; cU = ug[-1] + 1; lU = cU - len(ug); WeU = e * lU - cU
inT = [False] * (N + 1); inT[0] = True
gens = [m] + A
for x in range(1, N + 1): inT[x] = any(x >= g and inT[x - g] for g in gens)
tg = [x for x in range(N + 1) if not inT[x]]; cT = tg[-1] + 1; lT = cT - len(tg)
Tel = [x for x in range(1, cT + 2 * m) if inT[x]]; Ts = set(Tel)
eT = sum(1 for x in Tel if not any((x - y) in Ts for y in Tel if y <= x // 2)); WT = eT * lT - cT
ap = {}
for x in range(N + 1):
    if inS[x] and (x < m or not inS[x - m]): ap.setdefault(x % m, x)
r = max(ap, key=lambda s: ap[s])
print("S=%s m=%d e=%d c=%d W=%d q=%d r=%d | U=3A'+mN: c=%d l=%d WeU=%d | T=<m,A>: c=%d l=%d e(T)=%d W(T)=%d | WeU-W(T)=%d | T\\U=%s" % (
      G, m, e, c, W, ap[r] // m, r, cU, lU, WeU, cT, lT, eT, WT, WeU - WT, [x for x in range(N + 1) if inT[x] and not U[x]]))
