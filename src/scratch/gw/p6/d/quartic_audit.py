"""Smallest all-phase and origin-phase quartic window-loss witnesses."""
from math import gcd
from collections import Counter
import json
from window_h import check

first=None;origin=None;tested=0
for m in range(5,8):
    for P in range(1,m):
        if m//gcd(m,P)<5:continue
        for sig in range(m):
            rho=(-sig)%m;u=(P-sig)%m
            r3=(3*P-sig)%m;r4=(4*P-sig)%m
            K3=(3*u-2*rho-r3)//m;K4=(4*u-3*rho-r4)//m
            kap=3*K4-4*K3;b=kap+int(r4>=m-rho)
            tested+=1
            if b<=-2:
                ans=dict(m=m,P=P,sigma=sig,rho=rho,u=u,r3=r3,r4=r4,
                         K3=K3,K4=K4,kappa=kap,b=b)
                if first is None:first=ans
                if sig==0 and origin is None:origin=ans
assert first['m']==5 and origin['m']==7
stats=Counter();minima={};C={tuple([0]*h) for h in range(5)}
check(C,[4],5,stats,minima)
assert minima['H4']['HC']==0
out=dict(first_any_phase=first,first_origin=origin,tested=tested,stats=stats,minima=minima)
print(json.dumps(out,sort_keys=True),flush=True)
with open('quartic_audit.json','w') as f:json.dump(out,f,indent=2)
