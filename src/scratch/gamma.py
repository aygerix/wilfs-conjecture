# (1) verify additive cell formula slack(s) = sum_{z in D} gamma_s(z),
#     gamma_s(z) = sum_a z_a [s in [phi(z)-p_a, phi(z)) mod m] - floor(V(z)/m),  V = <z, p> with p_a in [1,m-1].
# (2) test partial version on down-sets D' (|D'|=n<=m) with phi injective: 0 <= sum gamma <= n-1 ?
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
def gam(z,p,m,s):
    V=sum(a*b for a,b in zip(z,p)); ph=V%m
    return sum(z[a]*(1 if (ph-s-1)%m < p[a] else 0) for a in range(d)) - V//m
# note: s in [ph-p, ph)  <=>  (ph-1-s) mod m in [0,p)
for m in range(2,M+1):
  bad1=0; full=0
  for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    T=Tvals(D,d); tgt=(d-1)*m*(m-1)//2
    for p in itertools.product(range(1,m),repeat=d):
      res=[sum(x*y for x,y in zip(n,p))%m for n in Dl]
      if len(set(res))!=m: continue
      full+=1
      for s in range(m):
        sl=(sum(T[n]*((s-r)%m) for n,r in zip(Dl,res))-tgt)//m
        g=sum(gam(n,p,m,s) for n in Dl)
        if sl!=g: bad1+=1
  # partial
  stats={}
  for n in range(1,m+1):
    viol=0; tot=0; ex=None; lo=10**9; hi=-10**9
    for D in downsets(n,d):
      Dl=sorted(D)
      for p in itertools.product(range(1,m),repeat=d):
        res=[sum(x*y for x,y in zip(z,p))%m for z in Dl]
        if len(set(res))!=n: continue
        tot+=1
        for s in range(m):
          g=sum(gam(z,p,m,s) for z in Dl)
          lo=min(lo,g); hi=max(hi,g-(n-1))
          if g<0 or g>n-1:
            viol+=1
            if ex is None: ex=(Dl,p,s,g)
    stats[n]=(tot,viol,lo,hi,ex)
  print('d',d,'m',m,'full tiles',full,'formula mismatches',bad1)
  for n,(tot,viol,lo,hi,ex) in stats.items():
    print('   n',n,'pairs',tot,'viol',viol,'min sum',lo,'max sum-(n-1)',hi, ex if viol else '')
