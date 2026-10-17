# class-max bound: CM(s) = sum_r max_{z in support(class r)} gamma_s(z), support = cells lying in some tile (given p).
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
from math import gcd
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
  allD=[sorted(D) for D in downsets(m,d)]
  tot=over=0; worst=0; ex=None
  for p in itertools.product(range(1,m),repeat=d):
    g=m
    for a in p: g=gcd(g,a)
    if g!=1: continue
    tiles=[D for D in allD if len({sum(x*y for x,y in zip(z,p))%m for z in D})==m]
    if not tiles: continue
    supp=set(z for D in tiles for z in D)
    for s in range(m):
      best={}
      lo={}
      for z in supp:
        V=sum(a*b for a,b in zip(z,p)); ph=V%m
        gz=sum(z[a] for a in range(d) if (ph-1-s)%m<p[a])-V//m
        best[ph]=max(best.get(ph,-10**9),gz); lo[ph]=min(lo.get(ph,10**9),gz)
      CM=sum(best.values()); CL=sum(lo.values())
      tot+=1
      if CM>m-1 or CL<0:
        over+=1; worst=max(worst,CM-(m-1),-CL)
        if ex is None: ex=(p,s,CM,CL,len(tiles))
  print('d',d,'m',m,'(p,s)',tot,'class-max bound fails',over,'worst excess',worst,ex,flush=True)
