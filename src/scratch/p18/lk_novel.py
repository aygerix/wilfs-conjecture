"""Is LAYER-KNESER (LK) new?  Structured S = <m, m + A*>, A* a random k-subset of [1, L] (slow layer growth, deep), and
S with extra higher generators.  For each S: LK, DKM Thm 1.5, Cor 1.6 (g < 2m - sqrt(2m)), LIT (c <= 3m, 3e >= m,
m <= 18; Sammartano 2e >= m), Kaplan (2g < 3m), FGH type bound (t <= e-1  =>  Wilf), symmetric/pseudo-symmetric.
usage: python lk_novel.py seed trials"""
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
    c = max(ap)-m+1; g = sum(w//m for w in ap); ell = c-g; D = -(-c//m)
    inS = lambda z: z >= 0 and z >= ap[z % m]
    B = [0]+[s-m for s in range(m+1, 2*m) if inS(s)]; kk = len(B)-1
    if kk == 0 or math.gcd(m, *B) != 1: continue
    tot += 1
    delta = kk if isprime(m) else (kk+2)//2
    LB = D+kk*((D-1)//2)+delta*(((D-2)**2)//4)
    assert ell >= LB
    apset = set(ap)
    t = sum(1 for w in ap if w and not any((w+x) in apset for x in n))       # type = #maximal Apery elements
    crit = dict(LK=e*LB >= c, DKM=D > 2 and kk*kk*(D-2) >= D*m, COR16=g < 2*m-math.sqrt(2*m),
                LIT=c <= 3*m or 3*e >= m or m <= 18, KAPLAN=2*g < 3*m, FGH=t <= e-1, SYM=(t == 1))
    for kx, vx in crit.items(): cov[kx] = cov.get(kx, 0)+vx
    others = any(v for kx, v in crit.items() if kx != 'LK')
    if crit['LK'] and not others:
        new += 1
        if len(ex) < 5: ex.append((m, n, c, D, e, kk, t, ell, LB))
print("structured S:", tot, "coverage:", cov)
print("LK and none of the listed known criteria:", new)
for x in ex: print("  m=%d gens=%s c=%d D=%d e=%d k=%d type=%d ell=%d LB=%d" % x)
