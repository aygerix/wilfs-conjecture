"""Adversarial q2=2,3 five-A faces, with complete residue fillings.
Run on fejer only. Complements the q2=0,1 completion probe.
"""
from continuation_probe import monos,completed,a5_checks,extend
from collections import Counter
import random
import json
import argparse


def run(trials,seed):
    rng=random.Random(seed);hist=Counter();best=None
    for trial in range(trials):
        m=rng.randrange(200,701);h=rng.randrange(24,m//2+1);q2=2+trial%2
        t0=rng.randrange(3,(h-5)//2+1)
        middle=range((h+1)//2,h-t0)
        if len(middle)<q2-1:continue
        mids=sorted(rng.sample(middle,q2-1))
        highs=sorted(rng.sample(range(h-t0,h),5-q2))
        ts=(t0,)+tuple(mids)+tuple(highs);n=tuple(m+t for t in ts);M=4*m+h-1
        core={x for x in monos(5,4) if sum(a*b for a,b in zip(x,n))<=M}
        vals={sum(a*b for a,b in zip(x,n))%m for x in core}
        if len(vals)!=len(core) or (h-1)%m in vals:continue
        D,nn=completed(core,n,m,h);st=a5_checks(D,nn)
        if st is None or st['WA']>=0:continue
        assert st['q2']==q2
        hist[f'profile_{q2}_{st["u3"]}_{st["k"]}']+=1
        ss=st
        for step in range(2):
            options=[]
            for w in rng.sample(range(m+h,2*m+h),min(m,12)):
                out=extend(core,n,w,m,h,rng)
                if out is not None:options.append(out)
            if not options:break
            core,n=max(options,key=lambda item:len(item[0]))
            D,nn=completed(core,n,m,h);ss=a5_checks(D,nn)
            assert ss['WA']==st['WA'] and ss['W']>=0
            hist[f'checked_b{step+1}']+=1
        hist['accepted']+=1
        if best is None or ss['W']<best['W']:best=ss
    print(json.dumps(dict(trials=trials,seed=seed,counts=hist,best=best)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=5000);p.add_argument('--seed',type=int,default=20261022)
    args=p.parse_args();run(args.trials,args.seed)
