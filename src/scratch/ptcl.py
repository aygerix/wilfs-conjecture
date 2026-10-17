# Partial Tile-CL (P-TCL): for every down-set D' in N^d, every p in [1,m-1]^d with phi=<.,p> mod m injective on D',
# every s in Z/m:   0 <= G_s(D') := sum_{z in D'} gamma_s(z) <= |D'|-1.
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2]); m0=int(sys.argv[3]) if len(sys.argv)>3 else 2
def G(Dl,p,m):
    out=[0]*m
    for z in Dl:
        V=sum(a*b for a,b in zip(z,p)); ph=V%m; fl=V//m
        for s in range(m):
            t=(ph-1-s)%m   # s in [ph-p_a, ph) iff t < p_a
            out[s]+=sum(z[a] for a in range(d) if t<p[a])-fl
    return out
cache={}
for m in range(m0,M+1):
  tot=viol=0; ex=None; tight_lo=tight_hi=0
  for n in range(1,m+1):
    if n not in cache: cache[n]=[sorted(D) for D in downsets(n,d)]
    for Dl in cache[n]:
      for p in itertools.product(range(1,m),repeat=d):
        res={sum(x*y for x,y in zip(z,p))%m for z in Dl}
        if len(res)!=n: continue
        tot+=1
        g=G(Dl,p,m)
        if min(g)<0 or max(g)>n-1:
          viol+=1
          if ex is None: ex=(Dl,p,g)
        tight_lo+=min(g)==0; tight_hi+=max(g)==n-1
  print('d',d,'m',m,'(D,p) pairs',tot,'violations',viol,'tight lo/hi',tight_lo,tight_hi,ex if ex else '',flush=True)
