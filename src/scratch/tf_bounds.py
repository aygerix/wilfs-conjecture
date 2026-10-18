# Two-face e = 4: for which (m, L3) do the three proved bounds give Wilf?
#  A: L3 <= m/4 and c > 3m:  m + 2 L3^2 - 18 L3 + 3 >= 0          (identity, Def2D >= 0, M >= 4m, p_c >= m+1)
#  B: m > 2 L3:  (L3-1)(m+1)(m-2L3) >= 3m(m-1)                       (identity, Def2D' >= 0, M >= (L3-1) p_c)
#  C: tau-criterion  max 2tau + P2 <= m+1 over x1(x1+1)/2 + x2(x2+1)/2 <= m - L3
import sys
from functools import lru_cache
def C_ok(m, L3):
    cap = m - L3; best = -1
    x1 = 0
    while x1*(x1 + 1)//2 <= cap:
        rem = cap - x1*(x1 + 1)//2; x2 = 0
        while x2*(x2 + 1)//2 <= rem: x2 += 1
        x2 -= 1
        for y2 in range(0, x2 + 1):
            for ax in (0, 1):
                f = 2*(x1 + y2 + ax) + x1*(x1 - 1)//2 + y2*(y2 - 1)//2 + ax*(x1 + y2) + min(x1, y2)
                best = max(best, f)
        x1 += 1
    return best <= m + 1
def covered(m, L3):
    A = 4*L3 <= m and m + 2*L3*L3 - 18*L3 + 3 >= 0
    B = m > 2*L3 and (L3 - 1)*(m + 1)*(m - 2*L3) >= 3*m*(m - 1)
    return A or B or C_ok(m, L3), A, B
last_bad = None
for m in range(5, int(sys.argv[1]) + 1):
    bad = [L3 for L3 in range(2, m - 1) if not covered(m, L3)[0]]
    if bad: last_bad = m; print('m', m, 'uncovered L3', bad)
print('largest m with an uncovered L3:', last_bad)
