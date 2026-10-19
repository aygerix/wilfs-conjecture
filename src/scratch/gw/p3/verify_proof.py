"""Independent Python proof checks; execute exclusively on fejer.

The exhaustive mode enumerates labeled down-sets directly, without the C
scanner's canonical shapes, bit encodings, or orbit weights. Random mode
also checks dimensions and lifts beyond the exhaustive boxes.
"""
import argparse
import itertools
import json
import random

def verify(D,n,q,residue):
    d=len(n); zero=(0,)*d
    val={x:sum(a*b for a,b in zip(x,n)) for x in D}; M=max(val.values())
    F=lambda t:min(3,t//q)
    lhs=sum(F(v) for v in val.values()); rhs=d*sum(F(M-v) for v in val.values())
    sep={x:sum(F(x[a]*n[a]) for a in range(d)) for x in D}
    surplus=sum(max(0,sep[x]-F(val[x])) for x in D)
    carries=[x for x in D if sep[x]<F(val[x])]
    assert sum(sep.values())-lhs==surplus-len(carries)
    columns={}; column_slack={}
    for a in range(d):
        bases={x[:a]+(0,)+x[a+1:] for x in D}
        for z in bases:
            col=sorted([x for x in D if x[:a]+(0,)+x[a+1:]==z],key=lambda x:x[a])
            assert [x[a] for x in col]==list(range(len(col)))
            cs=sum(F(M-val[x])-F(x[a]*n[a]) for x in col)
            assert cs>=0
            columns[(a,z)]=col; column_slack[(a,z)]=cs
    CS=sum(column_slack.values())
    assert rhs==sum(sep.values())+CS
    if M>=4*q-1:
        Ys=set(); Cs=set()
        for x in carries:
            ab=[a for a in range(d) if x[a]]
            assert len(ab)==2 and sum(x)==2
            a,b=sorted(ab,key=lambda a:(n[a],a))
            assert q<n[a]<2*q and q<n[b]<2*q and n[a]+n[b]>=3*q
            y=tuple(x[j]+(j==b) for j in range(d))
            if y in D:
                assert y not in Ys;Ys.add(y)
                assert sep[y]-F(val[y])>=1
            else:
                z=tuple(int(j==a) for j in range(d)); key=(b,z)
                assert key not in Cs;Cs.add(key)
                assert len(columns[key])==2 and column_slack[key]>=1
        assert len(Ys)<=surplus and len(Cs)<=CS
        assert len(Ys)+len(Cs)==len(carries)
        assert lhs<=rhs
    if residue:
        assert q==len(D) and len({v%q for v in val.values()})==q
        if 3*q<=M<4*q:
            rho=4*q-1-M
            A={a for a in range(d) if n[a]<2*q-rho}
            B={a for a in range(d) if 2*q-rho<=n[a]<3*q-rho}
            C=set(range(d))-A-B
            a,b,c=len(A),len(B),len(C)
            Q=[];R=[];S=[];T=[];U=[]
            for x in D:
                if sum(x)==2:
                    if val[x]<3*q-rho:Q.append(x)
                    elif sum(x[j] for j in A)==2:R.append(x)
                    elif sum(x[j] for j in A)==1:S.append(x)
                    else:T.append(x)
                elif sum(x)==3:U.append(x)
                else:assert sum(x)<=1
            qq,r,s,t,u=map(len,(Q,R,S,T,U))
            assert len(D)==1+d+qq+r+s+t+u
            for x in U:
                for j in range(d):
                    if x[j]:assert tuple(x[k]-(k==j) for k in range(d)) in Q
            assert 3*u<=(a+2)*qq
            assert qq+r<=a*(a+1)//2 and s<=a*b and t<=min(rho,b*(b+1)//2)
            ell=sum((M-v)//q for v in val.values());g=sum(v//q for v in val.values())
            assert ell==3+2*a+b+qq and g+ell==3*q-rho
            H=2*a*(a+1)+(a-2)*qq-3*(r+u)
            W=(d+1)*ell-(3*q-rho)
            assert H>=a*(a+1)//2-qq>=0
            assert W==H+b*(3*a+b+1+qq)-3*(s+t)+c*(2*a+b+qq)+rho
            assert W>=b*qq+c*(2*a+b+qq)>=0
        assert lhs<=rhs
    return M>=4*q-1,3*q<=M<4*q,len(carries)

def downsets(d,limit):
    zero=(0,)*d;lev={frozenset([zero])}
    for m in range(1,limit+1):
        yield m,lev
        nxt=set()
        for D in lev:
            for x in D:
                for a in range(d):
                    y=tuple(x[j]+(j==a) for j in range(d))
                    if y not in D and all(not y[j] or tuple(y[k]-(k==j) for k in range(d)) in D for j in range(d)):
                        nxt.add(D|{y})
        lev=nxt

def exhaustive(d,limit):
    units=[tuple(int(a==j) for j in range(d)) for a in range(d)]
    total=high=low=carries=0
    for m,lev in downsets(d,limit):
        subtotal=0
        for D in lev:
            if not all(x in D for x in units):continue
            for s in itertools.permutations(range(1,m),d):
                if len({sum(x[a]*s[a] for a in range(d))%m for x in D})!=m:continue
                for ks in itertools.product(range(1,4),repeat=d):
                    n=tuple(s[a]+m*ks[a] for a in range(d))
                    h,l,c=verify(D,n,m,True)
                    total+=1;subtotal+=1;high+=h;low+=l;carries+=c
        print(json.dumps(dict(d=d,m=m,instances=subtotal,total=total,high=high,low=low,carries=carries)),flush=True)

def random_checks(trials,seed):
    rng=random.Random(seed);high=low=carry=0
    for trial in range(trials):
        d=rng.randrange(1,13); size=rng.randrange(d+1,101);D={(0,)*d}
        while len(D)<size:
            candidates=set()
            for x in D:
                for a in range(d):
                    y=tuple(x[j]+(a==j) for j in range(d))
                    if y not in D and all(not y[j] or tuple(y[k]-(k==j) for k in range(d)) in D for j in range(d)):
                        candidates.add(y)
            D.add(rng.choice(sorted(candidates)))
        active=[j for j in range(d) if any(x[j] for x in D)]
        D={tuple(x[j] for j in active) for x in D};d=len(active)
        q=rng.randrange(2,101)
        n=tuple(rng.randrange(q+1,30*q+1) for _ in range(d))
        h,l,c=verify(D,n,q,False);high+=h;low+=l;carry+=c
    print(json.dumps(dict(random_trials=trials,seed=seed,high=high,low=low,carries=carry)),flush=True)

def examples():
    def simplex(d,r):return {x for x in itertools.product(range(r+1),repeat=d) if sum(x)<=r}
    D=simplex(2,2); n=(9,10);m=len(D)
    print('distinct_value_P3_failure',dict(m=m,n=n,lhs=sum(min(3,sum(x[a]*n[a] for a in range(2))//m) for x in D),rhs=2*sum(min(3,(20-sum(x[a]*n[a] for a in range(2)))//m) for x in D)))
    for d,r,n in [(2,3,(11,19)),(7,2,(56,)*7)]:
        D=simplex(d,r)
        if d==7:D.add((3,)+(0,)*6)
        m=len(D);v={x:sum(a*b for a,b in zip(x,n)) for x in D};M=max(v.values())
        h={x:max(v[y]-v[x] for y in D if all(y[j]>=x[j] for j in range(d))) for x in D}
        Y=[x for x in D if any(x) and all(h[tuple(x[k]-(k==j) for k in range(d))]<3*m for j in range(d) if x[j])]
        beta=sum(max(0,3-v[x]//m) for x in D if any(x))
        T=sum(h[x]//m for x in D if 0<h[x]<3*m)
        print('false_strengthening',dict(d=d,m=m,n=n,M=M,Y=len(Y),beta=beta,T=T,TCI_lhs=3*len(Y),TCI_rhs=d*T+beta,LP_lhs=sum(min(3,z//m) for z in v.values()),LP_rhs=d*sum(min(3,z//m) for z in h.values())))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--d',type=int);p.add_argument('--m',type=int);p.add_argument('--random',type=int,default=0);p.add_argument('--seed',type=int,default=20261019);p.add_argument('--examples',action='store_true');a=p.parse_args()
    if a.d:exhaustive(a.d,a.m)
    if a.random:random_checks(a.random,a.seed)
    if a.examples:examples()
