"""Lead's symbolic checks of P5_REPORT sections 34-36 (uniform alpha). Run on fejer."""
from sympy import symbols, Rational as Q, expand, simplify
a, al, b, x, z = symbols('a alpha b x z')
Q0 = al*(al+1)/2; U0 = al*(al+1)*(al+2)/6
# U-POLY identity
nu = a/2 + Q(2,3)*al + Q(3,4) + Q(3,10)*b
f = lambda n: n**3 - n**2 + 2*n - Q(3,4)*n*Q0
B0 = (a-2*al-1)*Q0 + 2*U0 + 2*al - a + 1
lhs = f(nu) - 9*B0 - Q(18,5)*b*Q0 + 10
rhs = (Q(9,8)*al)*(x - Q(7,12)*al - Q(1,4))**2 + (119*z**3+1086*z**2+2559*z+2126)/128 \
      + Q(355,32)*x + Q(11,16)*x**2 + x**3/8 \
      + b*(Q(201,160)+Q(33,40)*x+Q(9,40)*x**2+Q(9,16)*al+Q(27,20)*al*x+Q(9,80)*al**2) \
      + b**2*(Q(99,400)+Q(27,200)*x+Q(81,200)*al) + Q(27,1000)*b**3
sub = {a: x + Q(5,3)*al + 1}
d = expand(lhs.subs(sub) - rhs.subs(z, al-4))
print("U-POLY identity:", d == 0, "" if d == 0 else d)
# A-LOW: a(a-1) at 5al/3+1 minus 3al(al+1)
print("A-LOW difference:", expand((Q(5,3)*al+1)*(Q(5,3)*al) - 3*al*(al+1)))
# f'(n) at n>=alpha lower bound
n = symbols('n'); fp = expand((n**3 - n**2 + 2*n - Q(3,4)*n*Q0).diff(n))
print("f'(alpha) =", expand(fp.subs(n, al)), " claimed (21al^2-19al+16)/8:", expand(fp.subs(n, al) - (21*al**2-19*al+16)/8) == 0)
# MID-B0 / LOW-H algebra: 3*delta lower minus 3*(upper) with c0,u0,k0 symbolic
c0, u0, k0, D3 = symbols('c0 u0 k0 D3')
B1 = (a-2*al-1)*Q0 + 2*c0 + 2*al - a + 1 - (a+1)*u0 + 5*k0
low = a-1 + (a+1)*(Q0+u0) - 3*k0 + D3 + 2*Q0 + 1
# delta <= B1 - D3 - 1  =>  3delta <= 3B1 - 3D3 - 3 ; difference low - (3B1-3D3-3)
diff = expand(low - (3*B1 - 3*D3 - 3))
claimed = 4*a - 6*al + (6*al+6-2*a)*Q0 - 6*c0 + 4*(a+1)*u0 - 18*k0 + 4*D3
print("LOW-H identity:", expand(diff - claimed) == 0, expand(diff-claimed))
lowH = expand(claimed.subs(c0, U0) - 4*(a+1)*u0 + 18*k0)   # with c0<=U0 and the u0,k0 terms dropped as claimed
print("LOW-H after c0<=U0:", expand(lowH - (4*a - 6*al + 2*(2*al+1-a)*Q0 + 4*D3)) == 0)
# MID-B0 upper bound: LOW-H <= 0 with D3=3eps
eps = symbols('eps')
bound = expand((-(4*a - 6*al + 2*(2*al+1-a)*Q0))/12)
print("eps upper from LOW-H<=0:", bound, " claimed:", expand(((a-2*al-1)*Q0 - 2*a + 3*al)/6), expand(bound - ((a-2*al-1)*Q0 - 2*a + 3*al)/6) == 0)
