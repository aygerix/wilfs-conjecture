# finer geometric types of covering pairs {(u,a),(v,b)}, a!=b, u,v differ in exactly one coordinate k
#  ABOVE: k=a and v_a>u_a (v on u's a-path)  [or symmetric: k=b, u on v's b-path]
#  BELOW: k=a and v_a<u_a                      [or symmetric]
#  OTHER: k not in {a,b}
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
from blossom import max_matching
d=int(sys.argv[1]); M=int(sys.argv[2]); m0=int(sys.argv[3]) if len(sys.argv)>3 else 3
def inarc(x,st,ln,m): return (x-st)%m<=ln
def ptype(u,a,v,b,d):
    diff=[k for k in range(d) if u[k]!=v[k]]
    if len(diff)!=1: return None
    k=diff[0]
    if k==a: return 'ABOVE' if v[a]>u[a] else 'BELOW'
    if k==b: return 'ABOVE' if u[b]>v[b] else 'BELOW'
    return 'OTHER'
modes=('ABOVE','BELOW','ABOVE|OTHER','BELOW|OTHER')
for m in range(m0,M+1):
    tot=0; bad={k:0 for k in modes}; ex={}
    for D in downsets(m,d):
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
            tot+=1
            c0=sum(sum((x[a]*p[a])%m for a in range(d))//m for x in Dl)
            arcs=[(x,a,res[x],(res[t]-res[x])%m) for (x,a),t in tops.items() if (res[t]-res[x])%m>0]
            n=len(arcs)
            for mode in modes:
                allowed=set(mode.split('|'))
                adj=[[] for _ in range(n)]
                for i in range(n):
                    for j in range(i+1,n):
                        (u,a),(v,b)=arcs[i][:2],arcs[j][:2]
                        if a==b: continue
                        if ptype(u,a,v,b,d) not in allowed: continue
                        si,li=arcs[i][2:]; sj,lj=arcs[j][2:]
                        if si!=sj and inarc(sj,si,li,m) and inarc(si,sj,lj,m): adj[i].append(j); adj[j].append(i)
                nu,_=max_matching(n,adj)
                if nu<c0:
                    bad[mode]+=1
                    if mode not in ex: ex[mode]=(Dl,p,c0,nu)
    print('d',d,'m',m,'tiles',tot,'fail',bad,ex,flush=True)
