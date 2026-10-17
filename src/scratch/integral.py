# Is the down-set transversal polytope integral?  Random integer objectives; check optimal vertex is 0/1.
import sys, itertools, random
sys.path.insert(0,'src/scratch')
from exactlp import maximize
from math import gcd
d=int(sys.argv[1]); m=int(sys.argv[2]); trials=int(sys.argv[3]); random.seed(7)
def region(m):
    R=[]
    def rec(pref,prod):
        if len(pref)==d: R.append(tuple(pref)); return
        k=0
        while prod*(k+1)<=m:
            rec(pref+[k],prod*(k+1)); k+=1
    rec([],1); return R
R=region(m); idx={z:i for i,z in enumerate(R)}
down=[(z,a) for z in R for a in range(d) if z[a]>=1]
frac=0; tot=0; ex=None
ps=[p for p in itertools.product(range(1,m),repeat=d) if gcd(m,*p)==1]
for t in range(trials):
    p=random.choice(ps)
    n=len(R)+len(down); A=[];b=[]
    for r in range(m):
        A.append([1 if (i<len(R) and sum(x*y for x,y in zip(R[i],p))%m==r) else 0 for i in range(n)]); b.append(1)
    for k,(z,a) in enumerate(down):
        row=[0]*n; row[idx[z]]=1; w=list(z); w[a]-=1; row[idx[tuple(w)]]=-1; row[len(R)+k]=1
        A.append(row); b.append(0)
    c=[random.randint(-5,5) for _ in R]+[0]*len(down)
    val,x=maximize(c,A,b)
    if val is None: continue
    tot+=1
    xs=x[:len(R)]
    if any(v not in (0,1) for v in xs):
        frac+=1
        if ex is None: ex=(p,{R[i]:str(v) for i,v in enumerate(xs) if v!=0})
print('d',d,'m',m,'LPs',tot,'fractional optimal vertices',frac,ex)
