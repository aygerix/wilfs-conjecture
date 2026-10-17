# For Apery lifts (V(exit vectors) >= 0), semigroup-relevant s* = phi(argmax V), sigma* = m-1-s*.
# Is rho(y) = floor((V(y)+sigma*)/m) directionally convex on D?  If yes, Ramp Lemma => CL (Wilf direction).
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2]); K=int(sys.argv[3])
def dirconvex(D,rho):
    for u in D:
        for a in range(d):
            ua=list(u); ua[a]+=1; ua=tuple(ua)
            if ua not in D: continue
            da=rho[ua]-rho[u]
            for b in range(d):
                ub=list(u); ub[b]+=1; ub=tuple(ub)
                uab=list(ua); uab[b]+=1; uab=tuple(uab)
                if ub in D and uab in D and rho[uab]-rho[ub] < da: return False
    return True
for m in range(3,M+1):
    nt=0; napery=0; nconv=0; tiles_conv=0; tiles_with_apery=0
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        for p in itertools.product(range(1,m),repeat=d):
            res={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
            if len(set(res.values()))!=m: continue
            inv={r:n for n,r in res.items()}
            nt+=1
            Ex=[]
            for z in Dl:
                for a in range(d):
                    y=list(z); y[a]+=1; y=tuple(y)
                    if y in D: continue
                    zp=inv[(res[z]+p[a])%m]; Ex.append(tuple(u-v for u,v in zip(y,zp)))
            anyap=False; anyconv=False
            for k in itertools.product(range(K+1),repeat=d):
                ph=[p[a]+m*k[a] for a in range(d)]
                if any(sum(l*q for l,q in zip(lam,ph))<0 for lam in Ex): continue
                anyap=True; napery+=1
                V={z:sum(x*q for x,q in zip(z,ph)) for z in Dl}
                ystar=max(Dl,key=lambda z:V[z]); sig=m-1-res[ystar]
                rho={z:(V[z]+sig)//m for z in Dl}
                if dirconvex(D,rho): nconv+=1; anyconv=True
            tiles_with_apery+=anyap; tiles_conv+=anyconv
    print(f'd={d} m={m}: tiles {nt}, with Apery lift in [0,{K}]^d: {tiles_with_apery}, (tile,lift) Apery pairs {napery}, convex pairs {nconv}, tiles with some convex Apery lift {tiles_conv}',flush=True)
