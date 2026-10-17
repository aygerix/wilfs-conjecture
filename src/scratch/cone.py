# Which test functions g on Z/m (g given on [0,m)) satisfy, for ALL tiles (D,p) and all s,
#    sum_y T(y) g(<s - phi(y)>) >= (d-1) * sum_x g(x)  ?   (sawtooth g(x)=x is the Tile-CL case)
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
  cands={}
  for k in range(m): cands[f'ramp{k}']=[max(x-k,0) for x in range(m)]
  for k in range(1,m): cands[f'min{k}']=[min(x,k) for x in range(m)]
  cands['tent']=[min(x,m-x) for x in range(m)]
  cands['sq']=[x*x for x in range(m)]
  cands['revsaw']=[(m-x)%m for x in range(m)]
  ok={k:True for k in cands}
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
  for name,g in cands.items():
    tg=(d-1)*sum(g)
    for w in tiles:
      if any(sum(w[r]*g[(s-r)%m] for r in range(m))<tg for s in range(m)):
        ok[name]=False; break
  print(d,m,'tiles',len(tiles),'valid:',[k for k,v in ok.items() if v],flush=True)
