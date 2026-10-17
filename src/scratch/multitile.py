# Multi-tile CL: for each lattice (p) and s:  sum_a min_{tiles D} f_a^D(s) >= (d-1) m(m-1)/2 ?
# f_a^D(s) = sum_{a-columns C of D} |C| <s - phi(top C)>.   (Tile-CL is the diagonal D_a = D.)
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
from math import gcd
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
  allD=[sorted(D) for D in downsets(m,d)]
  tot=fail=0; worst=0; ex=None
  for p in itertools.product(range(1,m),repeat=d):
    if gcd(m,*p)!=1: continue
    tiles=[D for D in allD if len({sum(x*y for x,y in zip(z,p))%m for z in D})==m]
    if not tiles: continue
    fa=[]  # per tile, per a, list over s
    for D in tiles:
      S=set(D); ph={z:sum(x*y for x,y in zip(z,p))%m for z in D}
      per=[]
      for a in range(d):
        tops=[(z,z[a]+1) for z in D if tuple(z[:a]+(z[a]+1,)+z[a+1:]) not in S]
        per.append([sum(L*((s-ph[z])%m) for z,L in tops) for s in range(m)])
      fa.append(per)
    tgt=(d-1)*m*(m-1)//2
    for s in range(m):
      val=sum(min(fa[k][a][s] for k in range(len(tiles))) for a in range(d))
      tot+=1
      if val<tgt:
        fail+=1; worst=max(worst,tgt-val)
        if ex is None: ex=(p,s,val,tgt)
  print('d',d,'m',m,'(p,s)',tot,'multi-tile CL fails',fail,'worst deficit',worst,ex,flush=True)
