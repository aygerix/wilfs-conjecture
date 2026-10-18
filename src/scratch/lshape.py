# d=2: crude class bound  sum_tau #{x in X_tau: rho_x >= e_tau >= 1}  <=  sum_tau |X_tau|(m-e_tau)/m  ?
# and finer: count of Ghat=-1 vs Ghat=+1 per class
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
M=int(sys.argv[1]); d=2
for m in range(3,M+1):
    tot=crude=0; ex=None
    for D in downsets(m,d):
        Dl=sorted(D); S=set(Dl)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
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
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            for s in range(m):
                tot+=1
                lhs=0; rhs=Fr(0)
                for tau,X in classes.items():
                    e=(sum(i*j for i,j in zip(tau,p))-s)%m
                    if e==0: continue
                    lhs+=sum(1 for x in X if (s-res[x])%m>=e)
                    rhs+=Fr(len(X)*(m-e),m)
                if lhs>rhs:
                    crude+=1
                    if ex is None: ex=(Dl,p,s,lhs,str(rhs),{t:len(X) for t,X in classes.items()})
    print('m',m,'(tile,s)',tot,'crude class bound fails',crude,ex,flush=True)
