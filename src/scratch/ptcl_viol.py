import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
sys.argv=[0,'2','2']; exec(open(sys.path[0]+'/../'+'x').read()) if False else None
d=int(sys.argv[1]) if False else 2
def G(Dl,p,m,d):
    out=[0]*m
    for z in Dl:
        V=sum(a*b for a,b in zip(z,p)); ph=V%m; fl=V//m
        for s in range(m):
            t=(ph-1-s)%m
            out[s]+=sum(z[a] for a in range(d) if t<p[a])-fl
    return out
def addable(Dl,d):
    S=set(Dl); out=[]
    for z in Dl:
        for a in range(d):
            x=list(z); x[a]+=1; x=tuple(x)
            if x in S or x in out: continue
            if all(x[b]==0 or tuple(x[:b]+(x[b]-1,)+x[b+1:]) in S for b in range(d)): out.append(x)
    return out
def extendable(Dl,p,m,d):
    # can D' be completed to a full down-set tile with same p (DFS)?
    S=set(Dl); R={sum(a*b for a,b in zip(z,p))%m for z in Dl}
    if len(S)==m: return True
    for x in addable(sorted(S),d):
        r=sum(a*b for a,b in zip(x,p))%m
        if r in R: continue
        if extendable(sorted(S|{x}),p,m,d): return True
    return False
d=int(sys.argv[1]) if len(sys.argv)>1 else 2
for m in range(5,11):
  for n in range(1,m):
    for D in downsets(n,d):
      Dl=sorted(D)
      for p in itertools.product(range(1,m),repeat=d):
        res=[sum(x*y for x,y in zip(z,p))%m for z in Dl]
        if len(set(res))!=n: continue
        g=G(Dl,p,m,d)
        if min(g)<0 or max(g)>n-1:
          miss=sorted(set(range(m))-set(res))
          print('m',m,'n',n,'D',[''.join(map(str,z)) for z in Dl],'p',p,'G',g,'missing',miss,'extendable',extendable(Dl,p,m,d))
