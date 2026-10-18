# Gap routing: demands (x,k): km < t <= V(x)+km  (t in [1,m], standard or given lift)
# slots (y->y'=y+e_b, k): V(y)+km < t <= V(y')+km, capacity y'_b.  demand (x,k) may use slot (y',b,k) iff y' <= x.
# test: maxflow >= K = sum floor(V/m)
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
from maxflow import MF
d=int(sys.argv[1]); M=int(sys.argv[2]); KL=int(sys.argv[3]) if len(sys.argv)>3 else 0
import math
for m in range(3,M+1):
    tot=bad=0; ex=None; minex=10**9
    for D in downsets(m,d):
        Dl=sorted(D); S=set(Dl)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        for p in itertools.product(range(1,m),repeat=d):
            res=[sum(i*j for i,j in zip(x,p))%m for x in Dl]
            if len(set(res))!=m: continue
            for kl in itertools.product(range(KL+1),repeat=d):
                ph=[p[a]+m*kl[a] for a in range(d)]
                V={x:sum(i*j for i,j in zip(x,ph)) for x in Dl}
                K=sum(V[x]//m for x in Dl)
                for t in range(1,m+1):
                    tot+=1
                    dem=[(x,k) for x in Dl for k in range(-(V[x]//m)-2,1) if k*m<t<=V[x]+k*m]
                    slots=[]
                    for y2 in Dl:
                        for b in range(d):
                            if y2[b]==0: continue
                            y=tuple(y2[i]-(i==b) for i in range(d))
                            for k in range(-(V[y2]//m)-2,1):
                                if V[y]+k*m<t<=V[y2]+k*m: slots.append((y2,b,k))
                    n=2+len(dem)+len(slots); g=MF(n)
                    for i,(x,k) in enumerate(dem):
                        g.add(0,2+i,1)
                        for j,(y2,b,k2) in enumerate(slots):
                            if k2==k and all(y2[q]<=x[q] for q in range(d)): g.add(2+i,2+len(dem)+j,1)
                    for j,(y2,b,k2) in enumerate(slots): g.add(2+len(dem)+j,1,y2[b])
                    f=g.flow(0,1)
                    minex=min(minex,f-K)
                    if f<K:
                        bad+=1
                        if ex is None: ex=(Dl,p,ph,t,K,f)
    print('d',d,'m',m,'cases',tot,'routing<K:',bad,'min(flow-K)',minex,ex,flush=True)
