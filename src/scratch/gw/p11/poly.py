"""P11 exact coefficient checks. RUN ON FEJER ONLY; no sympy.

This is an algebra verifier, not a numerical semigroup census.
"""
from fractions import Fraction as F
from collections import defaultdict
from math import comb

class P:
    dim = 6
    def __init__(self, value=0):
        self.d = dict(value) if isinstance(value, dict) else ({(0,)*self.dim:F(value)} if value else {})
    def __add__(self, other):
        other = other if isinstance(other,P) else P(other)
        d = defaultdict(F,self.d)
        for k,v in other.d.items(): d[k] += v
        return P({k:v for k,v in d.items() if v})
    __radd__ = __add__
    def __neg__(self): return P({k:-v for k,v in self.d.items()})
    def __sub__(self,other): return self+-other if isinstance(other,P) else self+(-F(other))
    def __rsub__(self,other): return -self+other
    def __mul__(self,other):
        other = other if isinstance(other,P) else P(other)
        d=defaultdict(F)
        for a,u in self.d.items():
            for b,v in other.d.items(): d[tuple(x+y for x,y in zip(a,b))] += u*v
        return P({k:v for k,v in d.items() if v})
    __rmul__ = __mul__
    def __truediv__(self,other): return self* (1/F(other))
    def __pow__(self,n):
        out=P(1)
        for _ in range(n): out=out*self
        return out

def var(i): return P({tuple(int(j==i) for j in range(P.dim)):F(1)})
checks=[]
def eq(name,a,b):
    diff=a-b
    assert not diff.d,(name,diff.d)
    checks.append(name)

A,T,V,a,ep,n=[var(i) for i in range(6)]
Q=A*(A+1)/2; U=Q*(A+2)/3
y=2*A*T/9; aa=2*A+1+6*y+2*A*V; ee=Q*y
nu=aa/2+2*A/3+F(5,6)+3*y/2
B0=(aa-2*A-1)*Q+2*U+2*A-aa+1
w=T+V
g=w**3+5*w**2-F(14,3)*w+F(44,27)
j=3*w**2-3*w-F(2,3)
actual=nu**3-nu**2+2*nu-9*B0-63*ee+10
certificate=A**2*((A-4)*g+4*g+j)+4*(A**3+A**2)*V+A*(F(16,9)+F(50,3)*T+F(68,3)*V)+F(358,27)
eq('P45 B0 identity',actual,certificate)
eq('nu identity',nu,A*(w+F(5,3))+F(4,3))
eq('g45 lower square',g,w**3+F(44,9)*(w-F(17,33))**2+(w+F(5,3))**2/9+F(7,297))
eq('4g45+j45',4*g+j,4*w*(w-F(1,2))**2+27*(w-F(34,81))**2+F(266,243))

B=(a-2*A-1)*Q+2*U+2*A-a+1
vv=a/2+2*A/3+F(5,6)+3*ep/(2)  # ep here is epsilon/Q
eq('epsilon elimination',vv**3-127*vv**2+8*vv-9*B-63*Q*ep+10,
   vv**3-127*vv**2+(8-42*Q)*vv+(12*a+40*A)*Q+32*Q-18*A+9*a+1)

z=n
eq('general positive cubic',z**3-z**2/32-(21+F(1,128))*z+38-F(83,4096),
   (z-F(8,3))**2*(z+F(509,96))+F(61,384)*z+F(30527,110592))
eq('1280 positive cubic',z**3-z**2/10-(21+F(1,60))*z+38-F(1,15),
   (z-F(27,10))**2*(z+F(53,10))+F(47,150)*z-F(2111,3000))
assert F(47,150)*F(9,4)-F(2111,3000)==F(1,750)
assert (F(27,10)-F(9,4))**2*F(53,10)-F(2111,3000)==F(887,2400)
eq('delta error at a=3A',3*A**2-(2+Q+3*A+(A+1)*(A+2)/3),
   (13*(A-3)**2+51*(A-3)+20)/6)
eq('low H identity',
   4*a-6*A+(6*A+6-2*a)*Q-6*U,
   4*a-6*A+2*(2*A+1-a)*Q)

eq('linear-threshold square',a**3/104-F(15,26)*A*a*a+F(45,2)*A*A*a,
   a**3/169+F(45,2)*a*(A-a/78)**2)
