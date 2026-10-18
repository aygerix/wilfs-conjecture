# Independent re-implementation of the finite part of THEOREM (two-face e = 4): for every (m, L3) and every feasible
# parameter tuple, one of the bounds A' (only if c > 3m; c <= 3m is Eliahou), B'', C, D gives W >= 0.
import sys
from math import comb
def xs(m, L):
    cap = m - L
    for ax in (0, 1):
        for x1 in range(0, L - ax + 1):
            t1 = x1*(x1 + 1)//2
            if t1 > cap: break
            for x2 in range(0, L - ax + 1):
                if t1 + x2*(x2 + 1)//2 > cap: break
                yield x1, x2, ax
def A_ok(m, L, x1, x2, ax):
    if 4*L > m: return False
    s = x1 + x2; tau = s + ax
    d = m*(m + 2*L - 2*s - comb(x1, 2) - comb(x2, 2) - ax*(L + 2)) + 3*comb(tau, 2)
    return 4*m*(m - 4*L) + 2*(m + 1)*L*(L - 1) + 4*max(0, d) >= 3*m*(m - 1)
def B_ok(m, L, x1, x2, ax):
    if m < 2*L: return False
    s = x1 + x2; tau = s + ax
    d = m*(m + L - 2*s - comb(x1, 2) - comb(x2, 2) - 2*ax) + 2*comb(tau, 2)
    return (L - 1)*(m + 1)*(m - 2*L) + 4*max(0, d) >= 3*m*(m - 1)
def C_ok(m, L, x1, x2, ax):
    s = x1 + x2; tau = s + ax
    return 2*tau + comb(x1, 2) + comb(x2, 2) + ax*s + min(x1, x2) <= m + 1
def D_ok(m, L):
    h = lambda H: (L - H)*(L - H - 1) if H < L else 0
    N = m - L
    for H1 in range(1, L + 1):
        for H2 in range(1, L + 1):
            if H1 + H2 > N: break
            G = m*(L - 1) - 2*L*(L - 1) + 2*h(H1) + 2*h(H2)
            if G < 0 or (m + 1)*G < 3*m*(m - 1): return False
    return True
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for m in range(lo, hi + 1):
    unc = []; unc_strict = []
    for L in range(2, m - 1):
        if D_ok(m, L): continue
        X = list(xs(m, L))
        if not all(A_ok(m, L, *x) or B_ok(m, L, *x) or C_ok(m, L, *x) for x in X): unc.append(L)
        if not (all(A_ok(m, L, *x) for x in X) or all(B_ok(m, L, *x) for x in X) or all(C_ok(m, L, *x) for x in X)):
            unc_strict.append(L)
    if unc or unc_strict: print('m', m, 'uncovered L3 (per-tuple):', unc, ' (single-bound):', unc_strict, flush=True)
print('done', lo, hi)
