"""Quick falsification of the stronger UF top-count candidate. Fejer only."""
from check import apery,evaluate
import json
cases=[[53]+list(range(85,96)),[32]+list(range(39,46)),[87]+list(range(105,123)),[5,9,12]]
for m in range(6,46):
 for a in range(1,m):
  for b in range(a+1,m):cases.append([m]+list(range(m+a,m+b+1)))
cnt=0;best=10**100;first=None
for g in cases:
 w=apery(g)
 if max(w)//g[0]!=4:continue
 r=evaluate(w);s=r['summary'];cnt+=1
 if s['TOP_strong_slack']<best:
  best=s['TOP_strong_slack'];print('TOP_RECORD',r['generators'],s,flush=True)
 if s['TOP_strong_slack']<0 and first is None:
  first=r
  with open('top_strong_counter.json','w') as out:json.dump(r,out,indent=2)
 if min(s[k] for k in ('CU_slack','PLUS_slack','POOR_slack'))<0:
  with open('criterion_counter.json','w') as out:json.dump(r,out,indent=2)
  print('CRITERION_COUNTER',s,flush=True);break
print('SUMMARY q4',cnt,'min strong top slack',best,'firstcounter',None if first is None else first['generators'],flush=True)
