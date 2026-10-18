# EXHAUSTIVE: all q*-free cylindrical non-two-face sets D = {x2 < h(x1), x3 < f(x1), x3 < g(x2)} with |D| <= M.
# h: [0,L1) -> [1,L2] nonincr, h(0) = L2, h(1) >= 2;  f: [0,L1) -> [1,L3], f(0) = L3, f(1) >= 2;  g: [0,L2) -> [1,L3],
# g(0) = L3, g(1) >= 2.  Reports per m: count, min H-(m-1), #fails.   usage: cyl_exhaust.py M
import sys
sys.path.insert(0, 'src/scratch')
from heightH import H_of
def stairs(L, top, first_min):
    """nonincreasing sequences of length L, s[0] = top, s[1] >= first_min, entries >= 1."""
    def rec(prefix):
        if len(prefix) == L: yield tuple(prefix); return
        lo = first_min if len(prefix) == 1 else 1
        for v in range(min(prefix[-1], top), lo - 1, -1): yield from rec(prefix + [v])
    if L < 2 or top < first_min: return
    yield from rec([top])
M = int(sys.argv[1])
res = {}
for L1 in range(2, M):
    for L2 in range(2, M):
        if L1 + L2 + 2 > M: break
        for L3 in range(2, M):
            if L1 + L2 + L3 + 4 > M: break      # D contains 3 axes + 3 cells e_a+e_b
            for h in stairs(L1, L2, 2):
                s3 = sum(h)
                if s3 + L3 + 2 > M: continue
                for f in stairs(L1, L3, 2):
                    for g in stairs(L2, L3, 2):
                        m = sum(min(f[i], g[j]) for i in range(L1) for j in range(h[i]))
                        if m > M: continue
                        D = {(i, j, k) for i in range(L1) for j in range(h[i]) for k in range(min(f[i], g[j]))}
                        v = H_of(D) - (m - 1)
                        c, mn, fl, arg = res.get(m, (0, None, 0, None))
                        res[m] = (c + 1, v if mn is None else min(mn, v), fl + (v < 0), arg if (mn is not None and mn <= v) else (h, f, g))
for m in sorted(res): print(m, res[m], flush=True)
