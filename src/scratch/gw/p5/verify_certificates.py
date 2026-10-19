"""Exact arithmetic checks of the analytic P5 certificates. fejer only."""
from fractions import Fraction as F
from math import comb
from certificate import P, poly, a, b

def constants(a,b,lam):
    Q=F(a*(a+1),2); B=F(b*(b+1),2)
    k=F(3*b-a-17+lam*(a-1),3)
    j=a+b+1+2*lam; ell=a+b+2+lam
    mu=F(max(k,0))/b; nu=(3-mu)/2
    eta=(j-nu*(a+1))/(b+1); chi=3-2*eta
    C=3*a*(a+1)+a*b+lam*(a-b-1-a*b-B)+min(k,0)*Q
    K=ell-a*chi
    assert min(mu,nu,eta,chi)>=0,(a,b,lam,mu,nu,eta,chi)
    assert mu+2*nu==chi+2*eta==3
    assert mu*b==max(k,0)
    assert nu*(a+1)+eta*(b+1)==j
    return C,K

def check(a,b):
    B=F(b*(b+1),2);Z=F(b*(b+1)*(b+2),6)
    Ca=F(a*(a+1)*(a-1),6);w=(a-1)*(b+1)
    C0,K0=constants(a,b,0);C1,K1=constants(a,b,1)
    assert C0+K0*B-3*Z==-Ca,(a,b,C0,K0,Ca)
    assert C1+K1*B-3*Z==w,(a,b,C1,K1,w)
    D=2*B*B/(2*b+1)
    margin=D*(C0-w)-(w-C1)*(C0+Ca)
    assert C0>=w and margin>=0,(a,b,margin)
    return C0,C1,margin

if __name__=='__main__':
    count=0
    for ai in range(2,251):
        for bi in range(ai+2,1001):check(ai,bi);count+=1
    for ai,bi in [(2,2),(2,3)]:check(ai,bi);count+=1
    print('Exact endpoint, sign, and curvature checks:',count,flush=True)
    exceptional=[(2,2),(2,3),(2,4),(2,5),(2,6),(3,5),(3,6),(4,6),(5,7)]
    for ai,bi in exceptional:print('exception',ai,bi,*map(str,check(ai,bi)),flush=True)
    # Symbolic identity for the infinite region. Shift a=1+x,b=a+2+y.
    shifted=(2*poly).subst(a+1,a+b+3)
    expected={
      0:[5508,13974,16650,10407,3342,495,24],
      1:[5634,9606,8497,4079,920,70],
      2:[3150,3856,2431,797,98],
      3:[936,854,390,70],4:[126,66,18],5:[6]}
    assert shifted.d=={(i,j):F(v) for j,vs in expected.items() for i,v in enumerate(vs)}
    print('Positive-coefficient identity verified exactly:',len(shifted.d),'monomials',flush=True)
    nlinear=0
    for ai in range(2,501):
        for bi in range(0,ai+2):
            if ai==2 and bi>1:continue
            Q=F(ai*(ai+1),2);B=F(bi*(bi+1),2)
            mu=F(ai*ai-ai-bi-1,ai*(ai+1));nu=(3-mu)/2
            mup=F(ai+1,ai);nup=F(2*ai-1,2*ai)
            kap=F(bi*(2*ai+bi+1),ai*(ai+1))-6
            assert min(mu,nu,mup,nup,-kap)>=0
            assert nu*(ai+1)+nup*(bi+1)==ai+bi+3
            assert mup*ai+bi+2==ai+bi+3
            assert mu+2*nu==mup+2*nup==3
            C1=3*ai*ai+4*ai-1-F(bi*bi+3*bi,2)
            assert C1+kap*Q==(ai-1)*(bi+1)
            nlinear+=1
    print('Linear certificate exact checks:',nlinear,flush=True)
