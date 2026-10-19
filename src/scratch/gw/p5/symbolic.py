"""Rational-function verification over Q(a,b), no sympy. fejer only."""
from certificate import P,a,b
from fractions import Fraction as F

class R:
    def __init__(self,n=0,d=1):
        if isinstance(n,R):self.n,self.d=n.n,n.d
        else:self.n,self.d=P(n),P(d)
    def __add__(s,o):
        o=R(o);return R(s.n*o.d+o.n*s.d,s.d*o.d)
    __radd__=__add__
    def __neg__(s):return R(-s.n,s.d)
    def __sub__(s,o):return s+-R(o)
    def __rsub__(s,o):return R(o)+-s
    def __mul__(s,o):
        o=R(o);return R(s.n*o.n,s.d*o.d)
    __rmul__=__mul__
    def __truediv__(s,o):
        o=R(o);return R(s.n*o.d,s.d*o.n)
    def __eq__(s,o):
        o=R(o);return not (s.n*o.d-o.n*s.d).d

if __name__=='__main__':
    a,b=R(a),R(b)
    Q=a*(a+1)/2;B=b*(b+1)/2;Z=b*(b+1)*(b+2)/6
    Ca=a*(a+1)*(a-1)/6;w0=(a-1)*(b+1)
    for lam in [0,1]:
        k=b-(a+17)/3+lam*(a-1)/3
        j=a+b+1+2*lam;ell=a+b+2+lam
        C=3*a*(a+1)+a*b+lam*(a-b-1-a*b-B)
        for negative in [False,True]:
            mu=R(0) if negative else k/b
            nu=(3-mu)/2;eta=(j-nu*(a+1))/(b+1);chi=3-2*eta
            Cp=C+k*Q if negative else C
            K=ell-a*chi
            assert mu+2*nu==3 and chi+2*eta==3
            assert nu*(a+1)+eta*(b+1)==j
            assert Cp+K*B-3*Z==(-Ca if lam==0 else w0)
        # Corrected LOW-ID, after paying v2 and the total q capacity.
        lowq=2*(a+b)-2+lam-(4-lam)*(a+2)/3-(1-lam)*b-k
        assert lowq==a+1+lam*(b+2)
    mu=(a*a-a-b-1)/(a*(a+1));nu=(3-mu)/2
    mup=(a+1)/a;nup=(2*a-1)/(2*a)
    kap=b*(2*a+b+1)/(a*(a+1))-6
    C1=3*a*a+4*a-1-(b*b+3*b)/2
    assert mu+2*nu==3 and mup+2*nup==3
    assert nu*(a+1)+nup*(b+1)==a+b+3
    assert mup*a+b+2==a+b+3
    assert b-6-mu*b==kap
    assert C1+kap*Q==w0
    print('All endpoint branches, LIN identities, and LOW-ID verified in Q(a,b).')
