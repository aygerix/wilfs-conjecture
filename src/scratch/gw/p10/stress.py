#!/usr/bin/env python3
"""Adversarial actual e=5 semigroups, q>=5, height>=4; fejer only."""
import json,math,random
from fractions import Fraction
from boundary import apery,stats,check

def run():
    rng=random.Random(51019);tested=boundary=0;best=None;min7=None
    for restart in range(24):
        m=rng.randrange(40,501);gens=sorted(rng.sample(range(m+1,5*m),4))
        score=100.0
        for step in range(180):
            gg=gens[:];a=rng.randrange(4)
            if step%13==0:gg[a]=rng.randrange(m+1,10*m)
            else:gg[a]=max(m+1,gg[a]+rng.choice([-1,1])*rng.randrange(1,max(2,m//3)))
            gg=sorted(gg)
            if len(set(gg))<4:continue
            ap=apery(m,gg,step%7==0)
            if ap is None:continue
            D,w=ap;c=max(w)-m+1;q=(c+m-1)//m;h=max(map(sum,D))
            if q<5 or h<4:continue
            tested+=1;H,t,n,ht,local=stats(D);tt=sum(t)
            ell=c-sum((v-r)//m for r,v in enumerate(w));W=5*ell-c
            if W<0:raise RuntimeError(json.dumps(dict(m=m,gens=gg,D=sorted(D),apery=w,W=W)))
            if not n[4]:check(D);boundary+=1
            ww=sorted((4+sum(x) for x in D if not ht[x]),reverse=True)
            R=sum(i*v for i,v in enumerate(ww));num=(m+1)*H+R;den=3*m*(m-1)//2
            rec=dict(m=m,gens=gg,q=q,height=h,H=H,t=t,n=n,R=R,W=W,hcr=str(Fraction(num,den)))
            if best is None or Fraction(num,den)<Fraction(best['hcr']):best=rec
            if min7 is None or H+7*tt-2*m<min7['slack']:min7=dict(slack=H+7*tt-2*m,**rec)
            ns=num/den;temp=.08*(1-step/180)+.001
            if ns<score or rng.random()<math.exp(min(0,(score-ns)/temp)):gens,score=gg,ns
    print(json.dumps(dict(seed=51019,tested=tested,boundary=boundary,min_hcr=best,min_H7=min7)))

if __name__=='__main__':run()
