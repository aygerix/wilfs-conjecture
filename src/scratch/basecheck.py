# check (1) base-slack(sigma) == sigma + sum_x G_sigma(x)  [carry form]
#       (2) for boxes: Tile slack(s) == base-slack(s - phi(kappa))
#       (3) Base-CL range on all tiles
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
    n=b1=b2=b3=nbox=0
    for D in downsets(m,d):
        Dl=sorted(D); S=set(Dl)
        if any(all(x[a]==0 for x in Dl) for a in range(d)): continue
        T=Tvals(D,d)
        kap=tuple(max(x[a] for x in Dl) for a in range(d))
        isbox = len(Dl)==eval('*'.join(str(k+1) for k in kap))
        # column lengths at bases
        Lam={}
        for x in Dl:
            for a in range(d):
                if x[a]==0:
                    L=1
                    while tuple(x[:a]+(L,)+x[a+1:]) in S: L+=1
                    Lam[(x,a)]=L
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            w=[0]*m
            for x in Dl: w[res[x]]=T[x]
            for sg in range(m):
                n+=1
                num=sum(L*((res[x]+sg)%m) for (x,a),L in Lam.items())-(d-1)*m*(m-1)//2
                if num%m: b1+=1; continue
                bs=num//m
                G=0
                for y in Dl:
                    l=[(y[a]*p[a])%m for a in range(d)]; Ssum=sg+sum(l); r=Ssum%m
                    G+=sum(1 for t in l if t>r)-Ssum//m
                if bs!=sg+G: b1+=1
                if not (0<=bs<=m-1): b3+=1
            if isbox:
                nbox+=1
                pk=sum(i*j for i,j in zip(kap,p))%m
                for s in range(m):
                    sl=(sum(k*w[(s-k)%m] for k in range(m))-(d-1)*m*(m-1)//2)//m
                    sg=(s-pk)%m
                    num=sum(L*((res[x]+sg)%m) for (x,a),L in Lam.items())-(d-1)*m*(m-1)//2
                    if sl!=num//m: b2+=1
    print('d',d,'m',m,'(tile,sigma)',n,'carryform mismatch',b1,'box reflection mismatch',b2,'(box tiles',nbox,') BaseCL range fails',b3,flush=True)
