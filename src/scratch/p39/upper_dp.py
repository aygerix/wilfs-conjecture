"""Exact upper-side, generator-aware split bound; diagnostic of which dual signs are needed.
No LP solver. Input: certprobe JSONL. All arithmetic is integral.
"""
import json,sys
from verify_probe import open_text
for line in open_text(sys.argv[1]):
 D=json.loads(line); m,e,q,c=(D[k] for k in ('m','e','q','c'))
 to=[[] for _ in range(m)]
 for i,j,s,J,tau,lo,up in D['pairs']:
  if not J: to[s].append((i,j,up))
 z=[0]*m; z[0]=q
 for s in sorted(range(1,m),key=lambda x:D['w'][x]):
  if not to[s]: z[s]=D['mu'][s]
  else: z[s]=max([0]+[z[i]+z[j]-q-up for i,j,up in to[s]])
 violations=[(i,j,s) for i,j,s,J,tau,lo,up in D['pairs'] if not J and z[i]+z[j]-z[s]<q-lo]
 value=e*sum(z)-c
 print('G=%s W=%d UPPER=%d missing_lower=%d'%(D['generators'],D['W'],value,len(violations)))
