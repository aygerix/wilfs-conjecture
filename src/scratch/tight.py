import sys
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
import itertools
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3, M+1):
  target=(d-1)*m*(m-1)//2
  cnt=0; tot=0
  for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    T=Tvals(D,d)
    for p in itertools.product(range(m),repeat=d):
      res=[sum(x*y for x,y in zip(n,p))%m for n in Dl]
      if len(set(res))!=m: continue
      w=[0]*m
      for n,r in zip(Dl,res): w[r]=T[n]
      for s in range(m):
        tot+=1
        f=sum(k*w[(s-k)%m] for k in range(m))
        if f==target:
          cnt+=1
          if m<=6 or (cnt<=3):
            R={n:(s-r)%m for n,r in zip(Dl,res)}
            print(m, 'D=',Dl,'p=',p,'s=',s,'R=',[R[n] for n in Dl],'T=',[T[n] for n in Dl])
  print('m',m,'tight',cnt,'of',tot)
