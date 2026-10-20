"""Falsify pointwise lower-cover payment at q=4. Fejer only."""
from check import apery,evaluate
import json
found=None;count=0
for m in range(3,41):
 for n in range(m+1,2*m):
  for t in range(2,9):
   K=3*m+t if t<m else 4*m
   g=[m,n,n+1,n+2]
   raw=apery(g);w=[0]+[min(raw[i],K+(i-K)%m) for i in range(1,m)]
   if max(w)//m!=4:continue
   r=evaluate(w);count+=1
   bad=[x for x in r['rows'] if x['E']>0 and x['P']>x['Eu']]
   if bad:
    found=r
    print('LOCAL_COUNTER',r['generators'],r['summary'],'bad',bad,flush=True)
    with open('local_counter.json','w') as fp:json.dump(r,fp,indent=2)
    break
  if found:break
 if found:break
print('SUMMARY tested',count,flush=True)
