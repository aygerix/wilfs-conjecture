# LocCL: can the carries c(x) be routed to columns through x, each column C absorbing at most
# H_C(s) = #{arcs (y,a) in C containing s}?  (flow test, for every s)
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
from maxflow import MF
d=int(sys.argv[1]); M=int(sys.argv[2]); m0=int(sys.argv[3]) if len(sys.argv)>3 else 3
for m in range(m0,M+1):
    tot=bad=0; ex=None; badtiles=0
    for D in downsets(m,d):
        Dl=sorted(D); S=set(Dl)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        cols={}  # (a, base) -> list of cells
        for x in Dl:
            for a in range(d):
                b=tuple(0 if i==a else x[i] for i in range(d))
                cols.setdefault((a,b),[]).append(x)
        colkeys=list(cols)
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            c={x:sum((x[a]*p[a])%m for a in range(d))//m for x in Dl}
            c0=sum(c.values()); tb=False
            for s in range(m):
                tot+=1
                cap={}
                for (a,b) in colkeys:
                    C=cols[(a,b)]; top=max(C,key=lambda y:y[a])
                    cap[(a,b)]=sum(1 for y in C if (s-res[y])%m < (res[top]-res[y])%m)
                n=2+len(Dl)+len(colkeys); g=MF(n); idx={x:2+i for i,x in enumerate(Dl)}
                cid={k:2+len(Dl)+j for j,k in enumerate(colkeys)}
                for x in Dl:
                    if c[x]: g.add(0,idx[x],c[x])
                    for a in range(d):
                        b=tuple(0 if i==a else x[i] for i in range(d)); g.add(idx[x],cid[(a,b)],c[x] or 0)
                for k in colkeys: g.add(cid[k],1,cap[k])
                f=g.flow(0,1)
                if f<c0:
                    bad+=1; tb=True
                    if ex is None: ex=(Dl,p,s,c0,f)
            badtiles+=tb
    print('d',d,'m',m,'(tile,s)',tot,'LocCL fails',bad,'tiles with a failure',badtiles,ex,flush=True)
