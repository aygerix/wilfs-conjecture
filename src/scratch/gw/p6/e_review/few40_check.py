"""Lead's independent symbolic check of the P6e algebra (2026-10-19): (LC) completion of the square in LINKED-CUBIC,
R increasing, (FP40) and the k = 40t+7 endpoint, (FP72), and the GENERAL-FEW80 numeric margins."""
import sympy as sp
v, e, t, x, y, k = sp.symbols('v e t x y k')
qD = v*(v+1)/2-e; X = 2*e-v
lhs = (sp.binomial(qD, 2).expand(func=True)+(v+1)*(X**2/(2*v)-X/2))/v
R = (4*v**4-16*v**2-12*v-1)/(8*(5*v+4))
rhs = R+(5*v+4)/(2*v**2)*(e-v*(v**2+7*v+5)/(2*(5*v+4)))**2
print("LC identity:", sp.simplify(sp.together(lhs-rhs)) == 0)
num = sp.factor(sp.together(R.subs(v, v+1)-R)).as_numer_denom()
print("R(v+1)-R(v) numerator:", sp.expand(num[0]), "| shifted:", sp.expand(sp.expand(num[0]).subs(v, x+1)))
print("R - v(v+1)(v-3)/10 numerator:", sp.factor(sp.together(R-v*(v+1)*(v-3)/10)))
# FP40: n = 20t+4+x, R(n) - t[(n+1)(2n+3)+2t], numerator over 8(5n+4)
n = 20*t+4+x
expr = sp.together(R.subs(v, n)-t*((n+1)*(2*n+3)+2*t))
nu, de = expr.as_numer_denom()
print("FP40 numerator:", sp.expand(nu*sp.sign(1)), "| denominator:", sp.factor(de))
n2 = 20*t+3
e2 = sp.together(R.subs(v, n2)-t*((n2+1)*(2*n2+3)+2*t)); print("endpoint numerator:", sp.expand(e2.as_numer_denom()[0]))
# C - 2kt - 2t^2 - 2t at k = 40t+8+y
C = k*(k-1)/2
print("FEW40 C-2kt-2t^2-2t:", sp.expand((C-2*k*t-2*t**2-2*t).subs(k, 40*t+8+y)))
print("FEW72 C-2kt-2t^2-2t:", sp.expand((C-2*k*t-2*t**2-2*t).subs(k, 72*t+10+y)))
nn = 36*t+5+x
print("FP72:", sp.expand(nn*(nn+1)*(nn-3)-18*t*((nn+1)*(2*nn+3)+2*t)))
