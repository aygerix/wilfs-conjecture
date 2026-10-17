# E(theta) = beta(H_theta), H_theta = {y in D: V(y) >= theta}, V = <y,phat>.  Test "local monotonicity on scale m":
#  (U) E(theta) <= mean_{theta' in (theta-m, theta]} E(theta')   for all theta >= 1   (=> upper half of Tile-CL)
#  (L) E(theta) >= mean_{theta' in [theta, theta+m)} E(theta')   for all theta >= 1   (=> lower half)
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
  tot=fu=fl=0; exu=exl=None
  for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    T=Tvals(D,d); beta={y:d+1-T[y] for y in Dl}
    for p in itertools.product(range(m),repeat=d):
      res=[sum(x*y for x,y in zip(n,p))%m for n in Dl]
      if len(set(res))!=m: continue
      tot+=1
      V={y:sum(a*b for a,b in zip(y,p)) for y in Dl}
      top=max(V.values())
      Ev={}
      for th in range(-m, top+m+2):
        Ev[th]=sum(beta[y] for y in Dl if V[y]>=th)
      E=lambda th: Ev[th] if th in Ev else (m if th< -m else 0)
      okU=all(m*E(th) <= sum(E(t) for t in range(th-m+1,th+1)) for th in range(1,top+1))
      okL=all(m*E(th) >= sum(E(t) for t in range(th,th+m)) for th in range(1,top+1))
      if not okU:
        fu+=1; exu=exu or (Dl,p)
      if not okL:
        fl+=1; exl=exl or (Dl,p)
  print(d,m,'inst',tot,'U-fail',fu,'L-fail',fl,flush=True)
