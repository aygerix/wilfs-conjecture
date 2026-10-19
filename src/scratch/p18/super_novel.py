"""LK-SUPER coverage for semigroups with EMPTY first layer (S cap (m,2m) = {}), where YZ / LK / DKM say nothing.
S = <m, jm + a : a in A*> (j = 2 or 3), A* a random subset of [1, L] (not an AP), sometimes plus higher generators.
Bound (m prime): Theta_t >= floor((t+1)/(j0+1)) * Theta_{j0}, j0 = first band with a nonzero residue;
ell >= q + sum_{t=1}^{q-2} Theta_t + max(0, Theta_{q-1} - rho).  General m: delta = ceil(u/2) per step, gcd(m, R_j0) = 1.
Criteria compared: SUPER, YZ33 (eta = 0: e*q >= c), LIT (c <= 3m, 3e >= m, m <= 18), Kaplan 2g < 3m, FGH t <= e-1, SYM, GAS (A* interval).
usage: python super_novel.py seed trials [path to pmin_tile]"""
import sys, random, math
sys.path.insert(0, sys.argv[3] if len(sys.argv) > 3 else '../nowrap')
from pmin_tile import apery, minimal_gens
def isprime(n): return n > 1 and all(n % p for p in range(2, int(n**0.5)+1))
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2])
tot = new = 0; ex = []; cov = {}
for tr in range(T):
    pr = rng.random() < 0.7
    pool = [p for p in range(60, 500) if isprime(p) == pr]
    m = rng.choice(pool); jj = rng.choice([2, 2, 3])
    L = rng.randint(6, int(2*math.sqrt(m)) + 6); k = rng.randint(2, L - 2)
    A = sorted(rng.sample(range(1, L + 1), k))
    if A == list(range(A[0], A[0] + len(A))): continue
    gens = [jj*m + a for a in A]
    if rng.random() < 0.3: gens += [rng.randint((jj+1)*m, 6*m) for _ in range(rng.randint(1, 3))]
    if math.gcd(m, *gens) != 1: continue
    ap = apery(m, gens)
    if None in ap: continue
    n, ap = minimal_gens(m, gens); e = len(n) + 1
    c = max(ap) - m + 1; g = sum(w // m for w in ap); ell = c - g; q = -(-c // m); rho = q*m - c
    inS = lambda z: z >= 0 and z >= ap[z % m]
    if any(inS(s) for s in range(m+1, 2*m)) or q < 4: continue
    R = lambda t: [r for r in range(m) if inS(t*m + r)]
    j0 = next(t for t in range(1, q) if len(R(t)) >= 2)
    Rj = R(j0); u = len(Rj)
    if not isprime(m) and math.gcd(m, *Rj) != 1: continue
    delta = (u - 1) if isprime(m) else (u + 1) // 2
    # Theta lower bounds: Theta_t >= (#steps) * delta + [base Theta_{j0} for the first copy]
    def thlow(t):
        s = (t + 1) // (j0 + 1)
        return 0 if s == 0 else (u - 1) + (s - 1) * delta
    LB = q + sum(thlow(t) for t in range(1, q - 1)) + max(0, thlow(q - 1) - rho)
    assert ell >= LB, (m, n, c, LB, ell)
    tot += 1
    apset = set(ap)
    tt = sum(1 for w in ap if w and not any((w + x) in apset for x in n))
    crit = dict(SUPER=e*LB >= c, YZ33=e*q >= c, LIT=c <= 3*m or 3*e >= m or m <= 18, KAPLAN=2*g < 3*m, FGH=tt <= e-1, SYM=(tt == 1))
    for kx, vx in crit.items(): cov[kx] = cov.get(kx, 0) + vx
    if crit['SUPER'] and not any(v for kx, v in crit.items() if kx != 'SUPER'):
        new += 1
        if len(ex) < 6: ex.append((m, n, c, q, e, j0, u, tt, ell, LB))
print("empty-first-layer S (q >= 4):", tot, "coverage:", cov)
print("SUPER and none of the listed criteria:", new)
for x in ex: print("  m=%d gens=%s c=%d q=%d e=%d j0=%d u=%d type=%d ell=%d LB=%d" % x)
