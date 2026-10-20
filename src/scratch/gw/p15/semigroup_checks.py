"""P15 exact all-shift T1/TAIL/T1-DOWN and reduction checks. Fejer only.
Heap Dijkstra, literal depths, capacitated below-poset matching; no tile input.
"""
import heapq,itertools,json,random,math,bisect
from collections import Counter,deque
from pathlib import Path

def apery(g):
 m=min(g);w=[10**30]*m;w[0]=0;hp=[(0,0)]
 while hp:
  v,i=heapq.heappop(hp)
  if v!=w[i]:continue
  for n in g:
   u=v+n;j=u%m
   if u<w[j]:w[j]=u;heapq.heappush(hp,(u,j))
 assert max(w)<10**30
 return w

def below_flow(pos,neg,w):
 # Integral Edmonds-Karp residual graph. Left/right capacities not expanded.
 m=len(w);left=list(pos);right=list(neg);N=len(left)+len(right)+2;t=N-1
 cap=[[0]*N for _ in range(N)];adj=[[] for _ in range(N)]
 def edge(i,j,c):cap[i][j]=c;adj[i].append(j);adj[j].append(i)
 need=sum(pos.values());INF=need+sum(neg.values())+1
 for i,v in enumerate(left,1):
  edge(0,i,pos[v])
  for j,u in enumerate(right,len(left)+1):
   if v>u and w[(v-u)%m]<=v-u:edge(i,j,INF)
 for j,u in enumerate(right,len(left)+1):edge(j,t,neg[u])
 flow=0
 while True:
  parent=[-1]*N;parent[0]=0;q=deque([0])
  while q and parent[t]<0:
   i=q.popleft()
   for j in adj[i]:
    if cap[i][j]>0 and parent[j]<0:parent[j]=i;q.append(j)
  if parent[t]<0:break
  add=INF;j=t
  while j: i=parent[j];add=min(add,cap[i][j]);j=i
  j=t
  while j:i=parent[j];cap[i][j]-=add;cap[j][i]+=add;j=i
  flow+=add
 if flow==need:return flow,[]
 seen={0};q=deque([0])
 while q:
  i=q.popleft()
  for j in adj[i]:
   if cap[i][j]>0 and j not in seen:seen.add(j);q.append(j)
 bad=[v for i,v in enumerate(left,1) if i in seen]
 D=[u for u in w if any(u<=v and w[(v-u)%m]<=v-u for v in bad)]
 return flow,sorted(D)

stats=Counter();records={};bestkeys={}
def record(kind,data,key):
 if kind not in bestkeys or key<bestkeys[kind]:
  bestkeys[kind]=key;records[kind]=data
  print('RECORD',kind,json.dumps({k:data[k] for k in ['generators','m','g','M','pstar','p'] if k in data}),flush=True)

