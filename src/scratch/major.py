"""Is the centered walk H - mean(H) (H(t) = f(t)/m up to sign/shift) majorized by the sawtooth vector
((m-1)/2 - j)_j ?  Equivalent: for each k, sum of k largest slack-deviations <= sum of k largest sawtooth values.
Here use slack(s) = (f(s) - target)/m in [0, m-1] (CL two-sided), mean (m-1)/2."""
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
  tgt=(d-1)*m*(m-1)//2; fails=0; tot=0; ex=None
  saw=sorted(range(m))  # slack values of a pure sawtooth: 0..m-1
  for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    T=Tvals(D,d)
    for p in itertools.product(range(m),repeat=d):
      res=[sum(x*y for x,y in zip(n,p))%m for n in Dl]
      if len(set(res))!=m: continue
      w=[0]*m
      for n,r in zip(Dl,res): w[r]=T[n]
      sl=sorted((sum(k*w[(s-k)%m] for k in range(m))-tgt)//m for s in range(m))
      tot+=1
      # majorization of sl by saw (same total): partial sums of sorted-desc sl <= those of saw
      a=sl[::-1]; b=saw[::-1]; pa=pb=0; ok=True
      for i in range(m):
        pa+=a[i]; pb+=b[i]
        if pa>pb: ok=False; break
      if not ok:
        fails+=1
        if ex is None: ex=(Dl,p,sl)
  print(d,m,'instances',tot,'majorization failures',fails,ex,flush=True)
