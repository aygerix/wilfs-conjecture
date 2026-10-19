"""e = 5 coverage map for q >= 5, m >= 40 by the proved band criteria:
 LKYZ (first layer, Kneser, gcd(m,B)=1), SHARP (first layer, window form), SUPER (first nonempty band j0),
 YZ42 (e(eta+2) >= 2m), plus per-band exact superadditive closure (prime m only, uses the actual Theta_j for j <= J):
 CLOSURE: Theta_t >= max over partitions t+1 = sum (a_i+1) of sum Theta_{a_i}, with a_i <= J (J = 2).
usage: python e5_coverage.py seed trials Kmax"""
import sys, random, math
sys.path.insert(0, '../nowrap')
from pmin_tile import apery, minimal_gens
def isprime(n): return n > 1 and all(n % p for p in range(2, int(n**0.5)+1))
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2]); Kmax = int(sys.argv[3])
tot = 0; cov = {}; unc = []
for _ in range(T):
    m = rng.randint(40, 250)
    K = rng.randint(2, Kmax)
    gens = sorted(set(rng.randint(m + 1, K * m) for _ in range(4)))
    if len(gens) != 4 or math.gcd(m, *gens) != 1: continue
    ap = apery(m, gens)
    if None in ap: continue
    n, ap = minimal_gens(m, gens)
    if len(n) != 4: continue
    e = 5; c = max(ap) - m + 1; q = -(-c // m); rho = q * m - c
    if q < 5: continue
    tot += 1
    g = sum(w // m for w in ap); ell = c - g
    x = [w // m for w in ap]
    Th = [sum(1 for r in range(1, m) if x[r] <= t) for t in range(q + 1)]
    pr = isprime(m)
    inS = lambda z: z >= 0 and z >= ap[z % m]
    B = [0] + [s - m for s in range(m + 1, 2 * m) if inS(s)]; eta = len(B) - 1
    eta_rho = sum(1 for s in range(m + 1, 2 * m - rho) if inS(s))
    crit = {}
    crit['YZ42'] = e * (eta + 2) >= 2 * m
    lkyz = sharp = 0
    if eta >= 1 and math.gcd(m, *B) == 1:
        delta = eta if pr else (eta + 2) // 2
        lkyz = q + (q - 2) * eta + delta * (((q - 3) ** 2) // 4) + max(eta_rho, eta + delta * ((q - 2) // 2) - rho)
        beta = max(B)
        thl = lambda t: max(eta + delta * ((t - 1) // 2), eta + (t - 1) * delta - beta)
        sharp = q + sum(thl(t) for t in range(1, q - 1)) + max(eta_rho, thl(q - 1) - rho)
    crit['LKYZ'] = e * lkyz >= c; crit['SHARP'] = e * sharp >= c
    # SUPER from first nonempty band j0
    j0 = next((t for t in range(1, q) if Th[t] >= 1), None)
    sup = 0
    if j0 is not None and j0 <= q - 2:
        u = Th[j0] + 1; Rj = [r for r in range(m) if x[r] <= j0]
        if pr or math.gcd(m, *Rj) == 1:
            dl = (u - 1) if pr else (u + 1) // 2
            def tl(t):
                s_ = (t + 1) // (j0 + 1)
                return 0 if s_ == 0 else (u - 1) + (s_ - 1) * dl
            sup = q + sum(tl(t) for t in range(1, q - 1)) + max(0, tl(q - 1) - rho)
    crit['SUPER'] = e * sup >= c
    # superadditive closure with actual Theta_1, Theta_2 (prime m)
    clo = 0
    if pr:
        J = 2; lb = [0] * q
        for t in range(1, q):
            best = Th[t] if t <= J else 0
            for a in range(1, min(J, t - 1) + 1):
                b_ = t - a - 1
                if b_ >= 0: best = max(best, lb[a] + lb[b_] if a <= J else 0)
            lb[t] = best
        clo = q + sum(lb[t] for t in range(1, q - 1)) + max(0, lb[q - 1] - rho)
    crit['CLOSURE'] = e * clo >= c
    for k_, v_ in crit.items(): cov[k_] = cov.get(k_, 0) + v_
    anyc = any(crit.values())
    cov['ANY'] = cov.get('ANY', 0) + anyc
    if not anyc and len(unc) < 8: unc.append((m, n, c, q, eta, round(e * ell / c, 3)))
print("e=5, q>=5, m in [40,250], Kmax=%d: %d semigroups; coverage %s" % (Kmax, tot, cov))
print("uncovered samples (m, gens, c, q, eta, e*ell/c):")
for u_ in unc: print("  ", u_)
