"""Lead's independent re-implementation of codex P10 certificate FIN64 (support-two e=5 tiles, 64 <= m <= 143),
written from the report text (P10_REPORT.md section 9), plus the analytic constants of B4 and A144 (exact arithmetic).
For each m, N2 in [0, m-5], N1 = m-1-N2, t1 in [0,4], and each multiset of six face antichain sizes a_1..a_6 with
sum t and sum C(a_i+1,2) <= N2:
  R_* (t,N2) = min rank term of {a_i copies of a_i+5}, rank term R(w) = sum_{i<j} min(w_i,w_j);
  H_* = max(0, ceil(3m - 15 t1/4 - 6t), D2(N2;6) + J12(3N1 - N2 - 6));
  check (m+1) H_* + R_* + 5(t t1 + C(t1,2)) - 3m(m-1)/2 > 0.
usage: python fin64_lead.py mlo mhi"""
import sys
from fractions import Fraction
from math import comb, isqrt
def rank_term(ws):
    ws = sorted(ws, reverse=True)
    return sum(i * w for i, w in enumerate(ws))   # = sum_{i<j} min
def parts6(t, maxpart=None):
    """multisets of 6 nonnegative integers (nondecreasing) summing to t"""
    def rec(k, rem, lo):
        if k == 1:
            if rem >= lo: yield (rem,)
            return
        for x in range(lo, rem // k + 1):
            for rest in rec(k - 1, rem - x, x): yield (x,) + rest
    yield from rec(6, t, 0)
def D2(n, f):
    s, j = 0, 0
    while n > 0:
        cap = f * (j + 1); take = min(cap, n); s += take * j; n -= take; j += 1
    return s
def J(q, S):
    if S < 0: return 0
    u, r = divmod(S, q); return q * comb(u, 2) + r * u
mlo, mhi = int(sys.argv[1]), int(sys.argv[2])
TMAX = isqrt(12 * mhi) + 2
# R_*(t, N2): min over partitions with sum C(a+1,2) <= N2; store per t the list of (cost, R) and take prefix minima
best = {}
for t in range(0, TMAX + 1):
    rows = []
    for p in parts6(t):
        cost = sum(comb(a + 1, 2) for a in p)
        ws = [a + 5 for a in p for _ in range(a)]
        rows.append((cost, rank_term(ws)))
    best[t] = sorted(rows)
def Rstar(t, N2):
    r = None
    for cost, R in best[t]:
        if cost > N2: break
        r = R if r is None else min(r, R)
    return r
glob_min = None; nprof = 0; fails = []
for m in range(mlo, mhi + 1):
    mmin = None
    for N2 in range(0, m - 4):
        N1 = m - 1 - N2
        if N1 < 4: continue
        hface = D2(N2, 6) + J(12, 3 * N1 - N2 - 6)
        for t in range(0, TMAX + 1):
            Rs = Rstar(t, N2)
            if Rs is None: continue
            for t1 in range(0, 5):
                nprof += 1
                hb = 3 * m - Fraction(15 * t1, 4) - 6 * t
                hb = -((-hb.numerator) // hb.denominator)   # ceil
                H = max(0, hb, hface)
                slack2 = 2 * ((m + 1) * H + Rs + 5 * (t * t1 + comb(t1, 2))) - 3 * m * (m - 1)
                if mmin is None or slack2 < mmin[0]: mmin = (slack2, m, N1, N2, t1, t, H, Rs)
                if slack2 <= 0: fails.append((m, N1, N2, t1, t, H, Rs, slack2))
    if glob_min is None or mmin[0] < glob_min[0]: glob_min = mmin
    print('m=%d  min 2*slack=%d at (m,N1,N2,t1,t,H*,R*)=%s' % (m, mmin[0], mmin[1:]))
print('profiles (m,N2,t,t1) checked:', nprof, ' failures:', len(fails), ' global min slack =', Fraction(glob_min[0], 2), 'at', glob_min[1:])
for f_ in fails[:10]: print('FAIL', f_)
# analytic constants
x = Fraction(12); u = None
poly = lambda X: Fraction(3, 2) * X**4 + Fraction(87, 2) * X**2 + 39 - (6 * X**2 + 27) * Fraction(52, 15) * X
print('A144 lower polynomial at sqrt(m)=12:', poly(Fraction(12)), '(report: 1707/5 =', Fraction(1707, 5), ')')
import sympy as sp
U = sp.symbols('u'); X = 12 + U
expr = sp.expand(sp.Rational(3, 2) * X**4 + sp.Rational(87, 2) * X**2 + 39 - (6 * X**2 + 27) * sp.Rational(52, 15) * X)
print('A144-POLY in u:', sp.Poly(expr, U).all_coeffs()[::-1])
print('sqrt(12) < 52/15:', Fraction(52, 15)**2 > 12, ' sqrt(12) < 7/2:', Fraction(7, 2)**2 > 12)
print('B4: (9/11)^3 < 9/16:', Fraction(9, 11)**3 < Fraction(9, 16), '  6^3*81/32 < (33/4)^3:', 216 * Fraction(81, 32) < Fraction(33, 4)**3,
      '  loss bound 1/1000+7/60+3/8 =', Fraction(1, 1000) + Fraction(7, 60) + Fraction(3, 8), '< 1/2')
print('B4 loss at m = 22^3 exactly (float):', 10 / 22**3 + (35 / 3) / (22**3)**0.5 + (33 / 4) / 22)
