import sys, itertools
from collections import Counter
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
    mins=Counter(); maxs=Counter(); tot=0; both=0
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        T=Tvals(D,d)
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            tot+=1
            w=[0]*m
            for x in Dl: w[res[x]]=T[x]
            f=[sum(k*w[(s-k)%m] for k in range(m)) for s in range(m)]
            sl=[(fs-(d-1)*m*(m-1)//2)//m for fs in f]
            mins[min(sl)]+=1; maxs[max(sl)]+=1
            if min(sl)==0 and max(sl)==m-1: both+=1
    print('d',d,'m',m,'tiles',tot,'min slack dist',dict(mins),'max slack dist',dict(maxs),'range exactly [0,m-1]:',both,flush=True)
