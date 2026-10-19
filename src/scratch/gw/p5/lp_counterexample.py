"""Exact verification of the smallest positive-(a,b) LP-bound failure."""
from fractions import Fraction as F
x=dict(q=F(3),u=F(4),s=F(28,11),S=F(16,11),H=F(0),
       t=F(21,11),T=F(12,11),I=F(0),v=F(42,11),w=F(42,11),
       z=F(28,11),rho=F(133,11))
q,u,s,S,H,t,T,I,v,w,z,rho=(x[n] for n in 'q u s S H t T I v w z rho'.split())
assert all(y>=0 for y in x.values())
assert q<=3 and 3*u<=4*q and s+S<=4 and H<=0 and t+T<=3 and I<=0
assert v<=2*q and 2*v<=3*s and w<=2*t and 2*w<=3*s and 3*z<=4*t
assert rho>=t+I+v+w+z
assert rho>=-1-q+u+s-S+H+t-T+I+v+w+z
W=5*(6+4+q+s+t)-4*sum(x[n] for n in x if n!='rho')+rho
assert W==F(29,11)<3
assert 3*z>4*t-2*t*(3-t)/5
print('Exact LP witness at (a,b,c,e)=(2,2,0,0): W=',W,'< 3; violates MC.')
