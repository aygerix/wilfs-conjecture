"""Check a C assignment certificate against independently audited certprobe data.
usage: python3 verify_matching.py matching.jsonl probe.jsonl [more_probe.jsonl ...]
       python3 verify_matching.py --standalone matching.jsonl
The standalone audit reconstructs S by membership and heap Dijkstra and streams
the repair rows; it requires neither Gurobi data nor a dense matching matrix.
"""
import sys,json
from fractions import Fraction as F
from verify_probe import audit,open_text
def transport_audit(C,w,mu,b,q,r,rho,gr):
 m=len(w);delta=[v-a for v,a in zip(mu,b)];order=sorted(range(1,m),key=w.__getitem__)
 top_ideal=[s for s in range(m) if w[s]+w[(r-s)%m]==w[r]]
 reports=[]
 for name in C['transport']:
  assert name in ('generators','zero_loss','capped_pairs')
  costs=[{} for _ in range(m)];used=set()
  for ii,i in enumerate(order):
   if 2*w[i]>w[r]:break
   for j in order[ii:]:
    if w[i]+w[j]>w[r]:break
    s=(i+j)%m
    if not s or w[i]+w[j]!=w[s]:continue
    tau=mu[i]+mu[j]-mu[s]-q
    lo=int((w[s]-C['c'])%m>=m-rho and i>r and j>r)
    a=tau+lo
    k=int(i<=r and j<=r and i+j<=2*r-m)+int(i>r and j>r and i+j<=m+r)
    assert a in (0,1) and k in (0,1) and a+k<=1
    for anchor,v in ((i,j),(j,i)):
     if name!='capped_pairs' and not (anchor in gr if name=='generators' else delta[anchor]==0):continue
     used.add(anchor)
     forward=k+(delta[anchor] if name=='capped_pairs' else 0)
     costs[s][v]=min(costs[s].get(v,10**100),a)
     costs[v][s]=min(costs[v].get(s,10**100),forward)
  T=C['transport'][name];u=T['u'];parent=T['parent']
  assert len(u)==len(parent)==m and all(type(v) is int for v in u+parent)
  assert u[0]==0 and all(0<=u[i]<=delta[i] for i in range(m))
  for i in range(m):
   for j,cost in costs[i].items():assert u[j]<=u[i]+cost
   p=parent[i];assert -1<=p<m
   if p==-1:assert u[i]==delta[i]
   else:assert i in costs[p] and u[i]==u[p]+costs[p][i]
   seen=set();v=i
   while parent[v]!=-1:
    assert v not in seen;seen.add(v);v=parent[v]
  assert T.get('used_composite_summands',T.get('used_composite_anchors'))==len(used-gr)
  assert T['unpaid']==sum(u) and T['bound']==C['W']-C['e']*sum(u)
  if name=='capped_pairs':assert all(u[s]==0 for s in top_ideal)
  reports.append('%s=%d[unpaid:%d,composites:%d]'%(name,T['bound'],sum(u),len(used-gr)))
 return 'TRANSPORT CERTIFIED G=%s W=%d top_ideal=%d | '%(sorted(C['G']),C['W'],len(top_ideal))+' '.join(reports)

