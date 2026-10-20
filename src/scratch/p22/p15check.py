# Lead's independent check of codex P15 claims (2026-10-20). Uses reviewcheck.semigroup (own code) and direct definitions.
import sys
from math import comb
import reviewcheck as rc
def full(gens):
    m, mem, ap, mg, c, g = rc.semigroup(gens)
    P = [n for n in mg if n != m]; e = len(mg)
    M = max(ap); q = -(-c // m); rho = q * m - c; pst = M % m + 1; h = c - (q - 1) * m
    def sK(p): return sum(rc.Cp(x, p, m) - sum(rc.nu(x, n, mem) * (rc.Cp(x, p, m) - rc.Cp(x - n, p, m)) for n in P) for x in ap)
    aps = set(ap)
    def top(x, n):
        while x + n in aps: x += n
        return x
    Lam = sum((M - top(x, n)) // m for n in P for x in ap)
    W = e * (c - g) - c
    allp = [sK(p) - (m - e) for p in range(1, m + 1)]
    return dict(m=m, e=e, c=c, g=g, M=M, q=q, pstar=pst, h=h, rho=rho, Lam=Lam, W=W, excess_pstar=sK(pst) - (m - e),
                maxexcess=max(allp), argmax=allp.index(max(allp)) + 1, KID=(W == rho + Lam - sK(pst)), eh=e - h + Lam)
for gens in ([13,22,23,50,51,60], [14,22,23,61,62,63,71], [14,22,23,57,61,62,63], [14,22,23]):
    print(gens, full(gens))
# family T1-H (5.2): m = H^2+3H-1, L = H+4, n = 2m-L, S = <m, n, n+1> u [c, inf), c = (2H-2)m+2
for H in range(3, 6):
    L = H + 4; m = H * H + 3 * H - 1; n = 2 * m - L; c = (2 * H - 2) * m + 2
    gens = [m, n, n + 1] + list(range(c, c + m))
    r = full(gens); print("T1-H H=%d" % H, r, "pred excess", comb(H - 1, 2))
# family 6.1: S_t = <3t+1, 5t+2, 5t+3> u [13t+5, inf)
for t in range(4, 8):
    m = 3 * t + 1; c = 13 * t + 5
    r = full([m, 5 * t + 2, 5 * t + 3] + list(range(c, c + m))); print("6.1 t=%d" % t, r, "pred W", 29 * t - 89)
