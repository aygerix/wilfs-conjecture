import sympy as sp
a,b,c,e,lam,rho,dl=sp.symbols('a b c e lam rho delta')
q2,q3,u3,u4,k,v2,v3,s,S,H,t,T,I,w,z=sp.symbols('q2 q3 u3 u4 k v2 v3 s S H t T I w z')
d=a+b+c+e; r=c+e; Q=a*(a+1)/2; B=b*(b+1)/2
N=q2+q3+s+S+H+t+T+I+u3+u4+v2+v3+w+z+k
ell4=3*a+2*b+c+2*q2+q3+s+t+u3
W=(d+1)*ell4-4*N+rho
SR=rho-t-I-v3-w-z
ARCrhs=a-b-c-e-1-q3+u4+s-S+H+t-T+I+v3+w+z
ARC=rho-(ARCrhs+q2+u3+k+v2-3*dl)
C=3*a*(a+1)+a*b+lam*(a-b-1-a*b-B); kk=b-(a+17)/sp.Integer(3)+lam*(a-1)/3; j=a+b+1+2*lam; l=a+b+2+lam
G=c*(1+r+lam*(a-1))+e*(3*a+2*b-lam)+r*(q3+s+t)
rest=(C+kk*q3+j*s+l*t-3*(v3+w+z)+G+(4-lam)/3*((a+2)*(q2+q3)-3*(u3+u4))+(4+lam)*(a*b-s-S+B-t-T)
      +(4-lam)*(a*c-H)+3*(b*c-I)+(1-lam)*SR+lam*ARC)
low=sp.expand(W-rest)
claim=sp.expand((2*(a+b)-2+lam-(4-lam)*(a+2)/3)*q2+(a+b+1)*u3-(4-lam)*(k+v2)-3*lam*dl+(c+e)*(2*q2+u3))
print("low terms match claim:", sp.simplify(low-claim)==0)
# endpoint modification (Region II): replace alpha*(Q-q3) by alpha*(Q-q2-q3), nu*((a+1)s-2v3) by nu*((a+1)s-2v2-2v3),
# then pay remaining v2 coefficient with v2<=b q2. Compute the leftover low part and compare with LOW-ID.
for ks in (+1,-1):
    al,mu=( (0,kk/b) if ks>0 else (-kk,sp.Integer(0)) )
    nu=(3-mu)/2
    # extra terms created by using the larger slacks: -alpha*q2 (from Q-q2-q3 vs Q-q3), +2nu v2 (from the v2 in 2(v2+v3) slack)
    extra=-al*q2+2*nu*v2
    leftover=sp.expand(claim+extra)  # remainder gains alpha*q2 + 2nu*v2 when the larger slacks are used
    v2coef=sp.simplify(sp.diff(leftover,v2))
    # pay v2 with v2<=b q2: leftover + (-v2coef)... coefficient of v2 is v2coef (<=0 claimed); add v2coef*(v2 - b q2)?? i.e. leftover - v2coef*v2 + v2coef*b*q2 >= leftover when v2coef<=0
    fin=sp.expand(leftover - v2coef*v2 + v2coef*b*q2)
    target=sp.expand((a+1)*q2+(a+b+1)*u3-4*k+lam*((b+2)*q2+k-3*dl)+(c+e)*(2*q2+u3))
    print("ksign",ks,"v2 coef:",sp.simplify(v2coef)," LOW-ID matches:",sp.simplify(fin-target)==0)
al=-kk; mu=sp.Integer(0); nu=(3-mu)/2
extra=al*q2+2*nu*v2
leftover=sp.expand(claim+extra); v2coef=sp.diff(leftover,v2)
fin=sp.expand(leftover - v2coef*v2 + v2coef*b*q2)
target=sp.expand((a+1)*q2+(a+b+1)*u3-4*k+lam*((b+2)*q2+k-3*dl)+(c+e)*(2*q2+u3))
print("k<0 branch: fin-target =",sp.factor(sp.simplify(fin-target)))
