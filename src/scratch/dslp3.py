# d=3 LP with extra cut x_0 = 1 ; print an optimal fractional solution when value > m-1
import sys, itertools
sys.path.insert(0,'src/scratch')
from exactlp import maximize
from math import gcd
d=int(sys.argv[1]); m=int(sys.argv[2]); cut=sys.argv[3] if len(sys.argv)>3 else 'x0'
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
worst=None; cnt=0
for p in itertools.product(range(1,m),repeat=d):
  if gcd(m,*p)!=1: continue
  # restrict region to cells whose box is phi-injective (necessary for tiles)
  Rp=[z for z in R if len({sum(x*y for x,y in zip(w,p))%m for w in itertools.product(*[range(c+1) for c in z])})==len(list(itertools.product(*[range(c+1) for c in z])))] if cut=='box' else R
  ix={z:i for i,z in enumerate(Rp)}
  dn=[(z,a) for z in Rp for a in range(d) if z[a]>=1]
  n=len(Rp)+len(dn); A=[];b=[]
  for r in range(m):
    A.append([1 if (i<len(Rp) and sum(x*y for x,y in zip(Rp[i],p))%m==r) else 0 for i in range(n)]); b.append(1)
  for k,(z,a) in enumerate(dn):
    row=[0]*n; row[ix[z]]=1; w=list(z); w[a]-=1; row[ix[tuple(w)]]=-1; row[len(Rp)+k]=1; A.append(row); b.append(0)
  row=[0]*n; row[ix[tuple([0]*d)]]=1; A.append(row); b.append(1)
  for s in range(m):
    c=[]
    for z in Rp:
        V=sum(a*b for a,b in zip(z,p)); ph=V%m
        c.append(sum(z[a] for a in range(d) if (ph-1-s)%m<p[a])-V//m)
    val,x=maximize(c+[0]*len(dn),A,b); cnt+=1
    if worst is None or val>worst[0]:
        worst=(val,p,s,{Rp[i]:str(x[i]) for i in range(len(Rp)) if x[i]!=0})
print('d',d,'m',m,'cut',cut,'LPs',cnt,'max LP',worst[0],'p,s',worst[1],worst[2])
print('   support',worst[3])
