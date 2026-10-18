import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
from blossom import max_matching
d=int(sys.argv[1]); m=int(sys.argv[2]); want=int(sys.argv[3]) if len(sys.argv)>3 else 3
def inarc(x,st,ln,m): return (x-st)%m<=ln
shown=0
for D in sorted(downsets(m,d),key=lambda D:sorted(D)):
    Dl=sorted(D); S=set(Dl)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    tops={}
    for x in Dl:
        for a in range(d):
            t=list(x)
            while tuple(t[:a]+[t[a]+1]+t[a+1:]) in S: t[a]+=1
            tops[(x,a)]=tuple(t)
    for p in itertools.product(range(1,m),repeat=d):
        res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
        if len(set(res.values()))!=m: continue
        carries=[x for x in Dl if sum((x[a]*p[a])%m for a in range(d))//m>0]
        c0=sum(sum((x[a]*p[a])%m for a in range(d))//m for x in Dl)
        if c0<2: continue
        arcs=[]
        for (x,a),t in tops.items():
            ln=(res[t]-res[x])%m
            if ln>0: arcs.append((x,a,res[x],ln))
        n=len(arcs); adj=[[] for _ in range(n)]
        for i in range(n):
            for j in range(i+1,n):
                si,li=arcs[i][2:]; sj,lj=arcs[j][2:]
                if si!=sj and inarc(sj,si,li,m) and inarc(si,sj,lj,m): adj[i].append(j); adj[j].append(i)
        nu,match=max_matching(n,adj)
        print('D',Dl,'p',p,'c0',c0,'carries',carries,'nu',nu)
        print('  residues', {x:res[x] for x in Dl})
        print('  all covering pairs:',[ (arcs[i][:2],arcs[j][:2]) for i in range(n) for j in adj[i] if j>i])
        shown+=1
        if shown>=want: sys.exit()
