"""Sharp support-fiber constant and pure-A relaxations. Run on fejer only."""
from fractions import Fraction
from itertools import combinations_with_replacement
from math import comb,gcd
from collections import Counter
import argparse
import json
import random
from a4_stability import catalog


def fiber_constant(s):
    best=Fraction(0)
    witness=None
    for n1 in range(s+1):
        for n2 in range((s-n1)//2+1):
            for n3 in range((s-n1-2*n2)//3+1):
                g=n1+n2+n3
                if g<2:continue
                total=n1+2*n2+3*n3
                pairs=(total*total-n1-4*n2-9*n3)//2
                value=Fraction(pairs,g-1)
                if value>best:best=value;witness=(n1,n2,n3)
    return best,witness


def bound(s):
    if s<5:return fiber_constant(s)[0]
    return Fraction(3*(s-(s%3!=0)),2)


def coverage_bound(s,m,r):
    H=s*(s*(s-1)//2+1)
    answer=H-bound(s)*r
    if s>=6 and s%3==0:
        k=s//3
        answer=max(answer,H-Fraction(3*s-6,2)*r-3*(k-1)*gcd(k,m))
    return answer


def constants():
    rows=[]
    for s in range(2,101):
        actual,witness=fiber_constant(s)
        assert actual==bound(s),(s,actual,bound(s))
        if s<=15:rows.append((s,str(actual),witness))
    print(json.dumps(dict(mode='fiber_constants',range=[2,100],rows=rows)),flush=True)


def trials(number,seed):
    rng=random.Random(seed);hist=Counter();heavy_examples=[]
    for _ in range(number):
        m=rng.randrange(7,401);s=rng.randrange(3,min(13,m))
        B=[0]+rng.sample(range(1,m),s-1)
        res=lambda x:sum(B[i] for i in x)%m
        pairs=list(combinations_with_replacement(range(s),2))
        if len({res(x) for x in pairs})!=len(pairs):continue
        hist['pair_injective']+=1
        triples=list(combinations_with_replacement(range(s),3))
        groups={}
        for x in triples:groups.setdefault(res(x),[]).append(x)
        excess=len(triples)-len(groups)
        H=s*(s*(s-1)//2+1)
        assert m>=H-bound(s)*excess,(m,B,excess)
        assert m>=coverage_bound(s,m,excess),(m,B,excess,'complete_support')
        hist['packing_checks']+=1
        hist[f's_{s}']+=1
        if s>=6 and s%3==0:
            hist['HP_checks']+=1;k=s//3
            heavy={r:xs for r,xs in groups.items() if len(xs)==k and all(len(set(x))==3 for x in xs)}
            assert len(heavy)<=gcd(k,m)
            for r in heavy:assert (k*r-sum(B))%m==0
            hist['full_support_fibers']+=len(heavy)
            if s==9 and heavy and len(heavy_examples)<8:
                heavy_examples.append(dict(m=m,B0=B,excess=excess,heavy_fibers=heavy))
    from pathlib import Path
    Path('heavy_fiber_examples.json').write_text(json.dumps(heavy_examples,indent=2)+'\n')
    print(json.dumps(dict(mode='fiber_trials',number=number,seed=seed,counts=hist)),flush=True)


def pure_a(a):
    profiles=catalog(a);hist=Counter();survivors=[]
    Q=comb(a+1,2);U=comb(a+2,3);P=comb(a+3,3)
    H=lambda d:(d+1)*(d*(d+1)//2+1)
    for q2,q3,u3,u4,k,WA in profiles:
        rA=Q-q2-q3;t=U-u3-u4;m=P-rA-t+k
        if rA==0 and m<H(a)-bound(a+1)*t:
            hist['all_pairs']+=1;continue
        if rA==1 and m<H(a-1)-bound(a)*(t-a):
            hist['delete_missing_pair_endpoint']+=1;continue
        survivors.append((q2,q3,u3,u4,k,WA,rA,t,m))
    print(json.dumps(dict(mode='pure_A',a=a,excluded=hist,survivors=survivors)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--constants',action='store_true')
    p.add_argument('--trials',type=int,default=0);p.add_argument('--seed',type=int,default=20261023)
    p.add_argument('--a',type=int,default=0);args=p.parse_args()
    if args.constants:constants()
    if args.trials:trials(args.trials,args.seed)
    if args.a:pure_a(args.a)
