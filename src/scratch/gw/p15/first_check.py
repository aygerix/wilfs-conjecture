"""First exact falsification test for P15. Run on fejer only."""
from itertools import product
from heapq import heappush,heappop
import json
m=14;r=(8,9);p=2
D=[f for f in product(range(4),repeat=2) if sum(f)<=3]
C=lambda y:(y-p)//m+1
rows=[]
for f in sorted(D,key=lambda f:(sum(f),f)):
 R=sum(x*y for x,y in zip(f,r))
 K=C(R)-sum(f[a]*(C(R)-C(R-r[a])) for a in range(2) if f[a])
 rows.append(dict(f=f,R=R,residue=R%m,C=C(R),K=K))
assert len(set(z['residue'] for z in rows))==len(D)
assert sum(z['K'] for z in rows)==8 and sum(sum(f)>=2 for f in D)==7
gens=[14,22,23];w=[10**20]*m;w[0]=0;heap=[(0,0)]
while heap:
 v,i=heappop(heap)
 if v!=w[i]:continue
 for n in gens[1:]:
  z=v+n;j=z%m
  if z<w[j]:w[j]=z;heappush(heap,(z,j))
M=max(w);pstar=M%m+1
assert pstar==p
real=[]
for f in D:
 x=f[0]*22+f[1]*23
 assert w[x%m]==x
 nu=[]
 for n in gens[1:]:
  k=0
  while x-(k+1)*n>=0 and w[(x-(k+1)*n)%m]<=x-(k+1)*n:k+=1
  nu.append(k)
 kreal=C(x)-sum(k*(C(x)-C(x-n)) for k,n in zip(nu,gens[1:]) if k)
 real.append(dict(f=f,x=x,nu=nu,K=kreal))
assert sum(z['K'] for z in real)==8
answer=dict(m=m,r=r,p=p,D=rows,sumK=8,decomposables=7,generators=gens,Ap=w,M=M,c=M-m+1,pstar=pstar,real_downset=sorted(real,key=lambda z:z['x']))
print(json.dumps(answer,indent=2))

for gg in [[14,22,23,57,61,62,63],[14,22,23,61,62,63,71]]:
 ww=[10**20]*14;ww[0]=0;hh=[(0,0)]
 while hh:
  x,i=heappop(hh)
  if ww[i]!=x:continue
  for n in gg[1:]:
   y=x+n;j=y%14
   if y<ww[j]:ww[j]=y;heappush(hh,(y,j))
 mm=max(ww);ps=mm%14+1;bad=[]
 for pp in range(1,15):
  cfun=lambda y:(y-pp)//14+1
  kval=[]
  for x in ww:
   kk=cfun(x)
   for n in gg[1:]:
    dep=0
    while x-(dep+1)*n>=0 and ww[(x-(dep+1)*n)%14]<=x-(dep+1)*n:dep+=1
    if dep:kk-=dep*(cfun(x)-cfun(x-n))
   kval.append(kk)
  if sum(kval)>14-len(gg):bad.append(dict(p=pp,K=kval,sumK=sum(kval)))
 assert bad and any(z['p']==2 and z['sumK']==8 for z in bad)
 ll=sum((mm-x)//14 for x in ww);cc=mm-13
 print(json.dumps(dict(generators=gg,Ap=ww,M=mm,c=cc,pstar=ps,e=len(gg),ell=ll,W=len(gg)*ll-cc,bad_shifts=bad)))
