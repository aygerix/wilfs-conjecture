# Localizations of slack = sum_C [H_C(tau_C) - H_C(kappa_C)] (lex order kappa).
# (a) per direction a: Delta_a >= 0 ?   (b) best order: exists permutation pi with all prefix... just per-direction min over orders
# (c) per column: tau_C <= kappa_C ?  fraction
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2])
def columns(D):
    cols=[]
    for a in range(d):
        for x in D:
            if x[a]!=0: continue
            C=[x]; y=list(x)
            while True:
                y[a]+=1
                if tuple(y) not in D: break
                C.append(tuple(y))
            cols.append((a,C))
    return cols
for m in range(3,M+1):
    tot=0; dirneg={a:0 for a in range(d)}; anyorder_ok=0; colviol=0; ncol=0
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        cols=columns(D)
        for p in itertools.product(range(1,m),repeat=d):
            res={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
            if len(set(res.values()))!=m: continue
            for s in range(m):
                tot+=1
                ok_some=False
                for pi in itertools.permutations(range(d)):
                    pos={a:i for i,a in enumerate(pi)}
                    De=[0]*d
                    for a,C in cols:
                        L=len(C)
                        H=lambda t: sum(1 for i in range(1,L) if (i*p[a])%m>=t)
                        tau=(res[C[-1]]-s-1)%m+1
                        kap=m-(sum(C[0][b]*p[b] for b in range(d) if pos[b]>pos[a])%m)
                        De[a]+=H(tau)-H(kap)
                        if pi==tuple(range(d)):
                            ncol+=1; colviol+= tau>kap and H(tau)<H(kap)
                    if pi==tuple(range(d)):
                        for a in range(d): dirneg[a]+= De[a]<0
                    if all(x>=0 for x in De): ok_some=True
                anyorder_ok+=ok_some
    print(f'd={d} m={m}: cases {tot}; lex order: per-direction Delta_a<0 counts {dirneg}; some order makes all Delta_a>=0: {anyorder_ok}/{tot}; columns with H(tau)<H(kappa): {colviol}/{ncol}',flush=True)
