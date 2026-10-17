# Fractional arc certificate: slack(s) = sum_z sum_{t in C(z)} lam_{z,t} 1[s in [phi(t-z), phi(t))],  sum_t lam_{z,t}=1, lam>=0
#   family 'top': C(z) = {top_a z : a};   family 'all': C(z) = {t in D : t >= z}
import sys, itertools, random
sys.path.insert(0,'src'); sys.path.insert(0,'src/scratch')
from exp_cl_tiling import downsets, Tvals
from exactlp import feasible
d=int(sys.argv[1]); ms=[int(x) for x in sys.argv[2].split(',')]; fam=sys.argv[3]; cap=int(sys.argv[4]) if len(sys.argv)>4 else 10**9
random.seed(1)
def top(S,x,a):
    y=list(x)
    while True:
        y[a]+=1
        if tuple(y) not in S: y[a]-=1; return tuple(y)
for m in ms:
  inst=[]
  for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    for p in itertools.product(range(1,m),repeat=d):
      if len({sum(x*y for x,y in zip(n,p))%m for n in Dl})!=m: continue
      inst.append((Dl,p))
  random.shuffle(inst); inst=inst[:cap]
  bad=0; ex=None
  for Dl,p in inst:
    S=set(Dl); T=Tvals(S,d); tgt=(d-1)*m*(m-1)//2
    ph={x:sum(a*b for a,b in zip(x,p))%m for x in Dl}
    sl=[(sum(T[x]*((s-ph[x])%m) for x in Dl)-tgt)//m for s in range(m)]
    cols=[]; owner=[]
    cells=[z for z in Dl if any(z)]
    for zi,z in enumerate(cells):
      if fam=='top': C={top(S,z,a) for a in range(d)}
      else: C={t for t in Dl if all(t[b]>=z[b] for b in range(d))}
      arcs=set()
      for t in C:
        st=ph[tuple(t[b]-z[b] for b in range(d))]
        arcs.add(frozenset((st+k)%m for k in range(ph[z])))
      for A in arcs:
        cols.append(A); owner.append(zi)
    rows=[]; rhs=[]
    for zi in range(len(cells)):
      rows.append([1 if owner[j]==zi else 0 for j in range(len(cols))]); rhs.append(1)
    for s in range(m):
      rows.append([1 if s in cols[j] else 0 for j in range(len(cols))]); rhs.append(sl[s])
    x=feasible(rows,rhs)
    if x is None:
      bad+=1
      if ex is None: ex=(Dl,p,sl)
  print('d',d,'m',m,'family',fam,'tiles',len(inst),'infeasible',bad,ex if ex else '',flush=True)
