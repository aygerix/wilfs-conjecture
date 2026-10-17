# perfect tiles: V=<.,p> bijective D -> [0,m).  X_s = #{(x,a): V(x)<=s<V(top_a x)}.
import sys, itertools, collections
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2])
def top(S,x,a):
    y=list(x)
    while True:
        y[a]+=1
        if tuple(y) not in S: y[a]-=1; return tuple(y)
stats=collections.Counter()
for m in range(2,M+1):
  n=0; mx=0; tight=0; prof=collections.Counter()
  for D in downsets(m,d):
    Dl=sorted(D); S=set(Dl)
    if any(all(x[a]==0 for x in Dl) for a in range(d)): continue
    for p in itertools.product(range(1,m),repeat=d):
      V={x:sum(a*b for a,b in zip(x,p)) for x in Dl}
      if sorted(V.values())!=list(range(m)): continue
      n+=1
      X=[0]*m
      for x in Dl:
        for a in range(d):
          t=top(S,x,a)
          for s in range(V[x],V[t]): X[s]+=1
      mx=max(mx,max(X)); tight+= max(X)==m-1
      # excess over s+1
      prof[max(X[s]-(s+1) for s in range(m-1))]+=1
      if max(X)>m-1: print('VIOLATION',Dl,p,X)
  print('d',d,'m',m,'perfect tiles',n,'max X',mx,'tight',tight,'max_s (X_s-(s+1)) distribution',dict(sorted(prof.items())),flush=True)
