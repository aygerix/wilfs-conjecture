# per-cell arc multiplicities b_x(s) = #{a: s in [phi(x), phi(top_a x)) cyclic};  slack = sum_x b_x - c0
import sys, itertools, random
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); m=int(sys.argv[2]); N=int(sys.argv[3]); random.seed(5)
inst=[]
for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    for p in itertools.product(range(1,m),repeat=d):
        res=[sum(x*y for x,y in zip(n,p))%m for n in Dl]
        if len(set(res))!=m: continue
        inst.append((Dl,p))
random.shuffle(inst)
def top(D,x,a):
    y=list(x)
    while True:
        y[a]+=1
        if tuple(y) not in D: y[a]-=1; return tuple(y)
for Dl,p in inst[:N]:
    S=set(Dl); T=Tvals(S,d); tgt=(d-1)*m*(m-1)//2
    ph={x:sum(a*b for a,b in zip(x,p))%m for x in Dl}
    sl=[(sum(T[x]*((s-ph[x])%m) for x in Dl)-tgt)//m for s in range(m)]
    b={x:[sum(1 for a in range(d) if (s-ph[x])%m < (ph[top(S,x,a)]-ph[x])%m) for s in range(m)] for x in Dl}
    tot=[sum(b[x][s] for x in Dl) for s in range(m)]
    c0=tot[0]-sl[0]
    ge1=[sum(1 for x in Dl if b[x][s]>=1) for s in range(m)]
    ge2=[sum(1 for x in Dl if b[x][s]>=2) for s in range(m)]
    print('D',[''.join(map(str,x)) for x in Dl],'p',p,'c0',c0)
    print('  slack',sl); print('  >=1  ',ge1); print('  >=2  ',ge2)
