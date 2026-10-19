"""Lead's independent re-derivation of the P6b polynomial certificates (DENSE9, DENSE075, FEW-POLY, THREE-CUBICS).
Built from the definitions only (CR R(m), ROW-DEF M, FLAT-CR), not from codex's scripts."""
from sympy import symbols, Rational as Q, expand, Poly, binomial, simplify, diff, floor
k, e, x, m, t, a = symbols('k e x m t a')
def C2(n): return n*(n-1)/2
Qk = k*(k+1)/2; Uk = k*(k+1)*(k+2)/6
def H(h): return (h**3+2*h**2+3*h+2)/2
def coeffs(expr, var): return [Poly(expand(expr), var).coeff_monomial(var**i) for i in range(Poly(expand(expr), var).degree()+1)]
def R(mm, q, p, tt):
    aa = q-p; J = C2(1+k+p); B = aa+2*tt
    return (mm-q-tt)*J - B*(mm-1) + tt*(tt-1) + aa*tt + C2(aa+1)-aa  # C(a,2)=a(a-1)/2
# check C2(aa+1)-aa == aa(aa-1)/2
assert simplify(C2(a+1)-a - a*(a-1)/2) == 0
ok = True
# ---- DENSE9
M9 = H(k) .subs(k, k)  # placeholder
M9 = (k**3+2*k**2+3*k+2)/2 - 3*(k-1)*e
t9 = Uk - e
F = R(M9, Qk, Qk-a, t9)
print("DENSE9: M-|C| =", simplify(expand(M9 - (1+k+Qk+t9))), "  vs k(k^2-1)/3-(3k-4)e:", simplify(expand(M9-(1+k+Qk+t9) - (k*(k**2-1)/3-(3*k-4)*e))))
print("  eps^2 coefficient of F:", simplify(Poly(expand(F), e).coeff_monomial(e**2)))
dFa = diff(F, a)
# claimed derivative form
Na = 1+k+Qk-a
print("  dF/da matches claim:", simplify(expand(dFa - (-(M9-Qk-t9)*(Na-Q(1,2)) - M9 + t9 + a + Q(1,2)))) == 0)
E0 = expand(216*F.subs({a: k/3, e: 0})); E1 = expand(216*F.subs({a: k/3, e: k**2/9}))
print("  216 E0(k):", coeffs(E0, k)); print("  216 E0(4+x):", coeffs(E0.subs(k, 4+x), x))
print("  216 E1(k):", coeffs(E1, k)); print("  216 E1(7+x):", coeffs(E1.subs(k, 7+x), x))
for kk in range(3, 7):
    ee = (kk*kk)//9
    print("   k", kk, "F(k,0,0) =", F.subs({k: kk, e: 0, a: 0}), " F(k,floor(k^2/9),0) =", F.subs({k: kk, e: ee, a: 0}))
# ---- DENSE075
n = Q(23, 25)*k
M75 = H(n) - 3*(n-1)*e
N0 = 1+k+Qk-Q(2, 25)*k; J0 = C2(N0); t75 = Uk - e
G = (M75-Qk-t75)*J0 - (Q(2, 25)*k+2*t75)*(M75-1) + t75*(t75-1)
print("DENSE075: eps^2 coefficient of G:", simplify(Poly(expand(G), e).coeff_monomial(e**2)))
G0 = expand(703125000*G.subs(e, 0)); G1 = expand(5625000000*G.subs(e, Q(3, 40)*k**2))
print("  703125000 G0(k):", coeffs(G0, k)); print("  703125000 G0(4+x):", coeffs(G0.subs(k, 4+x), x))
print("  5625000000 G1(k):", coeffs(G1, k)); print("  5625000000 G1(12+x):", coeffs(G1.subs(k, 12+x), x))
for ee in [0, Q(3, 40)*k**2]:
    MQt = expand((M75-Qk-t75).subs(e, ee)); print("  M-Q-t at eps=", ee, ":", coeffs(MQt, k))
print("  f(2k/25)=", expand(k*(2*k/25)-(2*k/25)*(2*k/25-1)/2), " minus 3k^2/40:", expand(k*(2*k/25)-(2*k/25)*(2*k/25-1)/2 - Q(3, 40)*k**2))
# ---- FLAT-CR / FEW-POLY
C_2 = k*(k-1)/2
mm = k**2+k+1; s = mm - (1+k+Qk+t)
print("FEW: s at pair-pack min =", simplify(expand(s - (C_2 - t))) == 0)
Fflat_nopair = s*C_2 - 3*t*(mm-1) + t*(t-1)
print("  FEW-POLY matches:", simplify(expand(Fflat_nopair - (C_2**2 - (C_2+3*k*(k+1)+1)*t + t**2))) == 0)
FP = C_2**2 - (C_2+3*k*(k+1)+1)*t + t**2
print("  at t=k^2/16:", expand(FP.subs(t, k**2/16) - Q(3, 256)*k**2*(3*k**2-56*k+16)), "; 3k^2-56k+16 at 19+x:", expand((3*k**2-56*k+16).subs(k, 19+x)))
print("  dFP/dt at t=k^2/16 (should be <0):", expand(diff(FP, t).subs(t, k**2/16)))
print("  t=1:", simplify(expand(FP.subs(t, 1) - k*(k+1)*(k-5)*(k+2)/4)) == 0)
# THREE-CUBICS L2, L3 : full FLAT-CR with pair term, p = t
for tt, pp, sh in [(2, 2, 7), (3, 3, 8)]:
    s_ = mm - (1+k+Qk+tt)
    L = s_*C_2 + (k+s_+2)*C2(pp) - 3*tt*(mm-1) + tt*(tt-1)
    print("  4 L_%d(k):" % tt, coeffs(expand(4*L), k), " shifted:", coeffs(expand(4*L).subs(k, sh+x), x), " m-slope:", expand(C_2 + C2(pp) - 3*tt))
