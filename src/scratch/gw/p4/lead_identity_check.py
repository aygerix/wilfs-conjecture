# Lead's independent exact symbolic check of the P4 identities (4) W = WA + T + R and (5) 3WA = ... (P4_REPORT §3).
# Tiny exact polynomial arithmetic (dict monomial -> Fraction), no external packages.
from fractions import Fraction as Fr
class P:
    def __init__(s, t=None): s.t = {k: v for k, v in (t or {}).items() if v != 0}
    @staticmethod
    def var(n): return P({((n, 1),): Fr(1)})
    @staticmethod
    def const(c): return P({(): Fr(c)})
    def __add__(s, o):
        o = o if isinstance(o, P) else P.const(o); r = dict(s.t)
        for k, v in o.t.items(): r[k] = r.get(k, 0) + v
        return P(r)
    __radd__ = __add__
    def __neg__(s): return P({k: -v for k, v in s.t.items()})
    def __sub__(s, o): return s + (-(o if isinstance(o, P) else P.const(o)))
    def __rsub__(s, o): return P.const(o) - s
    def __mul__(s, o):
        o = o if isinstance(o, P) else P.const(o); r = {}
        for k1, v1 in s.t.items():
            for k2, v2 in o.t.items():
                m = dict(k1)
                for n, e in k2: m[n] = m.get(n, 0) + e
                k = tuple(sorted(m.items())); r[k] = r.get(k, 0) + v1 * v2
        return P(r)
    __rmul__ = __mul__
    def __truediv__(s, c): return P({k: v / c for k, v in s.t.items()})
names = 'a b c e q2 q3 s3 s4 h t3 t4 i u3 u4 v2 v3 w z k rho'.split()
a,b,c,e,q2,q3,s3,s4,h,t3,t4,i,u3,u4,v2,v3,w,z,k,rho = [P.var(n) for n in names]
d = a+b+c+e; Q = a*(a+1)/2; B = b*(b+1)/2
N = q2+q3+s3+s4+h+t3+t4+i+u3+u4+v2+v3+w+z+k
ell4 = 3*a+2*b+c+2*q2+q3+s3+t3+u3
W = (d+1)*ell4 - 4*N + rho
WA = 3*a*(a+1)+(2*a-2)*q2+(a-3)*(q3+u3)-4*(u4+k)
T = (a*b-s3)+c*(c+1)+e*(3*a+2*b+c)+(c+e)*(2*q2+q3+s3+t3+u3)+b*u3
R = (4*(a*b-s3-s4)+4*(a*c-h)+4*(B-t3-t4)+(rho-t3-i-v3-w-z)+3*(b*c-i)+((b+2)*t3-3*z)
     +(a*t3+(b+1)*s3-3*w)+(2*b*q2+b*q3+(a+1)*s3-4*v2-3*v3))
print("identity (4): W - WA - T - R has", len((W-WA-T-R).t), "nonzero terms")
D3 = (a+2)*(q2+q3)-3*(u3+u4); Dlow = (a+2)*q2-3*u3; D4 = (a+3)*u3-4*k
print("identity (5): 3WA - RHS has", len((3*WA-(18*(Q-q2-q3)-(a-1)*q3+4*D3+2*Dlow+3*D4)).t), "nonzero terms")
# EF saturated face (rho=0): W - WA - [k0 Q + ab + 3ae + 2b(c+e) + c(k0+1) + (d+1)s3] with q2=u3=k=t3=i=v2=v3=w=z=0, using
# s3+s4<=ab, h<=ac, t4<=B, i.e. after substituting s4=ab-s3, h=ac, t4=B (worst case) the difference must be 0.
k0 = b+c+e
sub = lambda p, m: p
Wef = (d+1)*(3*a+2*b+c+q3+s3) - 4*(q3+u4+s3+(a*b-s3)+a*c+B)
WAef = (a+1)*(3*a+q3) - 4*(q3+u4)
print("EF expansion check: has", len((Wef - WAef - (k0*q3 + a*b + 3*a*e + 2*b*(c+e) + c*(k0+1) + (d+1)*s3)).t), "nonzero terms (q3 plays Q)")
