# Two-face e = 4: coverage of (m, L3) by proved bounds (see NOTEBOOK 2026-10-18 "two-face identity").
#  A' : L3 <= m/4, c > 3m: identity with M >= 4m, p_c >= m, Def2D >= m(2m + L3 - |runs ending in X|)
#  B'': m >= 2 L3: 3W >= (L3-1)(m+1)(m-2L3)/m + 4[m + L3 - 2(x1+x2) - C(x1,2) - C(x2,2) - 2 xax] - 3(m-1) >= 0
#       for all feasible x (x1(x1+1)/2 + x2(x2+1)/2 <= m - L3)  [B (Def2D' >= 0) is the bracket dropped]
#  C  : tau-criterion, max 2tau + P2 <= m+1
#  D  : G = m(L3-1) - 2 L3(L3-1) + 2 h(H1) + 2 h(H2) >= 3(m-1) for all 1 <= H1, H2 <= L3, H1 + H2 <= m - L3,
#       h(H) = (L3-H)(L3-H-1)   (single-cell rows above column 1, deficits measured from the axis top)
import sys
def feas(cap, L3):
    # x_i = number of top-layer off-axis corners of face i: distinct heights in [0, L3 - 1 - xax], distinct columns
    for ax in (0, 1):
        x1 = 0
        while x1*(x1 + 1)//2 <= cap and x1 <= L3 - ax:
            rem = cap - x1*(x1 + 1)//2; x2 = 0
            while (x2 + 1)*(x2 + 2)//2 <= rem and x2 + 1 <= L3 - ax: x2 += 1
            for y2 in range(x2 + 1): yield x1, y2, ax
            x1 += 1
def C_ok(m, L3):
    return max(2*(a + b + ax) + a*(a-1)//2 + b*(b-1)//2 + ax*(a + b) + min(a, b) for a, b, ax in feas(m - L3, L3)) <= m + 1
def B2_ok(m, L3):
    if m < 2*L3: return False
    first = (L3 - 1)*(m + 1)*(m - 2*L3)
    worst = min(max(0, m*(m + L3 - 2*(a + b) - a*(a-1)//2 - b*(b-1)//2 - 2*ax) + 2*(a + b + ax)*(a + b + ax - 1)//2) for a, b, ax in feas(m - L3, L3))
    return first + 4*worst - 3*m*(m - 1) >= 0
def D_ok(m, L3):
    h = lambda H: (L3 - H)*(L3 - H - 1) if H < L3 else 0
    N = m - L3
    G = min(m*(L3 - 1) - 2*L3*(L3 - 1) + 2*h(H1) + 2*h(H2) for H1 in range(1, min(L3, N - 1) + 1) for H2 in range(1, min(L3, N - H1) + 1))
    return G >= 0 and (m + 1)*G >= 3*m*(m - 1)
def A_ok(m, L3):
    # A' : 3mW + 3m(m-1) >= 4m(m - 4L3) + 2(m+1) L3 (L3-1) + 4 Def2D,  Def2D >= m(2m + L3 - sum_X R) + 3 C(tau, 2)
    #      (runs ending below c have deficit >= m; top-layer ends have distinct deficits m - pi(u), each run-length sum R >= 3)
    if 4*L3 > m: return False
    worst = min(max(0, m*(m + 2*L3 - 2*(a + b) - a*(a-1)//2 - b*(b-1)//2 - ax*(L3 + 2)) + 3*(a + b + ax)*(a + b + ax - 1)//2)
                for a, b, ax in feas(m - L3, L3))
    return 4*m*(m - 4*L3) + 2*(m + 1)*L3*(L3 - 1) + 4*worst >= 3*m*(m - 1)   # exact: p_c >= m+1, M >= 4m
if __name__ == '__main__':
    lo, hi = int(sys.argv[1]), int(sys.argv[2]); last = None
    for m in range(lo, hi + 1):
        bad = [L3 for L3 in range(2, m - 1) if not (A_ok(m, L3) or B2_ok(m, L3) or C_ok(m, L3) or D_ok(m, L3))]
        if bad: last = m; print('m', m, 'uncovered L3', bad)
    print('largest uncovered m in range:', last)
