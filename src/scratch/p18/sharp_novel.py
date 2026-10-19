"""(sharp variant) LK-SHARP: Theta_t >= max(eta + delta*floor((t-1)/2), eta + (t-1)*delta - beta), beta = max(S cap (m,2m)) - m.
Does LAYER-KNESER (Kneser growth of the band populations) add coverage beyond Yang-Zhang (preprints.org 202604.0551)?
Structured S = <m, m + A*> with A* a random k-subset of [1, L] (slow layer growth, deep), sometimes with extra higher
generators.  Criteria: YZ33 = e(q + (q-2)eta + eta_rho) >= c (their Cor 3.3, first-layer staircase), YZ42 = e(eta+2) >= 2m,
YZ45 = m | c and e(3 eta + 4) >= 4m, LKYZ = e * [q + (q-2)eta + delta floor((q-3)^2/4) + max(eta_rho, eta + delta floor((q-2)/2) - rho)] >= c,
plus DKM 1.5, Cor 1.6, LIT (c <= 3m, 3e >= m, m <= 18), Kaplan 2g < 3m, FGH t <= e-1, symmetric.
usage: python yz_novel.py seed trials [path to pmin_tile]"""
import sys, random, math
sys.path.insert(0, sys.argv[3] if len(sys.argv) > 3 else '../nowrap')
from pmin_tile import apery, minimal_gens
def isprime(n): return n > 1 and all(n % p for p in range(2, int(n**0.5)+1))
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2])
tot = new = 0; ex = []; cov = {}
for tr in range(T):
    m = rng.choice([p for p in range(60, 400) if rng.random() < 0.05] or [101])
    L = rng.randint(8, int(1.5*math.sqrt(m))+8); k = rng.randint(3, L-1)
    A = sorted(rng.sample(range(1, L+1), k))
    gens = [m+a for a in A]
    if rng.random() < 0.3: gens += [rng.randint(2*m, 5*m) for _ in range(rng.randint(1, 3))]
    ap = apery(m, gens)
    if None in ap: continue
    n, ap = minimal_gens(m, gens); e = len(n)+1
    c = max(ap)-m+1; g = sum(w//m for w in ap); ell = c-g; q = -(-c//m); rho = q*m-c
    inS = lambda z: z >= 0 and z >= ap[z % m]
    B = [0]+[s-m for s in range(m+1, 2*m) if inS(s)]; eta = len(B)-1
    eta_rho = sum(1 for s in range(m+1, 2*m-rho) if inS(s))
    if eta == 0 or math.gcd(m, *B) != 1 or q < 3: continue
    tot += 1
    delta = eta if isprime(m) else (eta+2)//2
    yz31 = q+(q-2)*eta+eta_rho
    lkyz = q+(q-2)*eta+delta*(((q-3)**2)//4)+max(eta_rho, eta+delta*((q-2)//2)-rho)
    beta = max(B)
    def thl(t): return max(eta + delta*((t-1)//2), eta + (t-1)*delta - beta)
    sharp = q + sum(thl(t) for t in range(1, q-1)) + max(eta_rho, thl(q-1) - rho)
    assert ell >= sharp, (m, n, c, sharp, ell)
    assert ell >= lkyz >= yz31 - 0 or ell >= lkyz
    assert ell >= yz31
    apset = set(ap)
    t = sum(1 for w in ap if w and not any((w+x) in apset for x in n))
    crit = dict(SHARP=e*sharp >= c, LKYZ=e*lkyz >= c, YZ33=e*yz31 >= c, YZ42=q >= 4 and e*(eta+2) >= 2*m, YZ45=rho == 0 and e*(3*eta+4) >= 4*m,
                DKM=q > 2 and eta*eta*(q-2) >= q*m, COR16=g < 2*m-math.sqrt(2*m),
                LIT=c <= 3*m or 3*e >= m or m <= 18, KAPLAN=2*g < 3*m, FGH=t <= e-1, SYM=(t == 1))
    for kx, vx in crit.items(): cov[kx] = cov.get(kx, 0)+vx
    others = any(v for kx, v in crit.items() if kx != 'SHARP')
    if crit['SHARP'] and not others:
        new += 1
        if len(ex) < 5: ex.append((m, n, c, q, e, eta, t, ell, sharp, lkyz))
print("structured S (q >= 3):", tot, "coverage:", cov)
print("SHARP and none of the listed criteria (incl. LKYZ and all YZ first-layer criteria):", new)
for x in ex: print("  m=%d gens=%s c=%d q=%d e=%d eta=%d type=%d ell=%d SHARP=%d LKYZ=%d" % x)
