"""Exact audit of ONCE-ID/ONCE-LEVEL, including E47 and actual semigroup tiles.
Run on fejer only.  Uses the lead's existing semigroup/tile generator.
"""
import collections
import json
from pathlib import Path
import random
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'nowrap'))
from pmin_tile import apery,minimal_gens,tile


def check(m,n,D):
    d=len(n);P=[x%m for x in n];D=set(D)
    v={x:sum(a*b for a,b in zip(x,P)) for x in D}
    T={};A=set()
    for x in D:
        T[x]=0
        maximal=True
        for a in range(d):
            y=list(x);y[a]+=1
            if tuple(y) not in D:T[x]+=x[a]+1
            else:maximal=False
        if maximal:A.add(x)
    N=D-A
    if any(v[x]>=2*m for x in N):return None
    assert all(v[x]<3*m for x in D)
    N1={x for x in N if v[x]>=m}
    k={x:v[x]//m for x in D}
    phases=negative=0
    worst=0
    for rho in range(m):
        theta=m-rho
        r={x:(v[x]+rho)%m for x in D}
        S=(d+1)*m*(m-1)//2-sum((d+sum(y))*r[y] for y in A)
        Lam=sum(T[x]*r[x] for x in N)
        q1=(sum(T[x] for x in D if v[x]%m>=theta)-d*rho
            +sum((sum(y)-1)*k[y] for y in A)
            +sum(T[x]-d-1 for x in N1))
        def boundary(b):
            return sum(x[a] for x in D for a in range(d) if v[x]-P[a]<b<=v[x])
        q2=(boundary(theta)+boundary(m+theta)
            +sum(sum(y) for y in A if v[y]>=2*m+theta)
            -sum(v[x]>=m for x in D)-sum(v[x]>=2*m for x in D))
        assert S-Lam==m*q1==m*q2
        phases+=1
        negative+=q1<0
        worst=min(worst,q1)
    return dict(phases=phases,negative_PC=negative,worst=worst,
                nonmax_wrap=bool(N1),height=max(map(sum,D)))


def main():
    rng=random.Random(2026101977)
    stats=collections.Counter();maxheight=0;named=[]
    trials=500
    fixtures=[(14,[22,23,57,61,62,63]),(17,[24,26,29,30,32])]
    for m,gens in fixtures:
        n,ap=minimal_gens(m,gens)
        D=tile(m,n,ap,lambda x:(sum(x),tuple(-z for z in x)))
        z=check(m,n,D.values());assert z
        named.append(dict(m=m,n=n,result=z))
    for tr in range(trials):
        m=rng.randint(8,100);d=rng.randint(2,min(8,m-1))
        gens=[rng.randint(m+1,4*m) for _ in range(d)]
        if None in apery(m,gens):continue
        n,ap=minimal_gens(m,gens)
        P=[g%m for g in n]
        for key in (lambda x:(sum(x),tuple(-z for z in x)),
                    lambda x:(sum(a*b for a,b in zip(x,P)),sum(x),tuple(-z for z in x))):
            D=tile(m,n,ap,key)
            z=check(m,n,D.values())
            stats['tiles_attempted']+=1
            if z is None:
                stats['outside_once']+=1
                continue
            stats['once_tiles']+=1
            stats['phases']+=z['phases']
            stats['negative_PC_phases']+=z['negative_PC']
            stats['once_with_nonmax_wrap']+=z['nonmax_wrap']
            maxheight=max(maxheight,z['height'])
    print(json.dumps(dict(seed=2026101977,trials=trials,stats=stats,
                          maxheight=maxheight,named=named,identities_failed=0),sort_keys=True))


if __name__=='__main__':main()
