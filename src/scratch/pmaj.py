# Partial majorization: for every down-set D' with phi injective, is the vector
#   F(sigma) = sigma + sum_{z in D'} delta_sigma(z),  delta_sigma(z) = sum_a z_a [<V+sigma> < p_a] - floor((V+sigma)/m)
# majorized by (0,1,...,m-1)?   (F(sigma) equals Ghat_s with s = m-1-sigma.)
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2])
def F(Dl,p,m):
    out=list(range(m))
    for z in Dl:
        V=sum(a*b for a,b in zip(z,p))
        for sg in range(m):
            r=(V+sg)%m
            out[sg]+=sum(z[a] for a in range(d) if r<p[a])-(V+sg)//m
    return out
def majorized(v,m):
    v=sorted(v,reverse=True); ref=list(range(m-1,-1,-1)); a=b=0
    for x,y in zip(v,ref):
        a+=x; b+=y
        if a>b: return False
    return a==b
cache={}
for m in range(2,M+1):
  tot=viol=rng=0; ex=None
  for n in range(1,m+1):
    if n not in cache: cache[n]=[sorted(D) for D in downsets(n,d)]
    for Dl in cache[n]:
      for p in itertools.product(range(1,m),repeat=d):
        if len({sum(x*y for x,y in zip(z,p))%m for z in Dl})!=n: continue
        tot+=1; f=F(Dl,p,m)
        if min(f)<0 or max(f)>m-1: rng+=1
        if not majorized(f,m):
          viol+=1
          if ex is None: ex=(Dl,p,f)
  print('d',d,'m',m,'pairs',tot,'range viol',rng,'majorization viol',viol,ex if ex else '',flush=True)
