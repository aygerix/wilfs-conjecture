# Cone of valid test functions: g on Z/m valid iff for all tiles, all s:
#   sum_y T(y) g(<s-phi(y)>) >= (d-1) sum_x g(x).
# Test tents tau_k (concave on [0,m], zero at 0 and m, peak at k): tau_k(x)= x(m-k) (x<=k), k(m-x) (x>=k).
# tau_{m-1}= sawtooth (Tile-CL), tau_1 = revsaw.  Report min normalized slack per k.
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
  tiles=[]
  for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    T=Tvals(D,d)
    for p in itertools.product(range(m),repeat=d):
      res=[sum(x*y for x,y in zip(n,p))%m for n in Dl]
      if len(set(res))!=m: continue
      w=[0]*m
      for n,r in zip(Dl,res): w[r]=T[n]
      tiles.append(w)
  if not tiles: continue
  out=[]
  for k in range(1,m):
    g=[x*(m-k) if x<=k else k*(m-x) for x in range(m)]
    tg=(d-1)*sum(g)
    mn=min(sum(w[r]*g[(s-r)%m] for r in range(m))-tg for w in tiles for s in range(m))
    out.append(mn)
  print(d,m,len(tiles),'min slack per k:',out,flush=True)
