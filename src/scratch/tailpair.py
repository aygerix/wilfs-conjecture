# Tail-pairing TP: for all J>=0: sum_{j>=J} F(E_{s+jm}) >= sum_z (floor(V(z)/m) - J)^+   (any positive lift?)
# F(E) computed as sum_{y in E}(d - T(y)).  Report failures for standard lift and for lifts k in [0,KL]^d.
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2]); KL=int(sys.argv[3]); M0=int(sys.argv[4]) if len(sys.argv)>4 else 3
for m in range(M0,M+1):
    tot=0; fstd=0; flift=0; ex=None; mins=10**9
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
                Jm=max(V.values())//m+1
                order=sorted(Dl,key=lambda z:V[z])
                for s in range(m):
                    tot+=1
                    # F(E_t) = sum_{V(y)<=t}(d-T(y))
                    Fs=[sum(d-T[y] for y in Dl if V[y]<=s+j*m) for j in range(Jm+1)]
                    bad=False
                    for J in range(Jm+1):
                        lhs=sum(Fs[J:]); rhs=sum(max(0,V[z]//m-J) for z in Dl)
                        mins=min(mins,lhs-rhs)
                        if lhs<rhs: bad=True
                    if bad:
                        if all(x==0 for x in k): fstd+=1
                        else: flift+=1
                        if ex is None: ex=(Dl,p,ph,s)
    print(f'd={d} m={m}: cases {tot}; TP fails std-lift {fstd}, other lifts {flift}; min surplus {mins}',ex if ex else '',flush=True)
