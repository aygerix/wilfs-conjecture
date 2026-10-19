"""Exact heavy-fiber family and signed-label loss. Run on fejer.

This refutes an n-independent defect constant for the cardinality
of the standard signed-label union, NOT for the ambient modulus.
The augmented family is an implicit residue-complete primary tile
with LC-minus for every g>=3; its E fill is specified by a formula.
"""
from itertools import combinations_with_replacement as cwr
from collections import Counter
from math import comb
import json

out=[]
for g in range(2,13):
    R=10**(4*g)
    A=[]
    for i in range(g):
        x,y=10**(2*i),10**(2*i+1)
        A.extend([R+x,R+y,2*R-x-y])
    pair=Counter(sum(z) for z in cwr(A,2))
    triple=Counter(sum(z) for z in cwr(A,3))
    assert max(pair.values())==1
    assert sorted(v for v in triple.values() if v>1)==[g]
    assert triple[4*R]==g
    signed=set(A)
    for i,x in enumerate(A):
        B=A[:i]+A[i+1:]
        signed.update(p+q-x for p,q in cwr(B,2))
    n=3*g;H=n*(comb(n,2)+1)
    assert len(signed)==H-9*comb(g,2)
    extra=[3*R-10**(2*g+j) for j in range(2*g)]
    allA=A+extra;a=len(allA);h=3*R+2;m=10*R
    vals=Counter()
    for d in range(4):
        for z in cwr(range(a),d):vals[sum(allA[i] for i in z)]+=1
    assert sorted(v for v in vals.values() if v>1)==[g]
    assert h-1 not in vals
    assert max(vals)<m
    q2=sum(sum(z)<h for z in cwr(allA,2))
    assert q2==3*g*g+2*g
    assert min(sum(z) for z in cwr(allA,3))>h-1
    assert sum(2*x<h for x in allA)==2*g
    f=comb(a+1,3);lc=(a+1)*q2;wa=-f+lc+4*(g-1)
    if g>=3:
        assert wa<0 and 3*(a+1)*q2<3*f
    out.append(dict(g=g,n=n,epsilon=g-1,H=H,signed_union=len(signed),
        loss=9*comb(g,2),loss_per_epsilon=[9*g,2],
        a=a,alpha=2*g,q2=q2,u3=0,k=0,t=g-1,LC=lc,WA=wa,
        R=str(R),m=str(m),h=str(h),A=[str(x) for x in allA]))
with open('fiber_family.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps(dict(verified=len(out),first=out[:2],last_summary={k:v for k,v in out[-1].items() if k!='A'})),flush=True)
