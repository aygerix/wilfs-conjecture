"""Lead check of P9 §6-§7 algebra: ET-31/ET-2 identities, the T_2/a table (XQ endpoints), ET-SIDON for small primes."""
import sympy as sp
p, u, A, x, z = sp.symbols('p u A x z')
s = p*(p+1)/2; beta = 2*p*(p-1)+1; T2 = p*(s-1)
print('ET31 identity:', sp.expand(27*T2-128*beta - sp.Rational(1,2)*(27*p**3-485*p**2+458*p-256)) == 0)
print('ET17 shift:', sp.expand((27*p**3-485*p**2+458*p-256).subs(p,17+u)))
print('ET2 identity:', sp.expand(2*(p*s-12*beta) - (p**3-47*p**2+48*p-24)) == 0)
print('ET47 shift:', sp.expand((p**3-47*p**2+48*p-24).subs(p,47+u)))
for r in (5,6,8):
    poly = sp.expand(2*(T2-r*beta)); ok = sp.expand(poly-(p**3-(4*r-1)*p**2+(4*r-2)*p-2*r))==0
    print('r',r,'identity',ok,'shift coeffs', sp.Poly(sp.expand(poly.subs(p,4*r-1+u)),u).all_coeffs())
XQ = (A-1)*x**2-(3*A+2)*x-(2*A+1)
for Av, xv in ((8,9),(6,14),(5,24)):
    print('XQ A=%s x=%s:'%(Av,xv), XQ.subs({A:Av,x:xv}), 'deriv', sp.diff(XQ,x).subs({A:Av,x:xv}))
print('XQ A=128/27, x=31+z:', sp.factor(sp.expand(XQ.subs({A:sp.Rational(128,27), x:31+z}))))
# ET-SIDON numerically
def sidon_ok(P):
    B=[2*P*i+(i*i%P) for i in range(P)]
    sums=[B[i]+B[j] for i in range(P) for j in range(i,P)]
    return len(set(sums))==len(sums) and B==sorted(B) and B[-1]==2*P*(P-1)+1
print('ET-SIDON', [(P, sidon_ok(P)) for P in (3,5,7,11,13,17,19,23,29,31,47,53)])
