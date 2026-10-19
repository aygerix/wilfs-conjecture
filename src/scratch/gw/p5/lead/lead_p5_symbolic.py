# Lead's independent symbolic verification of P5_REPORT (codex P5), written from the report's statements.
import sympy as sp
a,b,c,e,lam,rho=sp.symbols('a b c e lam rho')
q,u,s,S,H,t,T,I,v,w,z=sp.symbols('q u s S H t T I v w z')
d=a+b+c+e; r=c+e; Q=a*(a+1)/2; B=b*(b+1)/2; Z=b*(b+1)*(b+2)/6; A0=a*(a+1)*(a-1)/6
N=q+u+s+S+H+t+T+I+v+w+z
ell4=3*a+2*b+c+q+s+t            # ell-4 with q2=u3=k=0 (GW-21: ell=4+3a+2b+c+2q2+q3+s3+t3+u3)
W=(d+1)*ell4-4*N+rho             # GW-21 identity (1)
SR=rho-t-I-v-w-z
ARC=rho-(a-b-c-e-1-q+u+s-S+H+t-T+I+v+w+z)
# check ARC slack derivation from h <= 2(q+b+c+e+S+T)+2, h=m-rho, m=1+d+N
m=1+d+N
assert sp.expand((rho-(m-2*(q+b+c+e+S+T)-2))-ARC)==0
C=3*a*(a+1)+a*b+lam*(a-b-1-a*b-B)
k=b-(a+17)/sp.Integer(3)+lam*(a-1)/3
j=a+b+1+2*lam
l=a+b+2+lam
G=c*(1+r+lam*(a-1))+e*(3*a+2*b-lam)+r*(q+s+t)
RHS=(C+k*q+j*s+l*t-3*(v+w+z)+G+(4-lam)/3*((a+2)*q-3*u)+(4+lam)*(a*b-s-S+B-t-T)
     +(4-lam)*(a*c-H)+3*(b*c-I)+(1-lam)*SR+lam*ARC)
print("ID exact:", sp.expand(W-RHS)==0)
Gmin=c*(c+e+1)+e*(3*a+2*b-1)+r*(q+s+t)
print("G_lam - G =", sp.factor(sp.expand(G-Gmin)))
# LIN (Region I, lam=1)
mu=(a**2-a-b-1)/(a*(a+1)); nu=(3-mu)/2; mup=(a+1)/a; nup=(2*a-1)/(2*a); kap=b*(2*a+b+1)/(a*(a+1))-6
C1=C.subs(lam,1); k1=k.subs(lam,1); j1=j.subs(lam,1); l1=l.subs(lam,1)
print("LIN:", [sp.simplify(x)==0 for x in [mu+2*nu-3, mup+2*nup-3, nu*(a+1)+nup*(b+1)-j1, mup*a+(b+2)-l1, k1-mu*b-kap, C1+kap*Q-(a-1)*(b+1)]])
# full first-line expansion in Region I equals the claimed nonneg combination
first=C1+k1*q+j1*s+l1*t-3*(v+w+z)
cert=(a-1)*(b+1)+(-kap)*(Q-q)+mu*(b*q-v)+nu*((a+1)*s-2*v)+mup*(a*t-w)+nup*((b+1)*s-2*w)+((b+2)*t-3*z)
print("Region I first line = certificate:", sp.simplify(first-cert)==0)
# Region II endpoints, both signs of k
w0=(a-1)*(b+1)
def endpoint(lv,ksign):
    kl=k.subs(lam,lv); Cl=C.subs(lam,lv); jl=j.subs(lam,lv); ll=l.subs(lam,lv)
    if ksign>=0: al=0; mul=kl/b
    else: al=-kl; mul=sp.Integer(0)
    nul=(3-mul)/2; eta=(jl-nul*(a+1))/(b+1); chi=3-2*eta
    Cp=Cl-al*Q; Kl=ll-a*chi
    ids=[sp.simplify(kl-(mul*b-al)), sp.simplify(mul+2*nul-3), sp.simplify(chi+2*eta-3), sp.simplify(nul*(a+1)+eta*(b+1)-jl)]
    ep=sp.simplify(Cp+Kl*B-3*Z-(-A0 if lv==0 else w0))
    return ids,ep,Cp
for lv in (0,1):
  for ks in (1,-1):
    ids,ep,Cp=endpoint(lv,ks); print("END lam=%d ksign=%+d: ids zero:"%(lv,ks),all(x==0 for x in ids)," EP residual:",ep)
