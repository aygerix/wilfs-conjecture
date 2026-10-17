import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
for d,M in ((2,10),(3,8)):
  for m in range(3,M+1):
    tgt=(d-1)*m*(m-1)//2; bad=0; tot=0
    for D in downsets(m,d):
      Dl=sorted(D)
      if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
      T=Tvals(D,d)
      for p in itertools.product(range(m),repeat=d):
        res=[sum(x*y for x,y in zip(n,p))%m for n in Dl]
        if len(set(res))!=m: continue
        w=[0]*m
        for n,r in zip(Dl,res): w[r]=T[n]
        tot+=1
        if any((sum(k*w[(s-k)%m] for k in range(m))-tgt)%m for s in range(m)): bad+=1
    print(d,m,tot,'nondivisible',bad)
