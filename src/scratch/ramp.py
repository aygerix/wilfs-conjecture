# Test: for down-set D (tile or not) and weights q>=0, G(K) = sum_y beta(y) (V(y)-K)^+ <= 0 for all K,
# beta = d+1-T, V = <y,q>.  (Equivalent to sum beta g(V) >= 0 for all concave g with g(0)=0.)
import sys, itertools, random
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2]); Q=int(sys.argv[3])
for m in range(2,M+1):
  fails=0; tot=0; ex=None
  for D in downsets(m,d):
    Dl=sorted(D); T=Tvals(D,d)
    beta={y:d+1-T[y] for y in Dl}
    for q in itertools.product(range(1,Q+1),repeat=d):
      V={y:sum(a*b for a,b in zip(y,q)) for y in Dl}
      vals=sorted(set(V.values()))
      tot+=1
      for K in vals:
        G=sum(beta[y]*max(V[y]-K,0) for y in Dl)
        if G>0:
          fails+=1
          if ex is None: ex=(Dl,q,K,G)
          break
  print(d,m,'instances',tot,'fails',fails,ex,flush=True)