# MC
tt=sp.symbols('tt',positive=True); bb=sp.symbols('bb',positive=True)
Bb=bb*(bb+1)/2; Zb=bb*(bb+1)*(bb+2)/6; F=tt*(sp.sqrt(8*tt+1)+3)/6
lhs=3*(Zb*tt/Bb-F); rhs=4*tt*(Bb-tt)/(2*bb+1+sp.sqrt(8*tt+1))
print("MC identity:", sp.simplify(sp.radsimp(lhs-rhs))==0 or sp.simplify(lhs-rhs)==0)
x=sp.symbols('x'); print("condensed Macaulay F at t=C(x+1,2):", sp.simplify(F.subs(tt,x*(x+1)/2)-sp.binomial(x+2,3).expand(func=True)) )
# POLY: P(a,b)=12{2B^2(C0-w0)-(2b+1)H0(C0+A0)} with C0=3a(a+1)+ab, H0=B+ab-3a(a+1)
C0=3*a*(a+1)+a*b; H0=B+a*b-3*a*(a+1)
P=sp.expand(12*(2*B**2*(C0-w0)-(2*b+1)*H0*(C0+A0)))
X,Y=sp.symbols('X Y'); PXY=sp.expand(P.subs({a:X+1,b:Y+X+3}))
poly=sp.Poly(PXY,X,Y); coeffs=poly.coeffs()
print("POLY: #monomials",len(coeffs)," min coeff",min(coeffs)," all positive:",all(cf>0 for cf in coeffs))
print("C0-w0 =",sp.expand(C0-w0), " C1(lam=1,k>=0) =",sp.expand(C.subs(lam,1)))
# check: when k0,k1 >= 0 the primed constants are C0 (lam=0) and C.subs(lam,1) (lam=1)

# 9-point table and sign checks, exact
from fractions import Fraction as Fr
def vals(A,Bv,lv):
    A=Fr(A);Bv=Fr(Bv)
    kl=Bv-(A+17)/3+lv*(A-1)/3; Cl=3*A*(A+1)+A*Bv+lv*(A-Bv-1-A*Bv-Bv*(Bv+1)/2)
    jl=A+Bv+1+2*lv; ll=A+Bv+2+lv
    al=max(-kl,Fr(0)); mul=max(kl,Fr(0))/Bv; nul=(3-mul)/2; eta=(jl-nul*(A+1))/(Bv+1); chi=3-2*eta
    Q=A*(A+1)/2; return dict(Cp=Cl-al*Q,mu=mul,nu=nul,eta=eta,chi=chi,al=al)
pts=[(2,2),(2,3),(2,4),(2,5),(2,6),(3,5),(3,6),(4,6),(5,7)]
for (A,Bv) in pts:
    v0=vals(A,Bv,0); v1=vals(A,Bv,1)
    w0=Fr((A-1)*(Bv+1)); A0=Fr(A*(A+1)*(A-1),6); Bb=Fr(Bv*(Bv+1),2); D0=2*Bb*Bb/(2*Bv+1)
    margin=D0*(v0['Cp']-w0)-(w0-v1['Cp'])*(v0['Cp']+A0)
    signs=all(x>=0 for vv in (v0,v1) for x in (vv['mu'],vv['nu'],vv['eta'],vv['chi'],vv['al']))
    print((A,Bv),"C'0=",v0['Cp'],"C'1=",v1['Cp'],"S margin=",margin,"C'0>w0:",v0['Cp']>w0,"signs ok:",signs)
# exhaustive sign + S check on a big grid of Region II (independent of codex's verifier)
bad=0;cnt=0
for A in range(2,121):
    for Bv in list(range(A+2,600))+([2,3] if A==2 else []):
        cnt+=1
        v0=vals(A,Bv,0); v1=vals(A,Bv,1)
        w0=Fr((A-1)*(Bv+1)); A0=Fr(A*(A+1)*(A-1),6); Bb=Fr(Bv*(Bv+1),2); D0=2*Bb*Bb/(2*Bv+1)
        ok=v0['Cp']>w0 and D0*(v0['Cp']-w0)>=(w0-v1['Cp'])*(v0['Cp']+A0) and all(x>=0 for vv in (v0,v1) for x in (vv['mu'],vv['nu'],vv['eta'],vv['chi'],vv['al']))
        if not ok: bad+=1
print("Region II grid pairs:",cnt,"failures:",bad)
