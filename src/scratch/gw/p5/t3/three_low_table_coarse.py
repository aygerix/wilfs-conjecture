"""Exact certificates for the three-low near-full quadratic face. fejer only."""
from math import comb,isqrt
import json
table=[]
for r in range(3):
    row=[]
    for l in range(6):
        s=7+l-2*r;d=9+10*l+l*l+17*r
        B1=5+5*l+7*r;B0=-15-17*l-13*r+2*comb(l+r+2,3)
        corr=2*r*(r+1)
        # G(a)=(s*a-d)(s*a-d-12)-144*(B(a)-1+corr).
        g2=s*s;g1=-s*(2*d+12)-144*B1
        g0=d*(d+12)-144*(B0-1+corr)
        A=max(13,13+3*l+2*r)
        while s*A-d<=12 or g2*A*A+g1*A+g0<0 or 2*g2*A+g1<0:A+=1
        shifted=[g2,2*g2*A+g1,g2*A*A+g1*A+g0]
        assert all(v>=0 for v in shifted)
        row.append(dict(l=l,A=A,s=s,d=d,B=[B1,B0],G=[g2,g1,g0],shifted=shifted))
    table.append(dict(r=r,row=row))
print(json.dumps(table),flush=True)

gap_cases=0
for a in range(13,301):
    Q=comb(a+1,2)
    for q in range(6,Q-2):
        j=(isqrt(8*q+1)-1)//2;s=q-comb(j+1,2)
        growth=comb(j+2,3)+comb(s+1,2)
        assert (a+2)*q-3*growth>=6*a-18
        gap_cases+=1
print(json.dumps(dict(MG6_cases=gap_cases,a=[13,300],uniform_A=max(z['A'] for rr in table for z in rr['row']))),flush=True)
