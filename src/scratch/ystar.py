# slack(s) = sum_y v(y)/m * R_s(y) is an integer in [0,m-1]; R_s = <s - phi> is a bijection D->[0,m).
# So slack(s) = R_s(y*) for a unique y*. Study y*: is it maximal? a top? which?
import sys, itertools, collections
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
stats=collections.Counter()
for m in range(3,M+1):
  tgt=(d-1)*m*(m-1)//2
  for D in downsets(m,d):
    Dl=sorted(D); Ds=set(Dl)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    T=Tvals(D,d)
    maxl=[n for n in Dl if all(tuple(n[b]+(b==a) for b in range(d)) not in Ds for a in range(d))]
    for p in itertools.product(range(m),repeat=d):
      ph={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
      if len(set(ph.values()))!=m: continue
      inv={r:n for n,r in ph.items()}
      for s in range(m):
        sl=(sum(T[n]*((s-ph[n])%m) for n in Dl)-tgt)//m
        ys=inv[(s-sl)%m]
        stats['tot']+=1
        stats['max']+= ys in maxl
        stats['T>0']+= T[ys]>0
        stats['zero']+= ys==tuple([0]*d)
        stats['T>=d']+= T[ys]>=d
  print(d,m,dict(stats),flush=True)
