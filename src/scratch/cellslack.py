# slack attached to cells: c(y) = slack(s) with s = phi(y)-1 ; compare with phi(M-y) for maximal M >= y
import sys, itertools, random
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); m=int(sys.argv[2]); N=int(sys.argv[3]); random.seed(int(sys.argv[4]) if len(sys.argv)>4 else 3)
inst=[]
for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    for p in itertools.product(range(1,m),repeat=d):
        res=[sum(x*y for x,y in zip(n,p))%m for n in Dl]
        if len(set(res))!=m: continue
        inst.append((Dl,p))
random.shuffle(inst)
for Dl,p in inst[:N]:
    S=set(Dl); T=Tvals(S,d); tgt=(d-1)*m*(m-1)//2
    ph={x:sum(a*b for a,b in zip(x,p))%m for x in Dl}
    sl=[(sum(T[x]*((s-ph[x])%m) for x in Dl)-tgt)//m for s in range(m)]
    maxi=[x for x in Dl if all(tuple(x[:a]+(x[a]+1,)+x[a+1:]) not in S for a in range(d))]
    print('D',[''.join(map(str,x)) for x in Dl],'p',p,'maximal',[''.join(map(str,x)) for x in maxi])
    for y in Dl:
        c=sl[(ph[y]-1)%m]
        comp=[m-1-ph[tuple(M[a]-y[a] for a in range(d))] for M in maxi if all(M[a]>=y[a] for a in range(d))]
        print('   y',''.join(map(str,y)),'phi',ph[y],'c(y)',c,' m-1-phi(M-y):',comp)
