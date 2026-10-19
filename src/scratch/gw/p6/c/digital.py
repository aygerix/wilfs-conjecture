"""Mixed-radix stars, every phase, arbitrary heights, spike lifts.
Run only on fejer, nice and single-core. Exact integer arithmetic.
"""
from itertools import product
from math import comb,prod
from collections import Counter
from pathlib import Path
import random,json
rng=random.Random(2026101951);stats=Counter();saved=[]
def one(rs,x):
    H=len(rs);k=sum(rs);m0=prod(r+1 for r in rs);t=prod(rs);m=m0+x;d=k+x
    bases=[];B=1
    for r in rs:bases.append(B);B*=r+1
    top={sum(a*b for a,b in zip(aa,bases)) for aa in product(*[range(1,r+1) for r in rs])}
    assert len(top)==t and (k+H)*t<=k*m0
    f=0
    for sig in range(m0+1):
        assert m0*f<=t*sig
        f+=sig in top
    A=sum(top);Nsum=m0*(m0-1)//2-A
    assert 2*A==t*sum((r+1)*b for r,b in zip(rs,bases))
    S0=(k+1)*Nsum-(H-1)*A;assert S0>=0
    coeff=[(d+1 if v not in top else -(H-1)) if v<m0 else 0 for v in range(m)]
    S=sum(v*w for v,w in enumerate(coeff));C=sum(coeff);mn=(S,0)
    # Independent base-phase sums, for the exact lifting identity.
    basecoef=[k+1 if v not in top else -(H-1) for v in range(m0)]
    Sb=sum(v*w for v,w in enumerate(basecoef));Cb=sum(basecoef)
    NS=Nsum;TS=A;fN=fT=0
    for sig in range(m):
        if S<mn[0]:mn=(S,sig)
        assert S>=0
        if sig<m0:
            assert S==Sb+x*(NS+(k+1)*fN-(H-1)*fT)+x*x*fN
            assert (k+1)*fN>=(H-1)*fT
            assert Sb>=S0
            Sb+=m0*basecoef[sig]-Cb
            NS+=m0*(sig not in top)-(m0-t)
            TS+=m0*(sig in top)-t
            fN+=sig not in top;fT+=sig in top
        else:
            y=m-sig
            assert S==S0+x*Nsum+y*((k+x+1)*(m0-t)-(H-1)*t)
        S+=m*coeff[sig]-C;stats['phases']+=1
    assert S==sum(v*w for v,w in enumerate(coeff))
    stats['tiles']+=1;stats['height_'+str(H)]+=1
    if len(saved)<15 or (H==3 and rs==[11]*3):saved.append(dict(rs=rs,spikes=x,m=m,k=k,minS=mn,S0=S0))
    return mn

for rs in product(range(1,6),repeat=3):
    for x in (0,1,2,7):one(list(rs),x)
for H in range(2,8):
    for rep in range(12):
        rs=[rng.randint(1,3) for _ in range(H)]
        one(rs,rng.randint(0,12))
for x in (0,1,30,1000):one([11]*3,x)

# A failed intermediate formula: omitting maximal spikes from the top form.
wrong=5*comb(9,2)-7*8
actual=one([1,1,1],1)
assert wrong==124 and actual==(91,0)

# Exact CR family polynomial and its all-negative shift at r>=11.
poly=[0,3,21,52,51,15,-2] # 2R(r)
neg_div=[-3,-21,-52,-51,-15,2] # -2R(r)/r
shift=[sum(neg_div[j]*comb(j,i)*11**(j-i) for j in range(i,6)) for i in range(6)]
assert all(v>0 for v in shift)
for r in range(1,401):
    k=3*r;m=(r+1)**3;q=p=3*r*r;t=r**3
    R=(k+1)*comb(1+k+p,2)-2*t*(m-1)+t*(t-1)
    assert 2*R==sum(v*r**j for j,v in enumerate(poly))
    assert (R<0)==(r>=11)
out=dict(seed=2026101951,stats=dict(stats),saved=saved,
         negative_CR_shift_at_11=shift,failed_spike_top_formula=dict(claimed=wrong,actual=actual))
Path('digital.json').write_text(json.dumps(out,indent=2)+'\n')
print('DONE',json.dumps(out,sort_keys=True),flush=True)
