# Along a build-up D_1 ⊂ D_2 ⊂ ... ⊂ D (adding one cell at a time, prefixes of an order), with virtual completion,
# is Ghat(D_{k+1}) majorized by Ghat(D_k)  (each step a contraction)?  Test several orders.
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2])
def gam(z,p,m):
    V=sum(a*b for a,b in zip(z,p)); ph=V%m; fl=V//m
    return [sum(z[a] for a in range(d) if (ph-1-s)%m<p[a])-fl for s in range(m)]
def maj(x,y):  # x ≺ y ?
    xs=sorted(x,reverse=True); ys=sorted(y,reverse=True); a=b=0
    for u,v in zip(xs,ys):
        a+=u; b+=v
        if a>b: return False
    return a==b
orders={'V':lambda z,p:(sum(a*b for a,b in zip(z,p)),z),
        'deg':lambda z,p:(sum(z),sum(a*b for a,b in zip(z,p)),z),
        'lex':lambda z,p:z,
        'revV':lambda z,p:(-0,)}
for m in range(3,M+1):
  res={k:[0,0] for k in ('V','deg','lex')}
  for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    for p in itertools.product(range(1,m),repeat=d):
      if len({sum(x*y for x,y in zip(n,p))%m for n in Dl})!=m: continue
      for name in res:
        order=sorted(Dl,key=lambda z:orders[name](z,p))
        G=[m-1-s for s in range(m)]   # D_1={0} completed
        ok=True
        for z in order[1:]:
          ph=sum(a*b for a,b in zip(z,p))%m
          g=gam(z,p,m)
          G2=[G[s]+g[s]-(1 if ph>s else 0) for s in range(m)]
          if not maj(G2,G): ok=False
          G=G2
        res[name][0]+=1; res[name][1]+= (not ok)
  print('d',d,'m',m,{k:f'{v[1]}/{v[0]} non-monotone' for k,v in res.items()},flush=True)
