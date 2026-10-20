"""Minimize the finite SINGLE-E witness over translations of fixed B3 Y.
Fejer only. It does not search for a UF-RELAY counterexample.
"""
from itertools import combinations_with_replacement as cr
from pathlib import Path
import json
Y=[0,1,4,13,32,71,124];T=max(Y)
YY={j:sorted({sum(x) for x in cr(Y,j)}) for j in [1,2,3]}
assert [len(YY[j]) for j in [1,2,3]]==[7,28,84]
trials=0;answer=None
for m in range(4*T+2,1499):
 for shift in range(T+1,m-3*T):
  trials+=1
  rr={0};good=True
  for j in [1,2,3]:
   ss={(j*shift+x)%m for x in YY[j]}
   if len(ss)!=len(YY[j]) or rr&ss:good=False;break
   rr|=ss
  if not good:continue
  low=max(shift+T+1,3*(shift+T)-m+1)
  high=min(2*shift,m)
  for h in range(low,high+1):
   if h-1 in rr:continue
   t=[shift+y for y in Y];core={0}
   for j in [1,2,3]:core.update(j*m+j*shift+x for x in YY[j])
   assert len(core)==120
   c=3*m+h;M=c+m-1;w=[c+(i-c)%m for i in range(m)]
   for v in core:w[v%m]=v
   E=sorted(v for v in w if v not in core);g=[m]+[m+v for v in t]+E
   ell=sum((M-v)//m for v in w);Lam=len(E)*(ell-4);W=len(g)*ell-c
   assert max(w)==M and ell==53 and all(h<=2*v and v<h for v in t)
   assert max(core)<=M and 4*(m+min(t))>M
   answer=dict(m=m,h=h,c=c,M=M,Y=Y,shift=shift,A_offsets=t,E_count=len(E),e=len(g),ell=ell,R_A=84,p_A=28,C_U=0,Lambda=Lam,Z=28,rho=m-h,R_out=0,W=W,single_E_slack=-7,UF_RELAY_slack=Lam+28-84,trials=trials)
   Path('simplex_e_small_gens.txt').write_text(' '.join(map(str,g))+'\n')
   Path('simplex_e_small_ap.txt').write_text(' '.join(map(str,w))+'\n')
   Path('simplex_e_small.json').write_text(json.dumps(answer,indent=2))
   break
  if answer:break
 if answer:break
assert answer
print(json.dumps(answer))
