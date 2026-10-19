"""Exact necessary count profiles from LC-minus and total Macaulay."""
from math import comb,isqrt
import json
def mac2(q):
    k=(1+isqrt(1+8*q))//2
    return comb(k+1,3)+comb(q-comb(k,2)+1,2)
def run(a):
    Q=comb(a+1,2);Ca=comb(a+1,3);best=None;n=0
    for q in range(Q+1):
        r=Q-q
        cap=min(q,(a*(a-1)-1)//6,
                (3*Ca-(a+17)*r-1)//(3*(a+1)),
                (4*mac2(q)-3*a*(a+1)-(a-3)*q-1)//(a+1))
        if cap<0:continue
        n+=1
        z=cap+r;alpha=(isqrt(1+8*z)-1)//2
        if best is None or alpha>best['alpha']:
            best=dict(alpha=alpha,q=q,q2_cap=cap,rA=r,low_pair_slots=z)
    return dict(a=a,q_profiles=n,upper=best)
if __name__=='__main__':
    for a in [7,8,9,10,12,15,20,30,50,100,200,500]:print(json.dumps(run(a)),flush=True)
