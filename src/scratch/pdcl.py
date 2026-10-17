import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
def test(m,d):
  half=m*(m-1)//2
  fails=0; tot=0; ex=[]
  for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    # columns per direction: (top, length)
    cols=[]
    for a in range(d):
      cl=[]
      for n in Dl:
        x=list(n); x[a]+=1
        if tuple(x) not in D: cl.append((n, n[a]+1))
      cols.append(cl)
    for p in itertools.product(range(m),repeat=d):
      phi={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
      if len(set(phi.values()))!=m: continue
      tot+=1
      deltas=[]
      for a in range(d):
        mn=min(sum(L*((s-phi[t])%m) for t,L in cols[a]) for s in range(m))
        deltas.append(half-mn)
      if sum(deltas)>half:
        fails+=1
        if len(ex)<3: ex.append((Dl,p,deltas,half))
  return tot,fails,ex
for d,ms in [(2,range(3,13)),(3,range(4,10))]:
  for m in ms:
    print(d,m,test(m,d),flush=True)
