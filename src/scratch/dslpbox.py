# LP over cells with phi-injective boxes, constraints: one per class, down-closed, x0=1. Upper and lower.
import sys, itertools
sys.path.insert(0,'src/scratch')
from exactlp import maximize
from math import gcd, prod
d=int(sys.argv[1]); m=int(sys.argv[2])
def region(m):
    R=[]
    def rec(pref,pr):
        if len(pref)==d: R.append(tuple(pref)); return
        k=0
        while pr*(k+1)<=m:
            rec(pref+[k],pr*(k+1)); k+=1
    rec([],1); return R
R0=region(m)
hi=None; lo=None; cnt=0
for p in itertools.product(range(1,m),repeat=d):
  if gcd(m,*p)!=1: continue
  Rp=[z for z in R0 if len({sum(x*y for x,y in zip(w,p))%m for w in itertools.product(*[range(c+1) for c in z])})==prod(c+1 for c in z)]
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
    v1,x1=maximize(c+[0]*len(dn),A,b)
    if v1 is None: continue
    v2,x2=maximize([-t for t in c]+[0]*len(dn),A,b); v2=-v2; cnt+=1
    if hi is None or v1>hi[0]: hi=(v1,p,s,{Rp[i]:str(x1[i]) for i in range(len(Rp)) if x1[i]!=0})
    if lo is None or v2<lo[0]: lo=(v2,p,s,{Rp[i]:str(x2[i]) for i in range(len(Rp)) if x2[i]!=0})
print('d',d,'m',m,'LPs',cnt,'max LP',hi[0],'(m-1=%d)'%(m-1),'min LP',lo[0],flush=True)
if hi[0]>m-1: print('   hi witness',hi[1:])
if lo[0]<0: print('   lo witness',lo[1:])