def check(w,tag):
 m=len(w);M=max(w);order=sorted(w);have=set(w);ns=[]
 for v in order[1:]:
  if not any(v>=n and w[(v-n)%m]<=v-n for n in ns):ns.append(v)
 e=len(ns)+1;ell=sum((M-v)//m for v in w);c=M-m+1;genus=c-ell
 stats['semigroups']+=1;stats['all_shifts']+=m
 nu={};J={};F={0:(0,)*len(ns)}
 for v in order:
  dep=[]
  for n in ns:
   k=0
   while v-(k+1)*n>=0 and w[(v-(k+1)*n)%m]<=v-(k+1)*n:k+=1
   dep.append(k)
  nu[v]=dep;J[v]=sum(k+1 for n,k in zip(ns,dep) if v+n not in have)-e
  if v:
   cand=[]
   for a,n in enumerate(ns):
    if v-n in have:
     f=list(F[v-n]);f[a]+=1;cand.append(tuple(f))
   F[v]=max(cand)
  assert all(k>=f for k,f in zip(dep,F[v]))
 assert sum(J.values())==-m
 dec=set(w)-set(ns)-{0};q=M//m;pstar=M%m+1
 LT=0
 for v in w:
  for n in ns:
   t=v
   while t+n in have:t+=n
   LT+=(M-t)//m
 data=dict(tag=tag,generators=[m]+ns,m=m,e=e,Ap=w,M=M,c=c,g=genus,pstar=pstar,ell=ell,Lambda=LT,W=e*ell-c)
 if data['W']<0:print('WILF_COUNTEREXAMPLE',json.dumps(data),flush=True);raise RuntimeError('Stop: Wilf counterexample')
 st1=sdown=stail=False
 for p in range(1,m+1):
  C=lambda y:(y-p)//m+1
  K={v:C(v)-sum(k*(C(v)-C(v-n)) for k,n in zip(nu[v],ns) if k) for v in w}
  assert K[0]==0 and all(K[n]==0 for n in ns)
  assert sum(K.values())==-sum(J[v]*C(v) for v in w)
  # The lex reduction and cancellation are checked separately at every shift.
  for v in w:
   f=F[v];R=sum(a*(n%m) for a,n in zip(f,ns))
   ku=C(R)-sum(a*(C(R)-C(R-n%m)) for a,n in zip(f,ns) if a)
   kf=C(v)-sum(a*(C(v)-C(v-n)) for a,n in zip(f,ns) if a)
   assert ku==kf and K[v]<=ku
  excess=sum(K.values())-len(dec)
  if p==pstar:
   assert K=={v:q-(M-v)//m-sum(k*((M-v+n)//m-(M-v)//m) for k,n in zip(nu[v],ns) if k) for v in w}
   assert data['W']==q*m-c+LT-sum(K.values())
  if excess>0:
   stats['T1_bad_shifts']+=1;st1=True
   if p==pstar:stats['T1_true_bad']+=1
   record('T1_true' if p==pstar else 'T1_other',dict(data,p=p,K=K,sumK=sum(K.values()),bound=len(dec),excess=excess),(m,genus,e,p))
  # Q computed from J; all suffixes on each congruence class beyond m.
  suff=0;qs=[];top=p+m*((M-p)//m)
  for z in range(top,m,-m):
   Q=-sum(J[v] for v in w if v>=z);suff+=Q;qs.append((z,Q,suff))
   if suff>0:
    stats['TAIL_bad_suffixes']+=1;stail=True
    record('TAIL',dict(data,p=p,y=z,Q_samples=sorted(qs),suffix=suff,J=J),(m,genus,e,p,z))
  assert suff==excess
  pos={v:K[v]-1 for v in dec if K[v]>1}
  if pos:
   stats['matching_shifts']+=1
   neg={v:1-K[v] for v in dec if K[v]<1}
   flow,D=below_flow(pos,neg,w)
   if flow<sum(pos.values()):
    stats['DOWN_bad_shifts']+=1;sdown=True
    assert sum(K[v] for v in D)>len(set(D)&dec)
    fd={F[v] for v in D}
    for f in fd:
     for a,t in enumerate(f):
      if t:
       ff=list(f);ff[a]-=1;assert tuple(ff) in fd
    record('DOWN',dict(data,p=p,D=D,K_D={v:K[v] for v in D},sumK_D=sum(K[v] for v in D),dec_D=len(set(D)&dec),deficit=sum(pos.values()),flow=flow,lex_ideal=sorted(fd)),(m,genus,e,len(D),p))
 stats['T1_bad_semigroups']+=st1;stats['DOWN_bad_semigroups']+=sdown;stats['TAIL_bad_semigroups']+=stail
 return dict(data,K_true={v:q-(M-v)//m-sum(k*((M-v+n)//m-(M-v)//m) for k,n in zip(nu[v],ns) if k) for v in w})

named={}
for g in [[13,22,23,50,51,60],[13,22,23],[14,22,23],[14,22,23,57,61,62,63],[14,22,23,61,62,63,71],[14,22,23,48,49,57,61],[7,10,32]]:
 named[str(g)]=check(apery(g),'named')
for m in range(14,61,2):
 core=[m,3*m//2+1,3*m//2+2]
 check(apery(core),'two_high_directions')
 cap=4*m+2;w=apery(core)
 w=[min(v,cap+(i-cap)%m) if i else 0 for i,v in enumerate(w)]
 check(w,'spike_completion')
for t in range(4,20):
 m=3*t+1;w=apery([m,5*t+2,5*t+3]);cap=13*t+5
 w=[min(v,cap+(i-cap)%m) if i else 0 for i,v in enumerate(w)]
 ans=check(w,'mod13_family')
 assert ans['M']==16*t+5 and ans['pstar']==t+1 and ans['W']==29*t-89 and sum(ans['K_true'].values())==8
rng=random.Random(150022)
for it in range(350):
 m=rng.randrange(10,128);mode=it%4
 if mode<2:
  mult=rng.randrange(1,5);first=rng.randrange(1,m);length=rng.randrange(2,max(3,m//4))
  g=[m]+[mult*m+first+j for j in range(length)]
  if mode==1:g.append(m+rng.randrange(1,m))
 else:
  k=rng.randrange(2,9);mult=rng.randrange(2,9)
  g=[m,m+1]+[rng.randrange(m+1,mult*m) for _ in range(k)]
 w=apery(g)
 if it%3==0:
  cap=rng.randrange(2,11)*m+rng.randrange(1,m)
  w=[min(v,cap+(i-cap)%m) if i else 0 for i,v in enumerate(w)]
 check(w,'structured_or_random_'+str(it))
Path('semigroup_checks.json').write_text(json.dumps(dict(stats=stats,records=records,named=named),indent=2))
print('SUMMARY',json.dumps(stats,sort_keys=True))
