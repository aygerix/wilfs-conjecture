# LP relaxation of max/min over down-set transversals of sum gamma_s(z).
import sys, itertools
sys.path.insert(0,'src/scratch')
from exactlp import maximize
from fractions import Fraction as Fr
d=int(sys.argv[1]); ms=[int(x) for x in sys.argv[2].split(',')]
def region(m):
    R=[]
    def rec(pref,prod):
        if len(pref)==d: R.append(tuple(pref)); return
        k=0
        while prod*(k+1)<=m:
            rec(pref+[k],prod*(k+1)); k+=1
    rec([],1); return R
def gam(z,p,m,s):
    V=sum(a*b for a,b in zip(z,p)); ph=V%m
    return sum(z[a] for a in range(d) if (ph-1-s)%m<p[a])-V//m
for m in ms:
  R=region(m); idx={z:i for i,z in enumerate(R)}
  down=[(z,a) for z in R for a in range(d) if z[a]>=1]
  worst_hi=-1; worst_lo=1; cnt=0; ex=None
  for p in itertools.product(range(1,m),repeat=d):
    # need some tile: skip p with gcd issues (phi not surjective)
    from math import gcd
    g=m
    for a in p: g=gcd(g,a)
    if g!=1: continue
    n=len(R)+len(down)
    A=[];b=[]
    for r in range(m):
      A.append([1 if (i<len(R) and sum(x*y for x,y in zip(R[i],p))%m==r) else 0 for i in range(n)]); b.append(1)
    for k,(z,a) in enumerate(down):
      row=[0]*n; row[idx[z]]=1; w=list(z); w[a]-=1; row[idx[tuple(w)]]=-1; row[len(R)+k]=1
      A.append(row); b.append(0)
    for s in range(m):
      c=[gam(z,p,m,s) for z in R]+[0]*len(down)
      hi,_=maximize(c,A,b); lo,_=maximize([-v for v in c],A,b)
      cnt+=1
      if hi is None: continue
      lo=-lo
      if hi>worst_hi: worst_hi=hi; ex=('hi',p,s,hi)
      if lo<worst_lo: worst_lo=lo
  print('d',d,'m',m,'|R|',len(R),'LPs',cnt,'max LP upper',worst_hi,'(m-1 =',m-1,') min LP lower',worst_lo, ex,flush=True)
