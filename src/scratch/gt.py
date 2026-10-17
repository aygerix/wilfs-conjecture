# Generalized Tile-CL (GT): D down-set in N^d, phi(y)=<y,p> mod m INJECTIVE on D (|D|<=m), any s:
#   sum_y T_D(y) R_s(y) >= (d-1) sum_y R_s(y),  R_s = (s - phi) mod m.
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(2,M+1):
  tot=fails=0; ex=None
  for n in range(1,m+1):
    for D in downsets(n,d):
      Dl=sorted(D); T=Tvals(D,d)
      for p in itertools.product(range(m),repeat=d):
        res=[sum(x*y for x,y in zip(q,p))%m for q in Dl]
        if len(set(res))!=n: continue
        tot+=1
        for s in range(m):
          R=[(s-r)%m for r in res]
          lhs=sum(T[q]*Rv for q,Rv in zip(Dl,R)); rhs=(d-1)*sum(R)
          if lhs<rhs:
            fails+=1
            if ex is None: ex=(Dl,p,s,lhs,rhs)
            break
  print(d,m,'inst',tot,'GT fails',fails,ex,flush=True)
