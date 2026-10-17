# GTP: for all integers th >= 0:  sum_{t = s mod m, t >= th} F(E_t)  >=  #{gaps u of S_D=V(D)+mN with u >= th}
# (u gap iff u < V(c(u mod m))).  th=0 is the Wilf direction X(s) >= K.
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2]); KL=int(sys.argv[3]); M0=int(sys.argv[4]) if len(sys.argv)>4 else 3
for m in range(M0,M+1):
    tot=0; fails=0; ex=None; tight=0
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        T=Tvals(D,d)
        for p in itertools.product(range(1,m),repeat=d):
            res={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
            if len(set(res.values()))!=m: continue
            for k in itertools.product(range(KL+1),repeat=d):
                ph=[p[a]+m*k[a] for a in range(d)]
                V={z:sum(x*q for x,q in zip(z,ph)) for z in Dl}
                Vr={res[z]:V[z] for z in Dl}
                top=max(V.values())
                byV=sorted(Dl,key=lambda z:V[z])
                # prefix F: F(E_t) = sum_{V(y)<=t} (d - T(y))
                Fat={}; acc=0; idx=0
                for t in range(top+1):
                    while idx<len(byV) and V[byV[idx]]<=t: acc+=d-T[byV[idx]]; idx+=1
                    Fat[t]=acc
                gap=[1 if u<Vr[u%m] else 0 for u in range(top+1)]
                for s in range(m):
                    tot+=1
                    supply=0; demand=0; ok=True; tt=False
                    for th in range(top,-1,-1):
                        if th%m==s: supply+=Fat[th]
                        demand+=gap[th]
                        if supply<demand: ok=False; break
                        if supply==demand and demand>0: tt=True
                    if not ok:
                        fails+=1
                        if ex is None: ex=(Dl,p,ph,s,th)
                    tight+=tt
    print(f'd={d} m={m}: cases {tot}; GTP fails {fails}; cases with an intermediate tight threshold {tight}',ex if ex else '',flush=True)
