"""LAYER-KNESER check (lead, 2026-10-19).  Any numerical semigroup S, multiplicity m, depth D = ceil(c/m),
k = |S cap (m,2m)|, B = {0} u (S cap (m,2m) - m).  G_H = gap residues of band [Hm,(H+1)m).
Claims:  (1) G_{H+2} - B subset G_H (mod m);  (2) Kneser: g_H >= g_{H+2} + delta, delta = ceil((k+1)/2) (k if m prime),
whenever G_{H+2} nonempty;  (3) ell >= D + delta*floor((D-2)^2/4).
Also: criterion LK: e*(D + delta*floor((D-2)^2/4)) >= c  (=> Wilf), compared with DKM Thm 1.5 (k >= sqrt(Dm/(D-2)), D>2).
usage: python layer_kneser.py seed trials mmin mmax"""
import sys, random, math
sys.path.insert(0, sys.argv[5] if len(sys.argv) > 5 else '../nowrap')
from pmin_tile import apery, minimal_gens
def isprime(n): return n > 1 and all(n % p for p in range(2, int(n**0.5)+1))
seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
tot = viol1 = viol2 = viol3 = 0; LK = DKM = LKonly = DKMonly = 0; slack3 = None
for tr in range(T):
    m = rng.randint(mmin, mmax); mode = rng.random()
    if mode < 0.35: gens = [m+rng.randint(1, m-1) for _ in range(rng.randint(2, 8))]
    elif mode < 0.7: gens = [m+rng.randint(1, max(2, int(2*math.sqrt(m)))) for _ in range(rng.randint(2, 6))]
    else: gens = [rng.randint(m+1, rng.choice([3, 5, 9])*m) for _ in range(rng.randint(2, 9))]
    ap = apery(m, gens)
    if None in ap: continue
    n, ap = minimal_gens(m, gens); e = len(n)+1
    c = max(ap)-m+1
    if c <= m: continue
    inS = lambda z: z >= 0 and z >= ap[z % m]
    D = -(-c//m)
    Bset = [0]+[s-m for s in range(m+1, 2*m) if inS(s)]; k = len(Bset)-1
    if k == 0 or math.gcd(m, *Bset) != 1: continue        # hypothesis: B generates Z/m
    delta = k if isprime(m) else -(-(k+1)//2)
    tot += 1
    G = [set(r for r in range(m) if not inS(H*m+r)) for H in range(D+2)]
    for H in range(D):
        if not all(((r-b) % m) in G[H] for r in G[H+2] for b in Bset): viol1 += 1; break
    for H in range(D):
        if G[H+2] and len(G[H]) < len(G[H+2])+delta:
            viol2 += 1
            if viol2 <= 3: print("STEP FAIL m", m, "gens", n, "k", k, "H", H, "g_H", len(G[H]), "g_H+2", len(G[H+2]), "delta", delta, flush=True)
            break
    g = sum(w//m for w in ap); ell = c-g
    lb = D+delta*((D-2)**2//4) if D >= 2 else D
    if ell < lb: viol3 += 1
    sl = ell-lb
    if slack3 is None or sl < slack3[0]: slack3 = (sl, m, n)
    lk = e*lb >= c; dk = D > 2 and k >= math.sqrt(D*m/(D-2))
    LK += lk; DKM += dk; LKonly += lk and not dk; DKMonly += dk and not lk
print("semigroups (c > m, k >= 1, gcd(m,B) = 1):", tot, " violations (1) G-inclusion:", viol1, " (2) Kneser step:", viol2, " (3) ell bound:", viol3)
print("min (ell - bound):", slack3)
print("criterion LK holds:", LK, " DKM Thm 1.5 holds:", DKM, " LK only:", LKonly, " DKM only:", DKMonly)
