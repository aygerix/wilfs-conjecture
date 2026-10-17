import sys, itertools, random
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); m=int(sys.argv[2]); N=int(sys.argv[3]); random.seed(int(sys.argv[4]) if len(sys.argv)>4 else 1)
tgt=(d-1)*m*(m-1)//2
inst=[]
for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    T=Tvals(D,d)
    for p in itertools.product(range(m),repeat=d):
        res=[sum(x*y for x,y in zip(n,p))%m for n in Dl]
        if len(set(res))!=m: continue
        inst.append((Dl,p,T,res))
random.shuffle(inst)
for Dl,p,T,res in inst[:N]:
    w=[0]*m
    for n,r in zip(Dl,res): w[r]=T[n]
    sl=[(sum(k*w[(s-k)%m] for k in range(m))-tgt)//m for s in range(m)]
    print('D',[''.join(map(str,n)) for n in Dl],'p',p)
    print('   T by residue',w)
    print('   slack(s)    ',sl, 'sorted',sorted(sl))
