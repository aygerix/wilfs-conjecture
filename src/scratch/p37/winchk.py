# independent check of a WINDOW counterexample: membership DP, no Apery code from q5d
import sys
G = list(map(int, sys.argv[1:])); m = min(G); N = 8 * m
inS = [False] * (N + 1); inS[0] = True
for x in range(1, N + 1): inS[x] = any(x >= g and inS[x - g] for g in G)
gaps = [x for x in range(N + 1) if not inS[x]]; c = gaps[-1] + 1; g = len(gaps)
els = [x for x in range(1, 3 * max(G)) if inS[x]]; Ss = set(els)
mg = [x for x in els if x <= max(G) and not any((x - y) in Ss for y in els if 0 < y < x)]
e = len(mg); ell = c - g; W = e * ell - c
ap = {}
for x in range(N + 1):
    if inS[x] and (x - m < 0 or not inS[x - m]): ap.setdefault(x % m, x)
assert len(ap) == m
r = max(ap, key=lambda s: ap[s]); q = ap[r] // m
# factorization lengths of Apery elements (all factorizations over G \ {m})
H = [g_ for g_ in G if g_ != m]
def lens(x, memo={}):
    if x == 0: return {0}
    if x in memo: return memo[x]
    out = set()
    for h in H:
        if x - h >= 0 and inS[x - h]:
            for L in lens(x - h): out.add(L + 1)
    memo[x] = out; return out
hmin = {s: min(lens(ap[s])) for s in ap}; hmax = {s: max(lens(ap[s])) for s in ap}
sig = {s: ap[s] - m * hmin[s] for s in ap}
X = sorted(sig[s] for s in ap if sig[s] <= m + r); Y = [s for s in ap if sig[s] <= r]
print("G=%s m=%d e=%d c=%d g=%d ell=%d W=%d q=%d r=%d maxh=%d" % (mg, m, e, c, g, ell, W, q, r, max(hmax.values())))
print("X(sigma<=m+r)=%s |X|=%d e|X|=%d m+r+1=%d |Y|=%d e(|X|+|Y|)=%d" % (X, len(X), e * len(X), m + r + 1, len(Y), e * (len(X) + len(Y))))
print("sigma by residue:", {s: (hmin[s], sig[s]) for s in sorted(ap)})
