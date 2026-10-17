# per-direction walk extremes for d=2 tiles: 2*m*(max dev) etc, vs column-length data
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=2; M=int(sys.argv[1])
seen=set()
for m in range(3,M+1):
  for D in downsets(m,d):
    Dl=sorted(D); Ds=set(Dl)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    for p in itertools.product(range(m),repeat=d):
      ph={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
      if len(set(ph.values()))!=m: continue
      inv={r:n for n,r in ph.items()}
      out=[]
      for a in range(d):
        Ta={n:(n[a]+1 if tuple(n[b]+(b==a) for b in range(d)) not in Ds else 0) for n in Dl}
        U=[0]
        for r in range(m): U.append(U[-1]+Ta[inv[r]]-1)
        U=U[1:]; mean=Fr(sum(U),m)
        lens=sorted([Ta[n] for n in Dl if Ta[n]>0],reverse=True)
        out.append((float(max(U)-mean),float(mean-min(U)),lens))
      print(m,[''.join(map(str,n)) for n in Dl],p,'dir1 max-mean,mean-min,collens',out[0],' dir2',out[1], ' sums', out[0][0]+out[1][0], out[0][1]+out[1][1], '(m-1)/2=',(m-1)/2)
