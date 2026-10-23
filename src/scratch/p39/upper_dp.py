"""Exact upper-side, generator-aware split bound; diagnostic of which dual signs are needed.
No LP solver. Input: certprobe JSONL. Exact integer/rational arithmetic.
"""
import json,sys
from fractions import Fraction as F
from verify_probe import open_text
if len(sys.argv)>1 and sys.argv[1]=='--chain-budget':
 # Analyze already audited semigroup/certificate data against the recorded CH
 # identity. This is an exact diagnostic, not a new semigroup membership audit.
 certificates={}
 for path in sys.argv[3:]:
  for line in open_text(path):
   C=json.loads(line);key=tuple(sorted(C['G']))
   assert C.get('integer') and 'residual_matching' in C
   if key not in certificates or C['residual_matching']['rounded_bound']>certificates[key]['residual_matching']['rounded_bound']:certificates[key]=C
 for line in open_text(sys.argv[2]):
  D=json.loads(line);G=sorted(D['generators']);C=certificates[tuple(G)]
  m,e=D['m'],D['e'];w=D['w'];M=max(w);total=sum(w);deficits=[];excess=-total
  order=sorted(range(1,m),key=w.__getitem__);counts=[0]*m;counts[0]=1
  for g in G[1:]:
   nu=sum(max(k for k in range(v//g+1) if w[(v-k*g)%m]==v-k*g) for v in w)
   deficits.append(m*M-total-g*nu);excess+=g*nu
   # Coin-change by generator order counts each commutative factorization once.
   for s in order:
    t=(s-g)%m
    if w[t]+g==w[s]:counts[s]+=counts[t]
  correction=(e-2)*m*(m-1)//2
  assert min(deficits)>=0 and excess>=0 and all(v>0 for v in counts)
  unique=all(v==1 for v in counts);assert unique==(excess==0)
  assert sum(deficits)+excess-correction==m*D['W']
  R=C['unpaid']-(C['residual_matching']['M']+1)//2
  assert sum(deficits)+excess-correction-e*m*R==m*C['residual_matching']['rounded_bound']
  print(json.dumps({'G':G,'m':m,'e':e,'c':D['c'],'g':D['g'],'W':D['W'],'unique_apery_factorizations':unique,'excess':excess,'chain_deficits':deficits,'correction':correction,'unpaid_remainder':R,'proposed_excess_payment':e*m*R,'bound':C['residual_matching']['rounded_bound'],'max_factorizations':max(counts)}))
 sys.exit(0)
propagate=len(sys.argv)>1 and sys.argv[1]=='--propagate'
rigid=len(sys.argv)>1 and sys.argv[1]=='--rigid'
for line in open_text(sys.argv[2] if propagate or rigid else sys.argv[1]):
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
 if rigid:
  delta=[u-b for u,b in zip(D['mu'],z)]
  fixed={s for s,v in enumerate(delta) if not v};initial=len(fixed);sweeps=0
  while True:
   old=fixed.copy();sweeps+=1
   for i,j,s,J,tau,l,u in D['pairs']:
    if J:continue
    if tau+l==0 and s in fixed:fixed.update((i,j))
    if u-tau==0 and i in fixed and j in fixed:fixed.add(s)
   if old==fixed:break
  remaining=[(s,delta[s]) for s in range(m) if s not in fixed]
  bound=D['W']-e*sum(v for s,v in remaining)
  print('RIGID initial=%d fixed=%d/%d sweeps=%d bound=%d remaining=%s'%(initial,len(fixed),m,sweeps,bound,remaining))
  continue
 if not propagate:continue
 # All bounds are rational bounds on every UA3-feasible y, not integer rounding.
 lo=list(map(F,z));hi=[F(q)]+[None]*(m-1)
 gr={g%m for g in D['generators'] if g!=m}
 for s in sorted(range(1,m),key=lambda x:D['w'][x]):
  hi[s]=F(D['mu'][s]) if s in gr else min(hi[i]+hi[j]-q+l for i,j,t,J,tau,l,u in D['pairs'] if t==s and not J)
 tight=[p for p in D['pairs'] if not p[3]]
 for sweep in range(41):
  bound=e*sum(lo)-c
  assert all(lo[s]<=D['mu'][s]<=hi[s] for s in range(m))
  if 'UA3' in D['models']:
   from verify_probe import rat
   assert bound<=rat(D['models']['UA3']['value'])
  print('PROPAGATE sweep=%d bound=%s exact_coordinates=%d/%d'%(sweep,bound,sum(a==v==b for a,v,b in zip(lo,D['mu'],hi)),m))
  if sweep==40:break
  old=(lo.copy(),hi.copy())
  for i,j,s,J,tau,l,u in tight:
   L=q-l;U=q+u
   if i==j:
    lo[i]=max(lo[i],(L+lo[s])/2)
    hi[i]=min(hi[i],(U+hi[s])/2)
    lo[s]=max(lo[s],2*lo[i]-U)
    hi[s]=min(hi[s],2*hi[i]-L)
   else:
    lo[i]=max(lo[i],L+lo[s]-hi[j])
    lo[j]=max(lo[j],L+lo[s]-hi[i])
    hi[s]=min(hi[s],hi[i]+hi[j]-L)
    lo[s]=max(lo[s],lo[i]+lo[j]-U)
    hi[i]=min(hi[i],U+hi[s]-lo[j])
    hi[j]=min(hi[j],U+hi[s]-lo[i])
  if old==(lo,hi):print('INTERVAL_FIXED_POINT');break
