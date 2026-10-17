# AP-Ramp: A(t0) := sum_{j>=0} tau(t0 + j m), tau(t) = sum_{V(y)>t} beta(y).  Conjecture: A(t0) <= (m-1-t0)^+ for all t0>=0.
# Report max of A(t0) - (m-1-t0)^+ and the min of A(t0) (lower behaviour), per range of t0.
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2]); KL=int(sys.argv[3])
for m in range(3,M+1):
    worst=-10**9; ex=None; lowmin_ge_m=10**9; lowrel=10**9; tot=0
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
                top=max(V.values())
                tau=[sum(beta[y] for y in Dl if V[y]>t) for t in range(top+1)]
                for t0 in range(top+1):
                    tot+=1
                    A=sum(tau[t] for t in range(t0,top+1,m))
                    ex_=A-max(0,m-1-t0)
                    if ex_>worst: worst=ex_; ex=(Dl,p,ph,t0,A)
                    if t0>=m: lowmin_ge_m=min(lowmin_ge_m,A); lowrel=min(lowrel,A+ (t0 if t0<m else 0))
    print(f'd={d} m={m}: (tile,lift,t0) {tot}; max [A - (m-1-t0)^+] = {worst}; min A over t0>=m = {lowmin_ge_m}',ex if worst>0 else '',flush=True)
