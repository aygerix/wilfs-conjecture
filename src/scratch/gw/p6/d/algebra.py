"""Exact rational endpoint and finite local counterexample audits, fejer only."""
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr
from core import evaluate
from math import comb
import json

for v in range(33,1001):
    d=(F(129,1792)-F(1,16))*v**3-F(9,32)*v**2-F(3,4)*v
    assert 1792*d==v*(17*(v-33)**2+618*(v-33)+537)
    assert d>0
for k in range(67,1001):
    diff=(k-1)**3-64*(k*k-k+4)
    x=k-67
    assert diff==x**3+134*x*x+4556*x+4232>0
for k in (3,4,5):
    lower=F(k*(k*k+3*k-10),20)+F(k*k-8*k+10,30)*comb(k+1,2)
    assert lower=={3:F(1,5),4:F(8,5),5:F(5)}[k]
    print('BAD-NARROW small k',k,'lower',str(lower))

# Exact local enumeration, not an exhaustive shape certificate at larger m.
first=None; tested=0
for m in range(4,9):
    for k in (1,2,3):
        for U in cwr(range(1,m),k):
            if len(set(U))<k:continue
            for y in cwr(range(k),3):
                if set(y)!=set(range(k)):continue
                Q={y[:j]+y[j+1:] for j in range(3)}
                vals=[0,*U]+[(sum(U[i] for i in z))%m for z in Q]+[sum(U[i] for i in y)%m]
                if len(vals)>m or len(vals)!=len(set(vals)):continue
                tested+=1
                a=evaluate(m,list(U),Q,{y},0)
                if a['beta'] and any(2*U[i]<m for i in y):
                    w=dict(m=m,U=U,Q=sorted(Q),T=[y],evaluation=a)
                    if first is None:first=w
    if first is not None:break
assert first['m']==8
print('first origin-bad low-factor witness',json.dumps(first,sort_keys=True))
print('local injective cores tested through first witness modulus',tested)
print('large dimension and cluster algebra: all exact checks passed')
rho=4;ell3=-8;ell4=-12
assert 3*ell4+rho==4*ell3
assert 3*ell4+2*rho!=4*ell3
print('quartic wrong-lift counterexample: m=5, P=1, sigma=1, rho=4, ell3=-8, ell4=-12')
