"""Exact counterexample families; construct C-check inputs. Fejer only."""
import itertools,json
from pathlib import Path
out=Path('families');out.mkdir(exist_ok=True)
records=[]
def build(tag,m,coregens,D,c,expect):
 core={sum(x*n for x,n in zip(f,coregens)) for f in D}
 assert len(core)==len(D) and len({v%m for v in core})==len(D)
 M=c+m-1;rr={v%m for v in core};w=[c+(i-c)%m for i in range(m)]
 for v in core:w[v%m]=v
 assert max(w)==M
 spikes=sorted(w[i] for i in range(m) if i not in rr)
 g=[m]+coregens+spikes;e=len(g);p=M%m+1
 C=lambda y:(y-p)//m+1
 K=[]
 for f in D:
  R=sum(x*(n%m) for x,n in zip(f,coregens))
  K.append(C(R)-sum(x*(C(R)-C(R-n%m)) for x,n in zip(f,coregens) if x))
 ell=sum((M-v)//m for v in w);sk=sum(K);ex=sk-(m-e)
 assert ex==expect and min(coregens)*(max(map(sum,D))+1)>M
 W=e*ell-c;assert W>0
 row=dict(tag=tag,m=m,e=e,M=M,c=c,pstar=p,ell=ell,spikes=len(spikes),sumK=sk,bound=m-e,excess=ex,W=W)
 (out/(tag+'.txt')).write_text(str(e)+'\n'+' '.join(map(str,g))+'\n')
 if m<100:(out/(tag+'_ap.txt')).write_text(' '.join(map(str,w))+'\n')
 records.append(row)

for H in list(range(3,13))+[20,50]:
 L=H+4;m=H*H+3*H-1;r=m-L
 D=[(i,j) for i in range(H+1) for j in range(H+1-i)]
 assert len(D)==(H+1)*(H+2)//2
 build('height_'+str(H),m,[m+r,m+r+1],D,(2*H-2)*m+2,(H-1)*(H-2)//2)
 z=records[-1]
 assert z['ell']==H*(H+1)*(2*H+1)//6 and 2*z['e']==m+3

Y=[0,1,4,13,32,71,124]
for k in range(2,8):
 yy=Y[:k];tri=list(itertools.combinations_with_replacement(yy,3))
 assert len({sum(t) for t in tri})==len(tri)
 N=(k+1)*(k+2)*(k+3)//6
 threshold=max(24*max(yy)+6,2*N+1);m=8*(threshold//8+1)
 rr=[m//2+1+4*y for y in yy]
 D=[(0,)*k]
 for j in range(1,4):
  for inds in itertools.combinations_with_replacement(range(k),j):
   f=[0]*k
   for i in inds:f[i]+=1
   D.append(tuple(f))
 build('B3_'+str(k),m,[m+r for r in rr],D,4*m+2,k*(k+1)*(k-1)//6)
 z=records[-1];assert z['pstar']==2 and z['ell']==5+3*k+k*(k+1)//2
Path('families.json').write_text(json.dumps(records,indent=2))
for z in records:print(json.dumps(z))
