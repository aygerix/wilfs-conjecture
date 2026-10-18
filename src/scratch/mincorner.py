# is min_s slack(s) attained at s = phi(t) for a maximal cell t (all t+e_a not in D)?
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2]); m0=int(sys.argv[3]) if len(sys.argv)>3 else 3
for m in range(m0,M+1):
    tot=bad=0; ex=None; atmaxV=0
    for D in downsets(m,d):
        Dl=sorted(D); S=set(Dl)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        T=Tvals(D,d)
        maxc=[t for t in Dl if all(tuple(t[:a]+(t[a]+1,)+t[a+1:]) not in S for a in range(d))]
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            tot+=1
            w=[0]*m
            for x in Dl: w[res[x]]=T[x]
            sl=[(sum(k*w[(s-k)%m] for k in range(m))-(d-1)*m*(m-1)//2)//m for s in range(m)]
            mn=min(sl)
            if not any(sl[res[t]]==mn for t in maxc):
                bad+=1
                if ex is None: ex=(Dl,p,sl,[(t,res[t]) for t in maxc])
            # is it at the V-max cell (standard lift)?
            V={x:sum(x[a]*p[a] for a in range(d)) for x in Dl}
            tm=max(Dl,key=lambda x:V[x])
            if sl[res[tm]]==mn: atmaxV+=1
    print('d',d,'m',m,'tiles',tot,'min NOT at a maximal cell:',bad,' min at std-V-max cell:',atmaxV,ex,flush=True)
