"""Exact finite audits of the symbolic T2.2 formulas. Run on fejer only.

The proof is in P5_REPORT.md; these loops audit its formulas, not prove
the assertions beyond their explicitly printed finite ranges.
"""
from math import comb,isqrt
import json

def mac(q):
    k=(isqrt(8*q+1)-1)//2
    r=q-comb(k+1,2)
    return comb(k+2,3)+comb(r+1,2)

out={}
gap_n=0;gap_min=10**9
for a in range(7,301):
    for q in range(2,comb(a+1,2)):
        d=(a+2)*q-3*mac(q)
        assert d>=2*a-2
        gap_n+=1;gap_min=min(gap_min,d-(2*a-2))
out['macaulay_gap']=dict(a=[7,300],cases=gap_n,min_slack=gap_min)

rough_n=0;rough_min=10**9
for a in range(7,301):
    for n0 in range(4):
        for l1 in range(a-1):
            for l2 in range(a-1):
                z=a-13+(5-a)*n0+l1*(a+2-l1)+l2*(a+2-l2)
                assert z>=2-2*a
                if l1+l2>=2:assert z>=2
                rough_n+=1;rough_min=min(rough_min,z-(2-2*a))
out['rough']=dict(a=[7,300],cases=rough_n,min_slack=rough_min)

cold_n=0
for a in range(7,101):
    for qc in range(4):
        for u0 in range(5):
            growth=[0,1,2,3,5][u0]
            for k0 in range(growth+1):
                for t0 in range(5-u0):
                    if qc and u0+t0<qc+1:continue
                    assert (a+1)*u0-5*k0+3*t0>=2*qc
                    cold_n+=1
out['cold']=dict(a=[7,100],cases=cold_n)

alt_n=0
for a in range(7,1001):
    for l in (0,1):
        for R in range(a-1):
            nn=max(0,R-l)
            dlo=nn*(nn-1)+1
            B=2*a-2+(3*a-5)*l
            if 4*a-4+(a+1)*l-6*R<0:assert dlo>=B
            alt_n+=1
out['sidon_alternative']=dict(a=[7,1000],cases=alt_n)

out['a7_exception']=dict(mac26=mac(26),mac26_minus26=mac(26)-26,
    high_r0=24+comb(7,3)-comb(8,3),
    high_r1=24+comb(6,3)-comb(8,3)+5+12)
assert out['a7_exception']['high_r0']==3
assert out['a7_exception']['high_r1']==5
print(json.dumps(out,sort_keys=True),flush=True)
