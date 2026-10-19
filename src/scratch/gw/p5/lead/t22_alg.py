import sympy as sp
a,j,s,n,l=sp.symbols('a j s n l')
C2=lambda x: x*(x-1)/2
# MG2: q = C(j+1,2)+s, q^{<2>} = C(j+2,3)+C(s+1,2) ; f_j(s) = (a+2)q - 3 q^{<2>}
q=C2(j+1)+s; q2=sp.binomial(j+2,3)+C2(s+1)
f=sp.expand(sp.expand_func((a+2)*q-3*q2))
fj=sp.expand((a-j)*C2(j+1)+(a+2)*s-3*s*(s+1)/2)
print("f_j(s) formula matches:", sp.simplify(f-fj)==0)
print("f_j(j)-(2a-2) factor:", sp.factor(fj.subs(s,j)-(2*a-2)), " claimed:", sp.factor((j-1)*(a-1-j)*(j+4)/2))
print("f_j(0) at j=2:", sp.expand(fj.subs({s:0,j:2})), " >= 2a-2 ?  diff:", sp.expand(fj.subs({s:0,j:2})-(2*a-2)))
print("f_j(0) general:", sp.factor(fj.subs(s,0)))
# numeric exhaustive check of MG2 with true Macaulay pseudo-power for a in 4..60
def mac2(q):
    # q^{<2>}: write q = C(j+1,2)+C(s,1)? standard 2-binomial rep q = C(k2,2)+C(k1,1), k2>k1>=0 ; q^<2> = C(k2+1,3)+C(k1+1,2)
    k2=1
    while sp.binomial(k2+1,2)<=q: k2+=1
    r=q-sp.binomial(k2,2)
    return sp.binomial(k2+1,3)+sp.binomial(r+1,2)
bad=0
for A in range(4,61):
    Q=A*(A+1)//2
    for qq in range(2,Q):
        if (A+2)*qq-3*mac2(qq) < 2*A-2: bad+=1; print("MG2 fail",A,qq)
print("MG2 exhaustive a<=60 fails:",bad)
# ALT2 polynomial identities
x=sp.Rational(2,3)*(a-1)
print("ALT2 l=0:", sp.expand(x*(x-1)-(2*a-3)), "vs", sp.expand((4*a**2-32*a+37)/9), sp.expand((4*(a-7)**2+24*(a-7)+9)/9))
print("ALT2 l=1:", sp.expand((5*a-9)*(5*a-15)-36*(5*a-8)), "vs", sp.expand(25*(a-11)**2+250*(a-11)+148))
