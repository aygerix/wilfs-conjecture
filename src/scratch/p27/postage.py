r"""Postage-stamp fakes against TOV (lead, 2026-10-20).  X = {0} u X+ with X+ + X+ u X+ u {0} covering [0, n]
(a 2-basis found by search).  B = (H + X) u {xb}, m = 2H + xb - 1, so the window [m+1, m+n+1) = 2H + xb + [0, n] is
covered by the 3-sums (H+x)+(H+x')+xb.  Evaluates TOV and W_eff on the resulting local fakes (C1),(C3), and whether
C2w ([h, 2h) covered) / (C2) hold.  usage: postage k"""
import sys, itertools
sys.path.insert(0, '.')
def best_basis(k):
    best = (0, None)
    def n_of(X):
        S = set(x + y for x in X for y in X); n = 0
        while n + 1 in S: n += 1
        return n
    # greedy-random search over k-1 positive elements (exhaustive for small k)
    lim = 3 * k * k
    for comb in itertools.combinations(range(1, lim), k - 1):
        if comb[0] != 1: break
        X = (0,) + comb; n = n_of(X)
        if n > best[0]: best = (n, X)
    return best
k = int(sys.argv[1])
n, X = best_basis(k); print("basis k =", k, "X =", X, "covers [0,", n, "]")
from tov import go
import tov
for H in (n + 1, n + 2, 2 * n):
    for xb in range(2 * n + 2, 8 * n, max(1, n // 3)):
        B = sorted(set(H + x for x in X) | {xb}); m = 2 * H + xb - 1
        if max(B) >= m: continue
        st = dict(ovf_fail=0, red_fail=0, min={}, neg={})
        go(m, B, st)
        if st["min"]: print("H", H, "xb", xb, "m", m, "e", len(B) + 1, {kk: st["min"][kk][0:1] + st["min"][kk][3:4] for kk in st["min"]})
