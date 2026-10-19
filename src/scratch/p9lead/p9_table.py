"""P9 §6 table: hypothesis on T_2/a, so A = (T_2/a)/4. Check XQ endpoint values, derivatives, and dXQ/dA > 0."""
import sympy as sp
A, x, z = sp.symbols('A x z')
XQ = (A-1)*x**2-(3*A+2)*x-(2*A+1)
for t, xv in ((8,9),(6,14),(5,24)):
    Av = sp.Rational(t,4)
    print('T2/a>=%s A=%s x=%s: XQ=%s dXQ/dx=%s dXQ/dA=%s' % (t, Av, xv, XQ.subs({A:Av,x:xv}), sp.diff(XQ,x).subs({A:Av,x:xv}), sp.diff(XQ,A).subs({x:xv})))
Av = sp.Rational(128,27)/4
print('T2/a>=128/27 A=%s: XQ(31+z)=%s' % (Av, sp.factor(sp.expand(XQ.subs({A:Av,x:31+z})))))
