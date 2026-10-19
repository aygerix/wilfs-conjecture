"""Exact continuation experiments. Execute only on fejer.

Macaulay growth catalogues are finite consequences of a stated theorem,
not an inference from arbitrary bounded weight searches.
"""
import argparse
from collections import Counter
from itertools import combinations_with_replacement, combinations
from math import comb
import json
import random


def grow(n,degree):
    ans=0;remaining=n;upper=n+degree
    for j in range(degree,0,-1):
        t=min(upper,j)
        while t<upper and comb(t+1,j)<=remaining:t+=1
        while comb(t,j)>remaining:t-=1
        ans+=comb(t+1,j+1)
        remaining-=comb(t,j);upper=t-1
    assert remaining==0
    return ans


def catalog(a):
    Q=comb(a+1,2);C=comb(a+2,3)
    negative=[];table=[]
    for q2 in range(Q+1):
        limit=grow(q2,2)
        low=min(((a+1)*u-4*grow(u,3),u,grow(u,3)) for u in range(limit+1))
        table.append(dict(q2=q2,u3max=limit,minimum_low_cost=(a+1)*q2+low[0],at_u3=low[1],at_k=low[2]))
    for p in range(Q+1):
        for q2 in range(p+1):
            for f in range(grow(p,2)+1):
                for u3 in range(min(f,grow(q2,2))+1):
                    for k in range(grow(u3,3)+1):
                        q3=p-q2;u4=f-u3
                        WA=3*a*(a+1)+(2*a-2)*q2+(a-3)*(q3+u3)-4*(u4+k)
                        if WA<0:negative.append((q2,q3,u3,u4,k,WA))
    print(json.dumps(dict(mode='catalog',a=a,table=table,negative_count=len(negative),negative=negative if a<=4 else negative[:30]),indent=2),flush=True)
    if a==4:
        expected={(0,10,0,20-t,0,-10+4*t) for t in range(3)}
        expected|={(1,9,0,20-t,0,-5+4*t) for t in range(2)}
        expected.add((1,9,1,19,1,-4))
        assert set(negative)==expected,(set(negative)-expected,expected-set(negative))
    return negative


def weighted_pack(B,m,chosen):
    """Triples are tuples of indices into B, including index zero padding."""
    s=len(B);alltriples=list(combinations_with_replacement(range(s),3))
    residue=lambda x:sum(B[i] for i in x)%m
    assert len({residue(x) for x in combinations_with_replacement(range(s),2)})==comb(s+1,2)
    assert len({residue(x) for x in chosen})==len(chosen)
    omitted=set(alltriples)-set(chosen)
    # Linear form applies whenever omitted triples have distinct residues.
    assert len({residue(x) for x in omitted})==len(omitted)
    penalty=sum(len(set(x))*min(3,s-len(set(x))) for x in omitted)
    H=s*(s*(s-1)//2+1)
    assert m>=H-penalty
    return penalty


def pack_trials(trials,seed):
    rng=random.Random(seed);hist=Counter();min_example=None
    for _ in range(trials):
        m=rng.randrange(7,201);s=rng.randrange(3,min(9,m))
        B=(0,)+tuple(rng.sample(range(1,m),s-1))
        pairs=list(combinations_with_replacement(range(s),2))
        res=lambda x:sum(B[i] for i in x)%m
        if len({res(x) for x in pairs})!=len(pairs):continue
        hist['pair_injective']+=1
        triples=list(combinations_with_replacement(range(s),3))
        groups={}
        for x in triples:groups.setdefault(res(x),[]).append(x)
        excess=len(triples)-len(groups)
        H=s*(s*(s-1)//2+1)
        assert 2*m>=2*H-3*s*excess
        hist['universal_linear_checks']+=1
        chosen={rng.choice(xs) for xs in groups.values()}
        omitted=set(triples)-chosen
        if len({res(x) for x in omitted})!=len(omitted):continue
        weighted_pack(B,m,chosen);hist['linear_distinct_omitted']+=1
        if all(set(x)&set(y) for x,y in combinations(omitted,2)):
            hist['intersecting_omitted']+=1
        if omitted and all(0 not in x for x in omitted):hist['all_quadratics_chosen']+=1
    print(json.dumps(dict(mode='packing',trials=trials,seed=seed,counts=hist)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--a',type=int,default=0);p.add_argument('--packing',type=int,default=0);p.add_argument('--seed',type=int,default=20261019)
    args=p.parse_args()
    if args.a:catalog(args.a)
    if args.packing:pack_trials(args.packing,args.seed)
