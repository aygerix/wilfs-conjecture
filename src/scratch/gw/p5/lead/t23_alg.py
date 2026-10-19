"""Lead's symbolic/exhaustive checks of the algebra in P5_REPORT sections 24-26 (three low directions).
Run on fejer with ~/mathenv/bin/python."""
from sympy import symbols, binomial, expand, Poly, simplify, Rational
from math import comb

a, t = symbols('a t')

def mac2(q):  # Macaulay pseudo-power q^{<2>}
    j = 1
    while comb(j+2, 2) <= q: j += 1
    s = q-comb(j+1, 2)
    return comb(j+2, 3)+comb(s+1, 2)

ok = True
# MG6 exhaustively, 13<=a<=400
for A in range(13, 401):
    Q = comb(A+1, 2)
    for q in range(6, Q-3+1):
        if (A+2)*q-3*mac2(q) < 6*A-18:
            print("MG6 FAIL", A, q); ok = False
print("MG6 exhaustive 13<=a<=400:", ok)
# MG6 endpoint identities
j, s = symbols('j s')
f = (a-j)*j*(j+1)/2+(a+2)*s-3*s*(s+1)/2
assert expand(f.subs({j: 3, s: 3})-(9*a-30)) == 0
assert expand(f.subs({j: a-2, s: a-2})-(a**2+3*a-10)/2) == 0
assert expand(f.subs({j: a-1, s: a-3})-(6*a-15)) == 0
assert expand(f.subs({j: a-1, s: 0})-(6*a-18)-(a-4)*(a-9)/2) == 0
assert expand(f.subs({j: 3, s: 0})-(6*a-18)) == 0
dfj = expand(f.subs(s, j).diff(j)*2)
print("d/dj f_j(j) *2 =", dfj)
# NEAR-GAP: q=Q-r, r=1,2
for r in (1, 2):
    for A in range(4, 401):
        Q = comb(A+1, 2); q = Q-r
        if (A+2)*q-3*mac2(q) != r*(4*A-3*r-1)//2:
            print("NEAR-GAP mismatch", r, A, (A+2)*q-3*mac2(q)); ok = False
print("NEAR-GAP exact for 4<=a<=400:", ok)
# 3L-HIGHARC constant B_{r,l}
l, r = symbols('l r')
e0 = l+r
C3 = lambda x: x*(x-1)*(x-2)/6
Bclaim = (5+5*l+7*r)*a-15-17*l-13*r+2*C3(l+r+2)
Bderiv = -(a-39+(a+3)*(6-r+l)-2*l-2*e0-2*C3(e0+2)-(12+6*e0)*(a-3))
print("B_{r,l} identity:", expand(Bclaim-Bderiv) == 0)
# 3L-FIX: A_{r,l}
Aclaim = (7+l-2*r)*a-9+2*l-l**2-5*r
Aderiv = a-27+(a+3)*(6-r)+l*(a+2-l)-(a+2)*r   # with R term removed (-2 n0 R <= -12R)
print("A_{r,l} identity:", expand(Aclaim-Aderiv) == 0)
# 3L-SHARP: Ahat for r>=1 : a-39+(a+3)(6-r)+l(a+2-l)+D_r
Dr = r*(4*a-3*r-1)/2
Ahat = (7+r+l)*a-21+2*l-l**2-r*(3*r+7)/2
print("Ahat identity:", expand(Ahat-(a-39+(a+3)*(6-r)+l*(a+2-l)+Dr)) == 0)
# table
TAB = {(0, 0): 16, (0, 1): 26, (0, 2): 33, (0, 3): 37, (0, 4): 41, (0, 5): 43,
       (1, 0): 32, (1, 1): 37, (1, 2): 40, (1, 3): 43, (1, 4): 45, (1, 5): 47,
       (2, 0): 39, (2, 1): 42, (2, 2): 44, (2, 3): 46, (2, 4): 47, (2, 5): 49}
COEF = {(0,0):(49,638,157),(0,1):(64,1472,112),(0,2):(81,2484,1296),(0,3):(100,3440,28),(0,4):(121,4760,3100),(0,5):(144,5904,144),
        (1,0):(64,1952,1852),(1,1):(81,2844,1936),(1,2):(100,3760,316),(1,3):(121,4980,2160),(1,4):(144,6240,2188),(1,5):(169,7752,4572),
        (2,0):(81,3006,253),(2,1):(100,4020,909),(2,2):(121,5112,828),(2,3):(144,6456,3421),(2,4):(169,7726,1141),(2,5):(196,9556,8293)}
for (R_, L_), A0 in TAB.items():
    sub = {r: R_, l: L_}
    if R_ == 0:
        Ah = Aclaim.subs(sub)
    else:
        Ah = Ahat.subs(sub)
    Cf = expand(Ah-12*(L_+R_))
    Bh = expand(Bclaim.subs(sub)-(Dr.subs(sub) if R_ > 0 else 0))
    G = expand(Cf*(Cf-12)-144*(Bh-1+2*R_*(R_+1)))
    P = Poly(expand(G.subs(a, A0+t)), t)
    co = tuple(int(c) for c in P.all_coeffs())
    good = co == COEF[(R_, L_)] and all(c >= 0 for c in co) and Cf.subs(a, A0) > 12 and (A0-13-3*L_-2*R_) >= 0
    # minimality of the table entry: G(A0-1)<0 or C(A0-1)<=12 or b-coefficient negative
    Gm = G.subs(a, A0-1); Cm = Cf.subs(a, A0-1)
    minimal = (Gm < 0) or (Cm <= 12) or (A0-1-13-3*L_-2*R_ < 0)
    print((R_, L_), "A=", A0, "coeffs", co, "match" if co == COEF[(R_, L_)] else "MISMATCH", "ok" if good else "BAD",
          "C(A)=", Cf.subs(a, A0), "entry minimal" if minimal else "entry not minimal")
    ok = ok and good
# 3L-GAP-STARS constants
for R_, s0 in ((0, 5), (1, 3), (2, 1)):
    val = expand(-(5*a-15)+s0*(a+2-s0)+(Dr.subs(r, R_) if R_ > 0 else 0))
    print("GAP-STARS r=%d s0=%d: P+D3 >=" % (R_, s0), val)
# c=e=0 reduction: Q-2-(5a-15)
print("Q-2-(5a-15) =", expand(a*(a+1)/2-2-(5*a-15)), " = (a^2-9a+26)/2, discriminant", 81-104)
print("ALL OK" if ok else "SOME CHECK FAILED")