def standalone(C):
 import heapq, math
 G=sorted(C['G']);m=C['m'];e=C['e']
 assert len(G)==len(set(G)) and m==min(G) and math.gcd(*G)==1
 # Stop after m consecutive members: closure under +m proves all later membership.
 member=bytearray([1]);run=0;x=0
 while run<m:
  x+=1;yes=any(x>=g and member[x-g] for g in G)
  member.append(yes);run=run+1 if yes else 0
 c=x-m+1;genus=sum(not v for v in member[:c])
 minimal=[g for g in G if not any(g>a and member[g-a] for a in G)]
 assert minimal==G and e==len(G) and C['c']==c
 assert C['W']==e*(c-genus)-c
 wm=[None]*m
 for a,v in enumerate(member):
  if v and wm[a%m] is None:wm[a%m]=a
 w=[10**100]*m;w[0]=0;todo=[(0,0)]
 while todo:
  val,s=heapq.heappop(todo)
  if val!=w[s]:continue
  for g in G[1:]:
   v=val+g;t=v%m
   if v<w[t]:w[t]=v;heapq.heappush(todo,(v,t))
 assert wm==w and max(w)-m+1==c
 q=(c+m-1)//m;rho=q*m-c;r=w.index(max(w))
 mu=[max(0,(c-v+m-1)//m) for v in w];assert sum(mu)==c-genus
 gr={g%m for g in G[1:]};b=[0]*m;b[0]=q
 penalty=[0]*m;length=[0]*m
 order=sorted(range(1,m),key=w.__getitem__)
 for s in order:
  b[s]=mu[s] if s in gr else 0
  penalty[s]=0 if s in gr else m*m
  length[s]=1 if s in gr else m
  for i in order:
   if 2*w[i]>w[s]:break
   j=(s-i)%m
   if not j or w[i]+w[j]!=w[s]:continue
   up=int((w[s]-c)%m<=m-rho-2 and i<=r and j<=r)
   tau=((w[i]-c)%m+(w[j]-c)%m-(w[s]-c)%m-rho)//m
   assert mu[i]+mu[j]-mu[s]==q+tau and up-tau in (0,1)
   closed_cost=int(i<=r and j<=r and i+j<=2*r-m)+int(i>r and j>r and i+j<=m+r)
   assert up-tau==closed_cost
   penalty[s]=min(penalty[s],penalty[i]+penalty[j]+up-tau)
   length[s]=min(length[s],length[i]+length[j])
   b[s]=max(b[s],b[i]+b[j]-q-up)
  assert penalty[s]<=length[s]-1
  assert b[s]==max(0,mu[s]-penalty[s])
 assert b==C['b'] and all(0<=a<=v for a,v in zip(b,mu))
 free={a for a in gr if (a<=r and a>=max(1,2*r-m)) or a==m-1}
 active=[0]*m
 for s in order:
  active[s]=min(active[(s-g%m)%m]+int(g%m not in free) for g in G[1:] if w[(s-g%m)%m]+g==w[s])
  assert mu[s]-b[s]<=max(0,active[s]-1)
 assert C['B']==e*sum(b)-c
 if 'transport' in C:return transport_audit(C,w,mu,b,q,r,rho,gr)
 res=[s for s in range(1,m) if s not in gr];assert C['residues']==res
 n=len(res);ix={s:a for a,s in enumerate(res)}
 cover_mode='cover' in C
 if cover_mode:
  v=C['cover'];assert len(v)==n and all(type(a) is int and a>=0 for a in v)
 else:
  p=C['permutation'];alpha=C['alpha'];beta=C['beta']
  assert len(alpha)==len(beta)==n and sorted(p)==list(range(n))
  assert all(type(v) is int for v in alpha+beta)
  assert min(alpha,default=0)+min(beta,default=0)>=0
 selected=[0]*n;actual=[mu[s]-b[s] for s in res]
 capacity_mode='capacity_lower' in C
 forced=[0]*n;diagonal=[0]*n;positive_edges=[]
 def edge(a,z,d):
  assert actual[a]+actual[z]>=d
  if capacity_mode:
   forced[a]=max(forced[a],d-actual[z]);positive_edges.append((a,z,d))
   if a==z:diagonal[a]=max(diagonal[a],d)
  if cover_mode:assert v[a]+v[z]>=d
  else:
   assert alpha[a]+beta[z]>=d
   if p[a]==z:selected[a]=max(selected[a],d)
 for ii,i in enumerate(order):
  if 2*w[i]>w[r]:break
  for jj in range(ii,len(order)):
   j=order[jj]
   if w[i]+w[j]>w[r]:break
   s=(i+j)%m
   if not s or w[i]+w[j]!=w[s]:continue
   rp=(w[s]-c)%m
   lo=int(rp>=m-rho and i>r and j>r)
   up=int(rp<=m-rho-2 and i<=r and j<=r)
   assert q-lo<=mu[i]+mu[j]-mu[s]<=q+up
   d=q-lo-b[i]-b[j]+b[s]
   if d<=0:continue
   a,z=ix.get(i),ix.get(j)
   assert a is not None or z is not None
   if a is None or z is None:
    a=z if a is None else a;edge(a,a,2*d)
   else:edge(a,z,d);edge(z,a,d)
 loss=sum(v-a for v,a in zip(mu,b))
 assert C['W']-C['B']==e*loss
 if cover_mode:
  total=sum(v);upper=C['B']+e*total
  assert total==C['cover_sum'] and upper==C['matching_bound_upper']
  return 'VERIFIED ASSIGNMENT UPPER CERTIFICATE G=%s c=%d B=%d loss=%d cover_sum=%d matching_bound_upper=%d W=%d'%(G,c,C['B'],loss,total,upper,C['W'])
 M=sum(selected);assert M==C['M']==sum(alpha)+sum(beta)
 assert 2*sum(actual)>=M
 corrected=C['B']+e*((M+1)//2)
 assert corrected==C['corrected']<=C['W']
 assert C['W']-C['B']==e*loss and M<=2*loss
 active_budget=sum(min(mu[s],max(0,active[s]-1)) for s in range(1,m))
 result='INDEPENDENTLY CERTIFIED G=%s c=%d B=%d M=%d loss=%d bound=%d W=%d free_generators=%d active_budget=%d'%(G,c,C['B'],M,loss,corrected,C['W'],len(free),active_budget)
 if capacity_mode:
  assert forced==C['capacity_lower']
  if 'individual_lower' in C:
   individual=[max(forced[a],(diagonal[a]+1)//2) for a in range(n)]
   assert individual==C['individual_lower'] and all(individual[a]<=actual[a] for a in range(n))
   ib=C['B']+e*sum(individual);assert ib==C['individual_bound']<=C['W']
   result+=' individual_bound=%d'%ib
  cp=C['capacity_permutation'];ca=C['capacity_alpha'];cb=C['capacity_beta']
  assert sorted(cp)==list(range(n)) and len(ca)==len(cb)==n
  assert all(type(v) is int for v in ca+cb)
  assert min(ca,default=0)+min(cb,default=0)>=0
  capselected=[0]*n
  for a,z,d in positive_edges:
   h=max(0,d-forced[a]-forced[z]);assert ca[a]+cb[z]>=h
   if cp[a]==z:capselected[a]=max(capselected[a],h)
  cm=sum(capselected);assert cm==C['capacity_M']==sum(ca)+sum(cb)
  twice=2*sum(forced)+cm;assert twice==C['capacity_value_twice']>=M
  assert twice-M==C['capacity_gap_twice']
  repair=[F(2*forced[a]+ca[a]+cb[a],2) for a in range(n)]
  assert all(0<=repair[a]<=actual[a] for a in range(n))
  assert 2*sum(repair)==twice
  for a,z,d in positive_edges:assert repair[a]+repair[z]>=d
  result+=' bounded_cover_twice=%d capacity_gap_twice=%d'%(twice,twice-M)
 return result

if len(sys.argv)>1 and sys.argv[1]=='--standalone':
 for path in sys.argv[2:]:
  for line in open_text(path):
   if line.startswith('{'):print(standalone(json.loads(line)))
 sys.exit(0)

D={}
for path in sys.argv[2:]:
 for line in open_text(path):
  x=json.loads(line); report=audit(x);D[tuple(sorted(x['generators']))]=(x,report)
for line in open_text(sys.argv[1]):
 if not line.startswith('{'):continue
 C=json.loads(line);S,R=D[tuple(sorted(C['G']))];m,e,q,c=(S[k] for k in ('m','e','q','c'))
 if 'transport' in C:
  print(standalone(C))
  assert C['transport']['generators']['bound']<=F(R['models']['UA3']['optimum'])
  continue
 gr={g%m for g in S['generators'] if g!=m};to=[[] for _ in range(m)]
 for i,j,s,J,tau,lo,up in S['pairs']:
  if not J:to[s].append((i,j,up))
 b=[0]*m;b[0]=q
 for s in sorted(range(1,m),key=lambda k:S['w'][k]):
  b[s]=S['mu'][s] if s in gr else max([0]+[b[i]+b[j]-q-up for i,j,up in to[s]])
 assert b==C['b'] and e*sum(b)-c==C['B']
 res=[s for s in range(1,m) if s not in gr];assert res==C['residues'];ix={s:i for i,s in enumerate(res)};n=len(res)
 w=[[0]*n for _ in range(n)]
 for i,j,s,J,tau,lo,up in S['pairs']:
  if J:continue
  d=q-lo-b[i]-b[j]+b[s]
  if d<=0:continue
  a,z=ix.get(i),ix.get(j)
  if a is None or z is None:
   assert a is not None or z is not None
   t=z if a is None else a;w[t][t]=max(w[t][t],2*d)
  else:w[a][z]=w[z][a]=max(w[a][z],d)
 p=C['permutation'];alpha=C['alpha'];beta=C['beta'];assert sorted(p)==list(range(n))
 value=sum(w[i][p[i]] for i in range(n));assert value==C['M']==sum(alpha)+sum(beta)
 for i in range(n):
  for j in range(n):assert alpha[i]+beta[j]>=w[i][j]
 cover=[F(alpha[i]+beta[i],2) for i in range(n)]
 assert min(cover,default=0)>=0
 for i in range(n):
  for j in range(n):assert cover[i]+cover[j]>=w[i][j]
 assert sum(cover)==F(value,2)
 t=[S['mu'][s]-b[s] for s in res];assert min(t,default=0)>=0
 for i in range(n):
  for j in range(n):assert t[i]+t[j]>=w[i][j]
 fractional=C['B']+F(e*value,2);rounded=C['B']+e*((value+1)//2)
 assert fractional<=F(R['models']['UA3']['optimum']) and rounded==C['corrected']<=S['W']
 print('CERTIFIED G=%s B=%d M=%d corrected=%d UA3=%s W=%d'%(C['G'],C['B'],value,rounded,R['models']['UA3']['optimum'],S['W']))
