# Do the column arcs [phi(x), phi(top_a x)) contain c0 disjoint PAIRS covering Z/m ?
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
from blossom import max_matching
d=int(sys.argv[1]); M=int(sys.argv[2])
def inarc(x,st,ln,m): return (x-st)%m<=ln   # closed arc [st, st+ln]
for m in range(2,M+1):
    tot=bad=badN=0; ex=None; minexcess=10**9
    for D in downsets(m,d):
        Dl=sorted(D); S=set(Dl)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        tops={}
        for x in Dl:
            for a in range(d):
                t=list(x)
                while True:
                    t[a]+=1
                    if tuple(t) not in S: t[a]-=1; break
                tops[(x,a)]=tuple(t)
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            tot+=1
            c0=sum(sum((x[a]*p[a])%m for a in range(d))//m for x in Dl)
            arcs=[]
            for (x,a),t in tops.items():
                ln=(res[t]-res[x])%m
                if ln>0: arcs.append((res[x],ln))
            N=[sum(1 for st,ln in arcs if (s-st)%m<ln) for s in range(m)]
            if min(N)<c0: badN+=1
            n=len(arcs); adj=[[] for _ in range(n)]
            for i in range(n):
                si,li=arcs[i]
                for j in range(i+1,n):
                    sj,lj=arcs[j]
                    if si!=sj and inarc(sj,si,li,m) and inarc(si,sj,lj,m):
                        adj[i].append(j); adj[j].append(i)
            nu,_=max_matching(n,adj)
            minexcess=min(minexcess,nu-c0)
            if nu<c0:
                bad+=1
                if ex is None: ex=(Dl,p,c0,nu,min(N))
    print('d',d,'m',m,'tiles',tot,'minN<c0:',badN,' matching<c0:',bad,'min(nu-c0)',minexcess,ex,flush=True)
