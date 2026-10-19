"""Exact polynomials for the dense full-pair theorem. Run on fejer only."""
from fractions import Fraction as F
from math import comb
import json
from pathlib import Path

def add(*ps):
    z=[F(0)]*max(map(len,ps))
    for p in ps:
        for j,x in enumerate(p):z[j]+=x
    while len(z)>1 and not z[-1]:z.pop()
    return z
def mul(a,b):
    z=[F(0)]*(len(a)+len(b)-1)
    for j,x in enumerate(a):
        for k,y in enumerate(b):z[j+k]+=x*y
    return z
def scale(p,c):return [F(c)*x for x in p]
def shift(p,A):return [sum(p[j]*comb(j,i)*A**(j-i) for j in range(i,len(p))) for i in range(len(p))]
def val(p,k):return sum(x*k**j for j,x in enumerate(p))

Q=[F(0),F(1,2),F(1,2)]
U=[F(0),F(1,3),F(1,2),F(1,6)]
M=[F(1),F(3,2),F(5,4),F(1,4)]
N=[F(5,4),F(5,4),F(1,2)]
J=scale(mul(N,add(N,[-1])),F(1,2))
B=add([F(-1,4),F(1,4)],scale(U,2))
D=add(mul(add(M,scale(add(Q,U),-1)),J),scale(mul(B,add(M,[-1])),-1))
print('POLY_D',list(map(str,D)))
for A in range(1,20):
    sh=shift(D,A)
    if all(x>=0 for x in sh):
        print('FIRST_NONNEGATIVE_SHIFT',A,list(map(str,sh)));break
small=[]
for k in range(3,8):
    q=comb(k+1,2);u=comb(k+2,3);h=(k**3+2*k*k+3*k+2)//2
    for r in range(k*(k-1)//12+1):
        # A missing cubic can spoil <=3 successor-complete pair rows, each
        # having <=k labels. A maximal pair needs all k upper cubics absent.
        m0=max(1+k+q+u-r,h-3*k*r)
        amin=0;amax=min(q,3*r//k)
        for a in range(amax+1):
            p=q-a;t=u-r;j=comb(1+k+p,2);b=a+2*t
            cr=(m0-q-t)*j-b*(m0-1)+t*(t-1)+a*t+a*(a-1)//2
            assert cr>=0,(k,r,a,m0,cr)
            small.append(dict(k=k,r=r,a=a,m_lower=m0,CR=cr))
print('SMALL_DENSE',json.dumps(small,sort_keys=True))
old=dict(D=list(map(str,D)),shift=A,coefficients=list(map(str,sh)),small=small)
# Stronger theorem r <= floor(k^2/9), using exact CR and weighted row loss.
M9=[F(1),F(3,2),F(4,3),F(1,6)]
N9=[F(1),F(7,6),F(1,2)]
J9=scale(mul(N9,add(N9,[-1])),F(1,2))
B9=add([0,F(1,3)],scale(U,2))
tmin=add(U,[0,0,F(-1,9)])
D9=add(mul(add(M9,scale(add(Q,U),-1)),J9),
       scale(mul(B9,add(M9,[-1])),-1),mul(tmin,add(tmin,[-1])))
print('POLY_D9',list(map(str,D9)))
for A9 in range(3,101):
    sh9=shift(D9,A9)
    if all(x>=0 for x in sh9):
        print('FIRST_NONNEGATIVE_SHIFT_D9',A9,list(map(str,sh9)));break
else:raise AssertionError('No positive coefficient shift <=100')
small9=[]
for k in range(3,A9):
    q=comb(k+1,2);u=comb(k+2,3);h=(k**3+2*k*k+3*k+2)//2
    for r in range(k*k//9+1):
        m0=max(1+k+q+u-r,h-3*(k-1)*r)
        amax=0 if r<k else min(q,3*r//k)
        for a in range(amax+1):
            p=q-a;t=u-r;j=comb(1+k+p,2);b=a+2*t
            cr=(m0-q-t)*j-b*(m0-1)+t*(t-1)+a*t+a*(a-1)//2
            assert cr>=0,(k,r,a,m0,cr)
            small9.append(dict(k=k,r=r,a=a,m_lower=m0,CR=cr))
print('SMALL_DENSE9_SUMMARY',len(small9),min(z['CR'] for z in small9))
# Avoid decoupling t and the same missing-cubic parameter r.  The exact
# CR expression is decreasing in a and concave in r on this interval.
H=[F(1),F(3,2),F(1),F(1,2)]
def crpoly(r,a):
    m=add(H,scale(mul([-3,3],r),-1))
    t=add(U,scale(r,-1));n=add([1,1],Q,scale(a,-1))
    j=scale(mul(n,add(n,[-1])),F(1,2));b=add(a,scale(t,2))
    return add(mul(add(m,scale(add(Q,t),-1)),j),
        scale(mul(b,add(m,[-1])),-1),mul(t,add(t,[-1])),
        mul(a,t),scale(mul(a,add(a,[-1])),F(1,2)))
ends={}
for label,r in [('zero',[0]),('max',[0,0,F(1,9)])]:
    f=crpoly(r,[0,F(1,3)])
    for Aend in range(3,30):
        coef=shift(f,Aend)
        if all(x>=0 for x in coef):break
    else:raise AssertionError(label)
    print('EXACT_ENDPOINT',label,'poly',list(map(str,f)),'shift',Aend,'coeff',list(map(str,coef)))
    ends[label]=dict(poly=list(map(str,f)),shift=Aend,coeff=list(map(str,coef)))
Mnear=[F(1),F(27,20),F(81,100),F(429,2000)]
Nnear=[F(1),F(5,4),F(1,2)]
Jnear=scale(mul(Nnear,add(Nnear,[-1])),F(1,2))
Bnear=add([0,F(3,20)],scale(U,2))
Dnear=add(mul(add(Mnear,scale(add(Q,U),-1)),Jnear),
          scale(mul(Bnear,add(Mnear,[-1])),-1))
assert all(x>0 for x in shift(Dnear,20))
print('NEAR20',list(map(str,Dnear)),'shift20',list(map(str,shift(Dnear,20))))
Path('dense_poly.json').write_text(json.dumps(dict(preliminary=old,D9=list(map(str,D9)),shift9=A9,
    coefficients9=list(map(str,sh9)),small9=small9,endpoints=ends,
    near20=dict(poly=list(map(str,Dnear)),shift=20,coeff=list(map(str,shift(Dnear,20))))),indent=2)+'\n')
print('DENSE_POLY_ALL_PASS')
