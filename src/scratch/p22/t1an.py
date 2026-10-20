# T1 analyzer (lead, 2026-10-20): given generators, print Apery set, nu, tops, J, K_p at the true shift, and T1 slack at every p.
# T1(p):  sum_{x in Ap*} J(x) * floor((x-p)/m) >= 0,  J(x) = sum_{a: x+n_a not in Ap} (nu_a(x)+1) - e.
import sys
def semigroup(gens, N):
    S = [False] * (N + 1); S[0] = True
    for x in range(1, N + 1): S[x] = any(x >= g and S[x - g] for g in gens)
    return S
def analyze(gens, verbose=True):
    gens = sorted(gens); m = gens[0]; N = m * max(gens) * 2 + 10
    S = semigroup(gens, N)
    Ap = [next(x for x in range(i, N, m) if S[x]) for i in range(m)]
    inAp = set(Ap)
    P = [g for g in gens[1:] if not any(S[g - h] and g - h > 0 for h in gens if h < g)]
    d = len(P); e = d + 1
    M = max(Ap); c = M - m + 1; q = -(-c // m); mu = M - q * m
    def nu(a, x):
        k = 0
        while x - (k + 1) * a >= 0 and S[x - (k + 1) * a]: k += 1
        return k
    J = {}
    for x in Ap:
        J[x] = sum(nu(a, x) + 1 for a in P if x + a not in inAp) - e
    slack = {}
    for p in range(1, m + 1):
        slack[p] = sum(J[x] * ((x - p) // m) for x in Ap if x)
    pt = mu + 1
    if verbose:
        print("gens", gens, "m", m, "e", e, "c", c, "q", q, "true p", pt, "g", sum((x - x % m) // m for x in Ap))
        for x in sorted(Ap):
            nus = [nu(a, x) for a in P]
            tops = [a for a in P if x + a not in inAp]
            Kp = ((x - pt) // m + 1 if x else 0) - sum(nu(a, x) * (((x - pt) // m) - ((x - a - pt) // m)) for a in P)
            print("  x=%4d res=%3d k=%3d nu=%s tops=%s J=%3d K(true p)=%d" % (x, x % m, x // m, nus, tops, J[x], Kp))
        print("  slack by p (K units):", [slack[p] for p in range(1, m + 1)])
    return slack, pt
if __name__ == "__main__":
    analyze([int(t) for t in sys.argv[1].split(",")])
