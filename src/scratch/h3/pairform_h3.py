"""Pure-pair decomposition of MaxCL at height <= 3 (lead, 2026-10-19).
For a cubic y: 2 rho(y) = sum_a y_a rho(y-e_a) - rho_0 - m kappa(y)   (kappa in {-1,0,1,2});
for a maximal pair x = e_a+e_b: rho(x) = rho_a + rho_b - rho_0 - m kappa(x)  (kappa in {-1,0,1}).
Then (exact)  RHS-LHS = sum_{N2} (d+1-psi(x)) rho(x) + sum_{N1} (d+1-deg_A2(a)) rho_a + (m-|N2|) rho_0 + m sum kappa,
psi(x) = sum_{c: x+e_c in D} (x_c+1) = cubic load of x.   Reports the pieces and tests candidate separate bounds.
usage: python pairform_h3.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '.')
from maxcl_h3 import apery_tile, in_semigroup

def analyze(m, gens, sig):
    best = apery_tile(m, gens)
    d = len(gens)
    D = {x: w for (w, x) in best.values()}
    E = [tuple(1 if i == a else 0 for i in range(d)) for a in range(d)]
    if any(e not in D for e in E): return None
    if max(sum(x) for x in D) != 3: return None
    rho = {x: (w-sig) % m for x, w in D.items()}
    z = (0,)*d; r0 = rho[z]
    def add(x, a): return tuple(x[i]+(i == a) for i in range(d))
    def sub(x, a): return tuple(x[i]-(i == a) for i in range(d))
    cub = [x for x in D if sum(x) == 3]; prs = [x for x in D if sum(x) == 2]
    A2 = [x for x in prs if all(add(x, c) not in D for c in range(d))]; N2 = [x for x in prs if x not in set(A2)]
    N1 = [a for a in range(d) if any(add(E[a], b) in D for b in range(d))]
    lhs = sum(rho[x] for x in A2)+2*sum(rho[y] for y in cub)
    rhs = (d+1)*(r0+sum(rho[E[a]] for a in N1)+sum(rho[x] for x in N2))
    kap = []; kneg = kpos = 0
    for y in cub:
        sc = sum(y[a]*rho[sub(y, a)] for a in range(d) if y[a])
        k = (sc-r0-2*rho[y]); assert k % m == 0; k //= m; kap.append(k)
    kp = []
    for x in A2:
        ab = [a for a in range(d) for _ in range(x[a])]
        k = rho[E[ab[0]]]+rho[E[ab[1]]]-r0-rho[x]; assert k % m == 0; kp.append(k//m)
    psi = {x: sum(x[c]+1 for c in range(d) if add(x, c) in D) for x in N2}
    degA2 = [sum(x[a] for x in A2) for a in range(d)]
    T1p = sum((d+1-psi[x])*rho[x] for x in N2); T1u = sum((d+1-degA2[a])*rho[E[a]] for a in N1)
    n2 = len(prs)
    T2 = (m-len(N2))*r0; T3 = m*(sum(kap)+sum(kp))
    assert rhs-lhs == T1p+T1u+T2+T3, (rhs-lhs, T1p, T1u, T2, T3)
    full = sum(rho[x] for x in N2 if psi[x] == d+2)
    return dict(m=m, d=d, n2=n2, n3=len(cub), a2=len(A2), r0=r0, slack=rhs-lhs, T1p=T1p, T1u=T1u, T2=T2,
                kc_neg=sum(1 for k in kap if k < 0), kc_pos=sum(k for k in kap if k > 0), kp_neg=sum(1 for k in kp if k < 0),
                kp_pos=sum(k for k in kp if k > 0), full=full, nfull=sum(1 for x in N2 if psi[x] == d+2))

if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5])
    rng = random.Random(seed); n = 0
    worst = {}
    for tr in range(T):
        m = rng.randint(mmin, mmax); mode = rng.randrange(3)
        if mode == 0:
            d = rng.randint(3, 10); gens = sorted(set(rng.randint(m+1, 2*m-1) for _ in range(d)))
        elif mode == 1:
            d = rng.randint(3, 10); gens = sorted(set(rng.randint(m+1, 4*m) for _ in range(d)))
        else:
            d = rng.randint(3, 9); a0 = rng.randint(m+1, 3*m); st = rng.randint(1, max(1, m//(2*d)))
            gens = sorted(set(a0+i*st for i in range(d)))
        gens = [x for x in gens if x % m]
        if len(set(x % m for x in gens)) < len(gens) or len(gens) < 2: continue
        if any(in_semigroup(gens[a], m, gens[:a]+gens[a+1:]) for a in range(len(gens))): continue
        best = apery_tile(m, gens)
        if len(best) != m: continue
        M = max(w for (w, x) in best.values()); c = M-m+1
        for sig in sorted(set([c % m, 0, rng.randrange(m)])):
            R = analyze(m, gens, sig)
            if R is None: break
            n += 1
            # candidate separate bounds
            cand = {
              'wrapbal: kneg-kpos<=r0': (R['kc_pos']+R['kp_pos'])-(R['kc_neg']+R['kp_neg'])+R['r0'],
              'cubic kpos>=kneg': R['kc_pos']-R['kc_neg'],
              'T1+T3+T2>=0 (MaxCL)': R['slack'],
              'm*kpos_c >= full + nN2*r0': m*R['kc_pos']-R['full']-(R['n2']-R['a2'])*R['r0'],
              'kc_neg<=ceil(r0/2)': (R['r0']+1)//2-R['kc_neg'],
              'kp_neg<=r0': R['r0']-R['kp_neg'],
            }
            for k, v in cand.items():
                nv = v/(m*m) if 'MaxCL' in k or 'full' in k else v
                if k not in worst or nv < worst[k][0]: worst[k] = (nv, v, m, gens, sig, {kk: R[kk] for kk in ('n2','n3','a2','r0','kc_neg','kc_pos','kp_neg','kp_pos','nfull')})
    print("tested (tile,sigma) pairs:", n)
    for k, v in worst.items(): print(f"  {k:32s} worst {v[0]:.4f} raw {v[1]}  m={v[2]} gens={v[3]} sig={v[4]} {v[5]}")
