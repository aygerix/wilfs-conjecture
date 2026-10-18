# Is there a MONOTONE transport (unit from x goes to a top t >= x componentwise) of cost <= m(m-1)/2 ?
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets, Tvals
from mcf import min_cost_transport
d=int(sys.argv[1]); M=int(sys.argv[2]); m0=int(sys.argv[3]) if len(sys.argv)>3 else 3
for m in range(m0,M+1):
    tot=bad=0; ex=None; worst=-10**9
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        T=Tvals(D,d); tops=[t for t in Dl if T[t]>0]
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            tot+=1
            cost=[[ ((res[t]-res[x])%m if all(t[k]>=x[k] for k in range(d)) else None) for t in tops] for x in Dl]
            c=min_cost_transport([d]*m,[T[t] for t in tops],cost)
            worst=max(worst,c-m*(m-1)//2)
            if c is None or c>m*(m-1)//2:
                bad+=1
                if ex is None: ex=(Dl,p,c,m*(m-1)//2)
    print('d',d,'m',m,'tiles',tot,'monotone transport too costly:',bad,'max(cost-m(m-1)/2)',worst,ex,flush=True)
