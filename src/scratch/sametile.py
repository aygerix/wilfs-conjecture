# for fixed (m,p) compare slack vectors of all down-set tiles D (same lattice ker phi)
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
    groups={}
    Ds=[D for D in downsets(m,d) if not any(all(n[a]==0 for n in D) for a in range(d))]
    for p in itertools.product(range(1,m),repeat=d):
        vecs=[]
        for D in Ds:
            Dl=sorted(D)
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            T=Tvals(D,d); w=[0]*m
            for x in Dl: w[res[x]]=T[x]
            sl=tuple((sum(k*w[(s-k)%m] for k in range(m))-(d-1)*m*(m-1)//2)//m for s in range(m))
            vecs.append((Dl,sl))
        if len(vecs)>=2: groups[p]=vecs
    same=sum(1 for v in groups.values() if len(set(s for _,s in v))==1)
    print('m',m,'p with >=2 tiles:',len(groups),'all slack vectors equal:',same, flush=True)
    for p,v in list(groups.items())[:2]:
        for Dl,sl in v: print('   p',p,'D',Dl,'slack',sl)
