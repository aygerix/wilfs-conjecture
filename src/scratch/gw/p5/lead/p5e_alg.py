"""Lead's symbolic check of P5_REPORT sections 45-46 (P47-B0 identity and certificates, the B-free analytic end,
LARGE-A constants), written from the report text.  Run with sympy on fejer."""
from sympy import symbols, Rational as Q, expand, simplify, binomial, sqrt, nsolve, Symbol
A, a, eps, R = symbols('A a eps R', positive=True)
ok = True
def chk(name, e):
    global ok
    e = simplify(expand(e))
    print(f"{name}: {'OK' if e == 0 else 'FAIL '+str(e)}")
    ok = ok and e == 0

Q0 = A*(A+1)/2; U0 = A*(A+1)*(A+2)/6
# P47-B0: nu, B0, F
y = eps/Q0
x = a-2*A-1-6*eps/Q0
nu = a/2+Q(2,3)*A+Q(5,6)+Q(3,2)*y
B0 = (a-2*A-1)*Q0+2*U0+2*A-a+1
F = nu**3-nu**2+2*nu-9*B0-67*eps+10
T = 9*y/(2*A); V = x/(2*A); w = T+V
g = w**3+5*w**2-Q(46,9)*w+Q(44,27)
j = 3*w**2-Q(31,9)*w-Q(2,3)
ID = A**2*((A-4)*g+4*g+j)+Q(40,9)*(A**3+A**2)*V+A*(Q(16,9)+Q(50,3)*T+Q(68,3)*V)+Q(358,27)
chk("P47-ID", F-ID)
W = Symbol('w')
gW = W**3+5*W**2-Q(46,9)*W+Q(44,27); jW = 3*W**2-Q(31,9)*W-Q(2,3)
chk("g certificate", gW-(W**3+5*(W-Q(23,45))**2+Q(131,405)))
chk("4g+j certificate", 4*gW+jW-(4*W*(W-Q(1,2))**2+27*(W-Q(112,243))**2+Q(254,2187)))
# check that nu as defined is the R-LOW bound: n >= a/2+2A/3+5/6+(a-2A)/(2Q0)+3y/2 from COLD-FIX with D3=3eps, n0=Q0, S=0, b=0
# fixed payment: D3 + a-1-2A-2U0+(a+3)Q0-2Q0 R <= -1  ->  R >= [3eps + a - 2A - 2U0 + (a+3)Q0]/(2Q0)
Rlow = (3*eps+a-2*A-2*U0+(a+3)*Q0)/(2*Q0)
chk("R-LOW n bound", (A+Rlow)-(a/2+Q(2,3)*A+Q(5,6)+(a-2*A)/(2*Q0)+Q(3,2)*y))
# DELTA-UP with E=l=0,b=0, c0<=U0: delta <= 2C_H-(a-1)-(a+3)Q0-D3-1 with C_H = A+Q0+U0+Q0(a-A)
CH = A+Q0+U0+Q0*(a-A)
chk("B0 from DELTA-UP", (2*CH-(a-1)-(a+3)*Q0-1)-(B0-1))
# C_dagger optimization: polynomial for general C
Cs = Symbol('C')
L = (2*Cs-48)/9
gC = w**3+5*w**2-L*w+Q(44,27); jC = 3*w**2-(L-Q(5,3))*w-Q(2,3)
FC = nu**3-nu**2+2*nu-9*B0-(Cs+20)*eps+10    # P(C): 2H(n)-C*eps*2... check the stated generalization below
# The report says: identity has coefficient (2C-54)/9 on (A^3+A^2)V.  Verify with eps coefficient = C+20? derive:
# P(C) gives 2(3s-2) >= 2H(n)-2C eps; with 2(3s-2) <= 9 delta - 1 and delta <= B0-3eps-1: 9B0-27eps-10 >= n^3-n^2+2n-2C eps
# i.e. F_C = nu^3-nu^2+2nu-9B0+27eps-2C eps+10 < 0 required.  At C=47: 27-94 = -67. matches.
FC = nu**3-nu**2+2*nu-9*B0+(27-2*Cs)*eps+10
IDC = A**2*((A-4)*gC+4*gC+jC)+(2*Cs-54)/9*(A**3+A**2)*V+A*(Q(16,9)+Q(50,3)*T+Q(68,3)*V)+Q(358,27)
chk("P(C) general identity", FC-IDC)
# C_dagger: 4g+j >= 0 for w>0 iff C <= 51/2+(18/5)w^2+(207/10)w+79/(15w)  (solve 4g+j=0 for C)
LW = (2*Cs-48)/9
fourgj = expand(4*(W**3+5*W**2-LW*W+Q(44,27))+(3*W**2-(LW-Q(5,3))*W-Q(2,3)))
Csol = (fourgj.coeff(Cs, 0)) / (-fourgj.coeff(Cs, 1))   # fourgj = c0 + c1*C  -> C = -c0/c1 (c1<0 for w>0)
chk("C_dagger expression", Csol-(Q(51,2)+Q(18,5)*W**2+Q(207,10)*W+Q(79,15)/W))
print("  coefficient of C in 4g+j:", fourgj.coeff(Cs, 1), "(negative for w>0, so 4g+j>=0 iff C<=expression)")
wd = nsolve(216*W**3+621*W**2-158, W, 0.4)
Cd = Q(51,2)+Q(18,5)*wd**2+Q(207,10)*wd+Q(79,15)/wd
print("C_dagger numeric =", Cd, " (claimed in (47,48))", "OK" if 47 < Cd < 48 else "FAIL")
# B-free analytic end: bracket identity a^2/8 - a(Q0/4+1/4) - 9Q0 + 1 = 172 + [a-(2Q0+38)](a/8+9/2)
chk("B0-strip analytic end bracket", (a**2/8-a*(Q0/4+Q(1,4))-9*Q0+1)-(172+(a-(2*Q0+38))*(a/8+Q(9,2))))
# LARGE-A constants
print("3135/8192 > 1/3:", Q(3135,8192) > Q(1,3), "; (17/16)^3/6 = 4913/24576 < 1/5:", Q(4913,24576) < Q(1,5),
      "; 17/512 < 1/30:", Q(17,512) < Q(1,30), "; 13/72 a^2 < a^3/60 for a>=11:", Q(13,72)*11 < Q(1,60)*11**2)
print("(15/16)(209/256)/2 =", Q(15,16)*Q(209,256)/2, "== 3135/8192:", Q(15,16)*Q(209,256)/2 == Q(3135,8192))
print("ALL", "OK" if ok else "FAIL")