eq('error cubic is bounded',11*a**3-(24*a*n*n-13*n**3),
   (a-n)**2*(11*a+13*n)+9*a*n*(a-n))
eq('linear final margin',a**3/169+F(47,52)*a*a-11*a**3/2197-36*a*a/169-F(40,13)*a,
   2*a**3/2197+F(467,676)*a*a-F(40,13)*a)

# Exact integer/rational stress of every scalar bound in the proof.
rows=0
for M in range(101):
    K=126+M; Al=9*K+6; Y=F(5*Al,3)
    assert (Al-4)*Y*Y/9-K*(Y+F(4,3))**2>0
    for rr in range(13):
      for ll in range(8):
       for bb in range(8):
        D=rr+ll+bb; Al=4096*(D+M+1)
        Ql=F(Al*(Al+1),2); Ul=Ql*(Al+2)/3
        assert Ql-rr>=Ql/2
        assert Ul*rr/(Ql*(Ql-rr))<=rr
        assert bb*Ql/(2*(Ql-rr))<=bb
        cc=127+M
        assert cc+6*D<=F(Al,32)
        loss=8*D**3+4*cc*D**2+16*D
        assert loss<=F(Al**3,2048)
        for aa in (3*Al,4*Al,10*Al,5*Al*(Al+1)-1):
            bound=2*D*(1+Al*aa)+2*comb(D+2,3)+bb*(Ql+3*D)
            assert bound<=3*D*Al*aa
            assert (12*aa+40*Al)*Ql-27*D*Al*aa >= (38-F(81,4096))*Al**3
            rows+=1
linear_rows=0;stable_rows=0
for Al in range(6,41):
 for D in range(21):
  for M in range(21):
   SS=Al+D+M+22; aa=13*SS; cc=127+M; CC=cc+6*D
   Ql=F(Al*(Al+1),2)
   assert CC<=6*SS-6*Al-5*M-5
   assert 42*Ql<=21*SS*SS
   assert F(aa,2)-2*D>F(2*cc,3)
   assert 3*F(aa,2)**2-2*CC*F(aa,2)-42*Ql>0
   loss=11*D**3+(4*cc+36)*D**2+40*D
   assert loss<=11*SS**3+36*SS**2+40*SS
   aa_min=F(aa**3,8)-F(CC*aa*aa,4)-9*aa*Ql-27*D*Al*aa-loss
   final=F(2*aa**3,2197)+F(467*aa**2,676)-F(40*aa,13)
   assert aa_min>=final
   linear_rows+=1
for D in range(101):
 for M in range(101):
    Al=1280*(D+M+1);aa=3*Al;cc=127+M
    Ql=F(Al*(Al+1),2)
    assert D<=Al
    assert cc+6*D<Al/F(10)
    assert 42*Ql/Al**2<21+F(1,60)
    loss=8*D**3+4*cc*D**2+16*D
    assert loss<=F(Al**3,512)
    assert F(81,1280)+F(1,512)<F(1,15)
    assert (12*aa+40*Al)*Ql-27*D*Al*aa >= (38-F(81,1280))*Al**3
    stable_rows+=1
bad_coarsening=None
for D in range(1,1001):
    Al=6;aa=13*(Al+D+22)
    actual=2*D*(1+Al*(aa-Al))+2*comb(D+2,3)
    false_bound=3*D*Al*aa
    if actual>false_bound:
        bad_coarsening=dict(alpha=Al,D=D,a=aa,E=D,b=0,l=0,T=actual,false_bound=false_bound)
        break
assert bad_coarsening['D']==258
print({'status':'PASS','coefficient_identities':checks,'scalar_rows':rows,
       'linear_rows':linear_rows,'stable_rows':stable_rows,'B0_threshold':'alpha >= 1140+9M',
       'linear_threshold':'a >= 13(alpha+D+M+22), n0 >= Q_alpha/2',
       'stable_threshold':'alpha >= 1280(D+M+1), a >= 3alpha',
       'failed_unrestricted_coarsening':bad_coarsening,
       'light_B0_finite_box':{'alpha_max':1139,'a_max':15092,
           'm_upper':comb(15095,3)+comb(1142,4)+(15092**2-1)//3}})
