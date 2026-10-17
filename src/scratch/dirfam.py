# direction-a arc families: S^a(s) = sum_z 1[s in [phi(top_a z - z), phi(top_a z))]  (arc of length phi(z)).
# Compare with slack: is slack = S^a ? = average_a S^a ?
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2])
def top(S,x,a):
    y=list(x)
    while True:
        y[a]+=1
        if tuple(y) not in S: y[a]-=1; return tuple(y)
for m in range(3,M+1):
  cnt=0; eq_any=0; eq_avg=0; eq_all=0; ex=None
  for D in downsets(m,d):
    Dl=sorted(D); S=set(Dl)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    T=Tvals(S,d); tgt=(d-1)*m*(m-1)//2
    for p in itertools.product(range(1,m),repeat=d):
      ph={x:sum(a*b for a,b in zip(x,p))%m for x in Dl}
      if len(set(ph.values()))!=m: continue
      cnt+=1
      sl=[(sum(T[x]*((s-ph[x])%m) for x in Dl)-tgt)//m for s in range(m)]
      fams=[]
      for a in range(d):
        Sa=[0]*m
        for z in Dl:
          t=top(S,z,a); st=ph[tuple(t[b]-z[b] for b in range(d))]
          for k in range(ph[z]): Sa[(st+k)%m]+=1
        fams.append(Sa)
      e=[f==sl for f in fams]
      eq_any+=any(e); eq_all+=all(e)
      avg=[sum(f[s] for f in fams) for s in range(m)]
      eq_avg+= all(avg[s]==d*sl[s] for s in range(m))
      if not any(e) and ex is None: ex=(Dl,p,sl,fams)
  print('d',d,'m',m,'tiles',cnt,'slack==S^a some a',eq_any,'all a',eq_all,'avg',eq_avg, ex if ex and m<8 else '',flush=True)
