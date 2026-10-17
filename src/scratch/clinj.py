# CL-inj: D down-set (any size n <= m), phi injective on D, r = <sigma+phi>.
# G2 = sum_x (d+1-T(x)) r(x) >= 0 ?   (equals CL for tiles)
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(2, M+1):
  fails=0; tot=0; ex=None
  for n in range(1, m+1):
    for D in downsets(n,d):
      Dl=sorted(D); T=Tvals(D,d)
      for p in itertools.product(range(m),repeat=d):
        res=[sum(x*y for x,y in zip(nn,p))%m for nn in Dl]
        if len(set(res))!=n: continue
        for s in range(m):
          tot+=1
          G=sum((d+1-T[nn])*((s+r)%m) for nn,r in zip(Dl,res))
          if G<0:
            fails+=1
            if ex is None: ex=(Dl,p,s,G)
  print(f'd={d} m={m}: instances {tot}, CL-inj failures {fails}', ex, flush=True)
