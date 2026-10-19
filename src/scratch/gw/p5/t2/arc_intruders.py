"""Adversarial test of a proposed pure-A arc payment. fejer only.

Relaxed inputs: arbitrary finite down-sets cut from degree <=4, scale
m independent of cardinality, all 1<=t<h, v<=4m+h-1. A failure only
refutes the scale/cardinality-free payment, not Wilf.
"""
import itertools as it
import random,json,argparse
from collections import Counter

def mons(a,k):
    for z in it.combinations_with_replacement(range(a),k):
        yield z

def evaluate(t,m,h,chosen):
    a=len(t);theta=(3*h+1)//2;q2=u3=k=J=0
    full=set(chosen)
    for x in full:
        tau=sum(t[j] for j in x);v=len(x)*m+tau
        assert v<=4*m+h-1
        q2+=len(x)==2 and tau<h
        u3+=len(x)==3 and tau<h
        k+=len(x)==4
        r=tau%m
        iny=(h<=r<min(theta,m)) or (1<=r<theta-m)
        allowed=len(x)==2 and tau>=h
        J+=iny and not allowed
    LC=(a+1)*(q2+u3)-4*k
    slack=(a-1)+LC+2*q2+k-2*J
    return dict(a=a,m=m,h=h,t=t,q2=q2,u3=u3,k=k,J=J,LC=LC,slack=slack,
                cardinality=len(full)+1,residues=len({sum(t[j] for j in x)%m for x in full}|{0}))

def trial(a,m,h,rng):
    t=sorted(rng.randrange(1,h) for _ in range(a))
    D=set((j,) for j in range(a))
    for deg in range(2,5):
        for x in mons(a,deg):
            if deg*m+sum(t[j] for j in x)>4*m+h-1:continue
            if all(x[:j]+x[j+1:] in D for j in range(deg)):
                if rng.randrange(8) or rng.randrange(2):D.add(x)
    return evaluate(t,m,h,D),D

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=20000);p.add_argument('--seed',type=int,default=202610191)
    args=p.parse_args();rng=random.Random(args.seed);hist=Counter();best=None;fail=None
    for i in range(args.trials):
        a=rng.randrange(2,16);m=rng.randrange(a+2,1000);h=rng.randrange(2,m+1)
        out,D=trial(a,m,h,rng);hist['trials']+=1
        if best is None or out['slack']<best['slack']:best=out
        if out['slack']<0:
            fail=dict(out,D=sorted(D));break
    print(json.dumps(dict(seed=args.seed,counts=hist,best=best,failure=fail)),flush=True)
