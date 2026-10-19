"""Sparse exact polynomial verification; no sympy. Execute on fejer."""
from fractions import Fraction as F
import json
names='a alpha n lx ly u0 u1 k0 k1 c0 R l qc delta b c e G D3 S JA j h q uu kk r'.split()
N=len(names);zero=(0,)*N
class P:
    def __init__(self,x=0):
        if isinstance(x,P):self.d=x.d.copy()
        elif isinstance(x,dict):self.d={k:F(v) for k,v in x.items() if v}
        else:self.d={zero:F(x)} if x else {}
    def __add__(self,o):
        d=self.d.copy()
        for k,v in P(o).d.items():d[k]=d.get(k,F(0))+v
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.d.items()})
    def __sub__(self,o):return self+-P(o)
    def __rsub__(self,o):return P(o)+-self
    def __mul__(self,o):
        d={}
        for k,v in self.d.items():
            for l,w in P(o).d.items():
                z=tuple(x+y for x,y in zip(k,l));d[z]=d.get(z,F(0))+v*w
        return P(d)
    __rmul__=__mul__
    def __truediv__(self,o):return self*F(1,o)
    def __pow__(self,n):
        r=P(1)
        for _ in range(n):r=r*self
        return r
v={}
for i,name in enumerate(names):
    z=list(zero);z[i]=1;v[name]=P({tuple(z):1})
globals().update(v)
checks=[]
def check(label,L,R):
    assert not (L-R).d,(label,(L-R).d)
    checks.append(label)
def C2(x):return x*(x-1)/2
def C3(x):return x*(x-1)*(x-2)/6

p=a-2;q2=n+lx+ly;u=u0+u1;k=k0+k1
Jrough=6+(p+1)*n+k0-u1+C2(lx+1)+C2(ly+1)
pure=a-1+(a+3)*q2+(a+1)*u-3*k-2*Jrough
check('2L-ROUGH',pure,a-13+(5-a)*n+lx*(a+2-lx)+ly*(a+2-ly)+(a+1)*u0-5*k0+(a+3)*u1-3*k1)
Jfix=6+qc+k0+3*R-u1+l
pure=a-1+(a+3)*(3+l)+(a+1)*u-3*k-2*Jfix
check('2L-FIX',pure,4*a-4+(a+1)*l-6*R+(a+1)*u0-5*k0-2*qc+(a+3)*u1-3*k1)
Jhi=9+3*p+(2*p+3)*l+k
pure=a-1+(a+3)*(3+l)+(a+1)*u-3*k+delta-2*Jhi
check('2L-HIGHARC',pure,delta-(2*a-2)-(3*a-5)*l+(a+1)*u-5*k)
fj0=(a-j)*C2(j+1)
fjj=fj0+(a+2)*j-3*C2(j+1)
check('MG2 endpoint',fjj-(2*a-2),(j-1)*(a-1-j)*(j+4)/2)
check('SIDON l0 shift',(2*(a-1)/3)*(2*(a-1)/3-1)-(2*a-3),(4*(a-7)**2+24*(a-7)+9)/9)
check('SIDON l1 shift',(5*a-9)*(5*a-15)-36*(5*a-8),25*(a-11)**2+250*(a-11)+148)
jj=a-1;ss=a-3
check('MG6 last endpoint',(a-jj)*C2(jj+1)+(a+2)*ss-3*C2(ss+1),6*a-15)
check('MG6 endpoint j3',(a-3)*C2(4)+(a+2)*3-3*C2(4),9*a-30)
jj=a-2
check('MG6 endpoint a-2',(a-jj)*C2(jj+1)+(a+2)*jj-3*C2(jj+1),(a*a+3*a-10)/2)
Jgen=alpha+(a-alpha+1)*n+c0+k0-u1+((a+3)*l-S)/2
pure=a-1+(a+3)*(n+l)+(a+1)*u-3*k-2*Jgen
check('GLOC pure identity',pure,a-1-2*alpha-2*c0+(2*alpha+1-a)*n+S+(a+1)*u0-5*k0+(a+3)*u1-3*k1)
q2=n+l;LC=(a+1)*(q2+u)-4*k
AA=(a-1)*(b+1)+G+LC+b*u+(c+e)*(2*q2+u)+D3
pay=AA+(b+2)*q2+k-2*(JA+b*(alpha+n)+alpha*c)
pure=a-1+LC+2*q2+k-2*JA
check('GLOC outside identity',pay,pure+D3+b*(a-1+q2+u-2*alpha-2*n)+G+(c+e)*(2*q2+u)-2*alpha*c)
MM=1+a+q+uu+kk;WA=3*a*(a+1)+(a-3)*q-4*uu+G
check('pure-A cardinality identity',WA+MM-h,(a+1)**2+4*(C2(a+1)-q)+G+kk+(a+2)*q-3*uu-h)
malpha=(a-2*alpha-1)*C2(alpha+1)+2*alpha+2*C3(alpha+2)-a+1
check('general rough constant',malpha,(C2(alpha+1)-1)*a+2*alpha+1-alpha*(alpha+1)*(4*alpha-1)/6)
dm=r*(4*a-3*r-1)/2
sharpA=(7+r+l)*a-21+2*l-l*l-r*(3*r+7)/2
check('three-low retained fixed gap',a-39+(a+3)*(6-r)+l*(a+2-l)+dm,sharpA)
oldB=(5+5*l+7*r)*a-15-17*l-13*r+2*C3(l+r+2)
sharpB=(5+5*l+5*r)*a-15-17*l-13*r+2*C3(l+r+2)+r*(3*r+1)/2
check('three-low retained high gap',oldB-dm,sharpB)
check('three-low threshold shift',sharpA-12*(l+r),(7+r+l)*a-(21+10*l+l*l+r*(3*r+31)/2))
hiCount=19+l+(l+r)+C3(l+r+2)+(6+3*(l+r))*(a-3)
check('three-low high count expansion',a-1+(a+3)*(6-r+l)-2*hiCount,-oldB)
for rr in range(3):
    tt=5-2*rr
    check('three-low gap stars r='+str(rr),15-5*a+rr*(4*a-3*rr-1)/2+tt*(a+2-tt),[0,10,9][rr])
print(json.dumps(dict(verified=len(checks),identities=checks)),flush=True)
