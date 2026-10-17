# Is there an optimal dual with 0 <= u_r <= 1 ?  (sum u = m-1)  Report which residue gets u<1.
import sys, itertools
sys.path.insert(0,'src/scratch')
from exactlp import maximize
from math import gcd
d=int(sys.argv[1]); m=int(sys.argv[2]); mode=sys.argv[3] if len(sys.argv)>3 else 'upper'
def region(m):
    R=[]
    def rec(pref,prod):
        if len(pref)==d: R.append(tuple(pref)); return
        k=0
        while prod*(k+1)<=m:
            rec(pref+[k],prod*(k+1)); k+=1
    rec([],1); return R
R=region(m); E=[(z,a) for z in R for a in range(d) if z[a]>=1]
tot=ok=0; bad=[]
for p in itertools.product(range(1,m),repeat=d):
  g=m
  for a in p: g=gcd(g,a)
  if g!=1: continue
  phi={z:sum(a*b for a,b in zip(z,p))%m for z in R}
  for s in range(m):
    gm={}
    for z in R:
        V=sum(a*b for a,b in zip(z,p)); ph=V%m
        gm[z]=sum(z[a] for a in range(d) if (ph-1-s)%m<p[a])-V//m
    if mode=='lower': gm={z:-v for z,v in gm.items()}
    target=m-1 if mode=='upper' else 0
    # vars: u (m, >=0), w (m slack for u<=1), f (|E|), sl (|R|)
    nv=2*m+len(E)+len(R); A=[];b=[]
    A.append([1]*m+[0]*(nv-m)); b.append(target)
    for r in range(m):
        row=[0]*nv; row[r]=1; row[m+r]=1; A.append(row); b.append(1 if mode=='upper' else 0)
    for zi,z in enumerate(R):
        row=[0]*nv; row[phi[z]]+=1
        for k,(w,a) in enumerate(E):
            if w==z: row[2*m+k]+=1
            zz=list(w); zz[a]-=1
            if tuple(zz)==z: row[2*m+k]-=1
        row[2*m+len(E)+zi]=-1; A.append(row); b.append(gm[z])
    val,x=maximize([0]*nv,A,b)
    tot+=1
    if val is not None: ok+=1
    elif len(bad)<5: bad.append((p,s))
print('d',d,'m',m,mode,'instances',tot,'with 0<=u<=1 dual:',ok,'fail examples',bad)
