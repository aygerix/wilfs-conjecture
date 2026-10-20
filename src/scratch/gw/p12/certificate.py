"""Exact polynomial-ring verification of the report certificates. Fejer only.

All coefficients are fractions.Fraction; no fitting or numerical sampling.
"""
from fractions import Fraction as F
import json

class P:
    def __init__(self,c):
        self.c=list(map(F,c if isinstance(c,(list,tuple)) else [c]))
        while len(self.c)>1 and self.c[-1]==0:self.c.pop()
    def __add__(self,b):
        b=b if isinstance(b,P) else P(b);n=max(len(self.c),len(b.c))
        return P([(self.c[i] if i<len(self.c) else 0)+(b.c[i] if i<len(b.c) else 0) for i in range(n)])
    __radd__=__add__
    def __neg__(self):return P([-x for x in self.c])
    def __sub__(self,b):return self+-b if isinstance(b,P) else self+(-F(b))
    def __rsub__(self,b):return -self+b
    def __mul__(self,b):
        b=b if isinstance(b,P) else P(b);z=[F(0)]*(len(self.c)+len(b.c)-1)
        for i,x in enumerate(self.c):
            for j,y in enumerate(b.c):z[i+j]+=x*y
        return P(z)
    __rmul__=__mul__
    def __truediv__(self,b):return self*F(1,b)
    def __pow__(self,n):
        q=P(1)
        for _ in range(n):q=q*self
        return q
    def __eq__(self,b):return self.c==(b.c if isinstance(b,P) else P(b).c)
    def strings(self):return list(map(str,self.c))

X=P([0,1]);out={}
def closed(k,odd):return (31*k**3-87*k**2-(499 if odd else 382)*k-(189 if odd else 144))/24
for odd in (0,1):
    k=2*X+odd;u=X+odd
    base=k*(k+1)*(17*k+4)/6
    low=(6*k+3)*k*u-(11*k+6)*u*(u-1)/2-u*(u-1)*(2*u-1)/3
    hole=u*(6*k+3)+u*(2*k-u-1)/2
    assert base-low-hole-2*(7*k+3)==closed(k,odd)
out['REST_from_counts']='exact identity in Q[X], both parities'

expected={17:[178,2642,1699,279],18:[918,F(6627,2),F(3677,2),279],
          19:[1346,3895,1978,279],20:[2058,F(9159,2),F(4235,2),279],
          21:[2965,5332,2257,279],22:[3932,F(12223,2),F(4793,2),279]}
rows={}
for k0 in range(17,23):
    k=k0+6*X;v=(k0+2)//3+2*X
    origin=-(k+1)*(7*k+2)+(k-v)*(13*k+5+v)/2
    if k0%3==2:origin=origin-(20*k+8)/3
    gap=closed(k,k0%2)+origin-(5*k+2)*(5*k+1)/2
    assert gap==P(expected[k0]);assert all(x>0 for x in gap.c)
    rows[k0]=gap.strings()
out['CHAIN_shift_table']=rows

k=6+X;q=24*closed(k,1);assert q==P([381,1805,471,31]);out['REST_positive_shift']=q.strings()
k=100+X;q=24*(closed(k,1)-F(5,4)*k**3);assert q==P([79911,12101,213,1]);out['REST_5_over_4_shift']=q.strings()
k=200+X;q=60*k**2-7531*k-2250;assert q==P([891550,16469,60]);out['L_110_shift']=q.strings()
print(json.dumps(out,indent=2))
