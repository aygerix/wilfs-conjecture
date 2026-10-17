# Residue-corrected partial Tile-CL (RP-TCL):  for every down-set D' (phi injective), every s:
#   0 <= Ghat_s(D') := sum_{z in D'} gamma_s(z) + #{r not in phi(D'): r > s} <= m-1 .
# Also test the mirror correction  #{r missing : r < s}  and  #{r missing: r >= s} variants.
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2]); m0=int(sys.argv[3]) if len(sys.argv)>3 else 2
def G(Dl,p,m):
    out=[0]*m
    for z in Dl:
        V=sum(a*b for a,b in zip(z,p)); ph=V%m; fl=V//m
        for s in range(m):
            t=(ph-1-s)%m
            out[s]+=sum(z[a] for a in range(d) if t<p[a])-fl
    return out
cache={}
for m in range(m0,M+1):
  tot=0; viol={'gt':0,'ge':0}; ex={}
  for n in range(1,m+1):
    if n not in cache: cache[n]=[sorted(D) for D in downsets(n,d)]
    for Dl in cache[n]:
      for p in itertools.product(range(1,m),repeat=d):
        R={sum(x*y for x,y in zip(z,p))%m for z in Dl}
        if len(R)!=n: continue
        tot+=1
        g=G(Dl,p,m)
        miss=[r for r in range(m) if r not in R]
        for key,cond in (('gt',lambda r,s:r>s),('ge',lambda r,s:r>=s)):
          gh=[g[s]+sum(1 for r in miss if cond(r,s)) for s in range(m)]
          if min(gh)<0 or max(gh)>m-1:
            viol[key]+=1
            ex.setdefault(key,(Dl,p,g,miss,gh))
  print('d',d,'m',m,'pairs',tot,'violations',viol,{k:v for k,v in ex.items()},flush=True)
