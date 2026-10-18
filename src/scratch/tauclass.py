# tau-class decomposition: slack(s) = sum_tau [ sum_{x in X_tau} Ghat(x) + |X_tau| <s - phi(tau)>/m ]
# Ghat(x) = #{a: l'_a(x) > rho_x} - ceil((sum_a l'_a(x) - rho_x)/m),  rho_x=<s-phi(x)>, l'_a = <(t_a(x)-x_a) p_a>
# checks: identity; per-class nonnegativity (m*classsum >= 0); weak class bound
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2]); m0=int(sys.argv[3]) if len(sys.argv)>3 else 3
for m in range(m0,M+1):
    tot=idbad=clsbad=0; ex=None; nclasses={}
    for D in downsets(m,d):
        Dl=sorted(D); S=set(Dl)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        T=Tvals(D,d)
        tv={}
        for x in Dl:
            t=[]
            for a in range(d):
                y=list(x)
                while tuple(y[:a]+[y[a]+1]+y[a+1:]) in S: y[a]+=1
                t.append(y[a])
            tv[x]=tuple(t)
        classes={}
        for x in Dl: classes.setdefault(tv[x],[]).append(x)
        nclasses[len(classes)]=nclasses.get(len(classes),0)+1
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            w=[0]*m
            for x in Dl: w[res[x]]=T[x]
            for s in range(m):
                tot+=1
                slack=(sum(k*w[(s-k)%m] for k in range(m))-(d-1)*m*(m-1)//2)//m
                total=Fr(0); clsvals=[]
                for tau,X in classes.items():
                    ptau=sum(i*j for i,j in zip(tau,p))%m
                    g=0
                    for x in X:
                        rho=(s-res[x])%m
                        l=[((tau[a]-x[a])*p[a])%m for a in range(d)]
                        g+=sum(1 for a in range(d) if l[a]>rho) - (-((rho-sum(l))//m))
                    cv=Fr(g)+Fr(len(X)*((s-ptau)%m),m)
                    total+=cv; clsvals.append(cv)
                if total!=slack: idbad+=1
                if min(clsvals)<0:
                    clsbad+=1
                    if ex is None: ex=(Dl,p,s,[str(v) for v in clsvals])
    print('d',d,'m',m,'(tile,s)',tot,'identity fails',idbad,'some class negative',clsbad,'#classes dist',nclasses,ex,flush=True)
