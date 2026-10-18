# Verify every intermediate inequality of the two-face e = 4 proof on actual semigroups (not just W >= 0).
# For each two-face S: actual x1, x2, xax, tau, P2, H1, H2, L3, M, p_c, Def2D, Def2D' and
#   (I)  3mW + 3m(m-1) == (m - 4L3) M + 4 SumAx + 4 Def2D == m M + 4 Def2D' - 2 p_c L3 (L3-1)
#   (A') Def2D  >= m(2m + L3 - sum_X R) + sum_X R(u) delta_u >= m(m + 2L3 - 2(x1+x2) - C(x1,2) - C(x2,2) - xax(L3+2)) + 3C(tau,2)
#   (B'') Def2D' >= m(m + L3 - 2(x1+x2) - C(x1,2) - C(x2,2) - 2xax) + 2 C(tau,2)
#   (D)  Def2D' >= p_c [C(L3-H1,2) + C(L3-H2,2)]
#   (C)  P2 <= C(x1,2) + C(x2,2) + xax(x1+x2) + min(x1,x2);  tau = x1+x2+xax
#   area x1(x1+1)/2 + x2(x2+1)/2 <= m - L3;  x_i <= L3 - xax
import sys, itertools, random
from math import gcd, comb
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from cl import factorizations_down_set
def check(s):
    p, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}; D = set(cells); d = 3; m = s.m; c = s.c
    faces = [(a, b) for a in range(d) for b in range(a + 1, d) if tuple(int(i in (a, b)) for i in range(d)) not in D]
    if not faces: return None
    a, b = faces[0]; cx = 3 - a - b
    M = max(cells.values()); assert M == c + m - 1
    L3 = max(x[cx] for x in D) + 1; pc = p[cx]
    def e(i, k=1): return tuple(k if j == i else 0 for j in range(3))
    def add(x, y): return tuple(u + v for u, v in zip(x, y))
    def top(x, i):
        while add(x, e(i)) in D: x = add(x, e(i))
        return x
    runs = []   # (length, end, is_axis_column)
    for k in range(L3):
        for dr in (a, b):
            t = top(e(cx, k), dr); runs.append((t[dr] + 1, t, False))
    for x in D:
        if x[cx] == 0:
            t = top(x, cx); runs.append((t[cx] + 1, t, x == (0, 0, 0)))
    assert sum(L for L, t, ax in runs) == 2*m + L3
    Def2 = sum(L*(M - cells[t]) for L, t, ax in runs); Def2p = sum(L*(M - cells[t]) for L, t, ax in runs if not ax)
    SumAx = pc*L3*(L3 - 1)//2
    W = s.W if isinstance(s.W, int) else s.W()
    lhs = 3*m*W + 3*m*(m - 1)
    assert lhs == (m - 4*L3)*M + 4*SumAx + 4*Def2 == m*M + 4*Def2p - 2*pc*L3*(L3 - 1)
    X = [x for x in D if cells[x] >= c]
    axt = e(cx, L3 - 1); xax = int(axt in X)
    X1 = [x for x in X if x[a] > 0]; X2 = [x for x in X if x[b] > 0]
    x1, x2 = len(X1), len(X2); tau = len(X); assert tau == x1 + x2 + xax
    assert x1*(x1 + 1)//2 + x2*(x2 + 1)//2 <= m - L3 and x1 <= L3 - xax and x2 <= L3 - xax
    P2 = sum(1 for u, v in itertools.combinations(X, 2) if sum(1 for i in range(3) if u[i] != v[i]) == 2)
    assert P2 <= comb(x1, 2) + comb(x2, 2) + xax*(x1 + x2) + min(x1, x2)
    # run-length sums R(u) and the A', B'' lower bounds
    R = {u: sum(L for L, t, ax in runs if t == u) for u in X}; Rp = {u: sum(L for L, t, ax in runs if t == u and not ax) for u in X}
    for u in X:
        assert R[u] == (sum(u) + 2 if u != axt else L3 + 2) and Rp[u] == (sum(u) + 2 if u != axt else 2)
    sumR = sum(R.values()); assert sumR <= (m - L3) + 2*(x1 + x2) + comb(x1, 2) + comb(x2, 2) + xax*(L3 + 2)
    lbA = m*(m + 2*L3 - 2*(x1 + x2) - comb(x1, 2) - comb(x2, 2) - xax*(L3 + 2)) + 3*comb(tau, 2)
    lbB = m*(m + L3 - 2*(x1 + x2) - comb(x1, 2) - comb(x2, 2) - 2*xax) + 2*comb(tau, 2)
    assert Def2 >= lbA and Def2p >= lbB, (s.P, Def2, lbA, Def2p, lbB)
    H1 = max(x[cx] for x in D if x[a] == 1) + 1; H2 = max(x[cx] for x in D if x[b] == 1) + 1
    assert H1 + H2 <= m - L3
    assert Def2p >= pc*(comb(L3 - H1, 2) + comb(L3 - H2, 2))
    return True
n = 0
if sys.argv[1] == 'exh':
    for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        for g3 in itertools.combinations(range(m + 1, int(sys.argv[4])*m), 3):
            if reduce(gcd, (m,) + g3) != 1: continue
            s = NS.from_generators([m, *g3])
            if s.e == 4 and check(s): n += 1
else:
    rng = random.Random(int(sys.argv[2])); N = int(sys.argv[3]); lo, hi = int(sys.argv[4]), int(sys.argv[5])
    while n < N:
        m = rng.randint(lo, hi); g = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 4, 8])*m) for _ in range(3)]))
        if len(g) != 4 or reduce(gcd, g) != 1: continue
        s = NS.from_generators(g)
        if s.e == 4 and check(s): n += 1
print('two-face semigroups checked:', n, '- all intermediate inequalities hold')
