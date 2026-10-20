"""Independent random checks of the sharp height-three replacement for U.
Includes noninjective inputs: this positive theorem does not need injectivity.
Run on fejer only.
"""
import random,itertools,json
from collections import Counter
rng=random.Random(150033);stats=Counter()
def test(D,r,m):
 d=len(r);dec=sum(sum(f)>=2 for f in D)
 R={f:sum(x*y for x,y in zip(f,r)) for f in D}
 for p in range(1,m+1):
  C=lambda y:(y-p)//m+1
  K={f:C(R[f])-sum(f[a]*(C(R[f])-C(R[f]-r[a])) for a in range(d) if f[a]) for f in D}
  assert all(K[f]<=1 for f in D if sum(f)<=2)
  beta=[f for f in D if K[f]==2]
  assert all(sum(f)==3 for f in beta) and max(K.values())<=2
  P=set();edges=set();vertices=set()
  for f in beta:
   ff=[i for i,x in enumerate(f) for _ in range(x)]
   for pair in itertools.combinations(ff,2):
    edge=tuple(sorted(pair));edges.add(edge);vertices.update(edge)
   for a,x in enumerate(f):
    if x:
     z=list(f);z[a]-=1;z=tuple(z);P.add(z)
     assert K[z]==0 and C(R[z])==2
  assert len(P)==len(edges)
  ex=sum(K.values())-dec;k=len(vertices)
  assert ex<=len(beta)-len(P)<=k*(k+1)*(k-1)//6
  adj={i:set() for i in vertices}
  for i,j in edges:adj[i].add(j);adj[j].add(i)
  seen=set();pseudo=True
  for root in vertices:
   if root in seen:continue
   todo=[root];seen.add(root);vs=set()
   for i in todo:
    vs.add(i)
    for j in adj[i]:
     if j not in seen:seen.add(j);todo.append(j)
   ec=sum(i in vs for i,j in edges)
   if ec>len(vs):pseudo=False
  if pseudo:stats['pseudoforest_shifts']+=1;assert ex<=0
  if all(max(f)<=1 for f in beta) and k<=5:stats['squarefree_small_shifts']+=1;assert ex<=0
  stats['shifts']+=1
 stats['ideals']+=1
for it in range(3000):
 d=rng.randrange(2,7);m=rng.randrange(3,61);r=[rng.randrange(1,m) for _ in range(d)]
 D={(0,)*d}|{tuple(int(i==a) for i in range(d)) for a in range(d)}
 square=it%2==0
 cubes=list(itertools.combinations(range(d),3) if square else itertools.combinations_with_replacement(range(d),3))
 rng.shuffle(cubes)
 for inds in cubes[:rng.randrange(len(cubes)+1)]:
  f=[0]*d
  for a in inds:f[a]+=1
  for g in itertools.product(*(range(x+1) for x in f)):D.add(g)
 test(D,r,m)
print(json.dumps(stats,sort_keys=True))
