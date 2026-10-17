# Pointwise: tau(t) = beta(D cap {V > t}) <= 0 for all t >= m-1 ?  (standard lift and others)
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2]); KL=int(sys.argv[3])
for m in range(3,M+1):
    tot=0; bad_std=0; bad_other=0; ex=None; worst=0; firstbad=[]
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        T=Tvals(D,d); beta={y:d+1-T[y] for y in Dl}
        for p in itertools.product(range(1,m),repeat=d):
            res={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
            if len(set(res.values()))!=m: continue
            for k in itertools.product(range(KL+1),repeat=d):
                ph=[p[a]+m*k[a] for a in range(d)]
                V={z:sum(x*q for x,q in zip(z,ph)) for z in Dl}
                top=max(V.values()); tot+=1
                for t in range(m-1,top+1):
                    tau=sum(beta[y] for y in Dl if V[y]>t)
                    if tau>0:
                        if all(x==0 for x in k): bad_std+=1
                        else: bad_other+=1
                        if tau>worst: worst=tau; ex=(Dl,p,ph,t,tau)
                        break
    print(f'd={d} m={m}: (tile,lift) {tot}; some t>=m-1 with tau>0: std-lift {bad_std}, other lifts {bad_other}; worst tau {worst}',ex if ex and m<=6 else '',flush=True)
