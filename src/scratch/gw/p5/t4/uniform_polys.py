"""Exact polynomial audit for the uniform small-defect theorem. fejer."""
from uniform_identities import P,v,check,C2,C3,checks
from fractions import Fraction as F
import json
al=v['alpha'];x=v['j'];bb=v['b']
aa=2*al+1+x;Q=C2(al+1)
B=(aa-2*al-1)*Q+2*C3(al+2)+2*al-aa+1
nn=(3*aa+4*al+5)/6+3*bb/8
poly=nn**3-nn**2+2*nn-3*nn*Q/4-9*B-9*bb*Q/4+10
def terms(z):
    return [{','.join(k+'^'+str(e) for k,e in zip(v,t) if e):str(c)} for t,c in sorted(z.d.items())]
print(json.dumps(dict(terms=terms(poly))),flush=True)
# Explicit square completion below is a nonnegative certificate:
# replace (5al+3)x^2/4 - (25/48)al^2*x by
# (5al/4)(x-5al/24)^2 -125al^3/2304, retaining 3x^2/4.
base=poly
certificate=poly-(5*al/4)*(x-5*al/24)**2
print(json.dumps(dict(after_square=terms(certificate))),flush=True)
aa=5*al/3+1+x
B=(aa-2*al-1)*Q+2*C3(al+2)+2*al-aa+1
nn=aa/2+2*al/3+P(F(3,4))+3*bb/10
poly=nn**3-nn**2+2*nn-3*nn*Q/4-9*B-18*bb*Q/5+10
print(json.dumps(dict(global_poly=terms(poly))),flush=True)
cert=poly-(9*al/8)*(x-7*al/12-P(F(1,4)))**2
print(json.dumps(dict(global_after_square=terms(cert))),flush=True)
z=al-4
positive=(119*z**3+1086*z**2+2559*z+2126)/128+355*x/32+11*x**2/16+x**3/8
positive+=bb*(P(F(201,160))+33*x/40+9*x**2/40+9*al/16+27*al*x/20+9*al**2/80)
positive+=bb**2*(P(F(99,400))+27*x/200+81*al/200)+27*bb**3/1000
check('uniform small-defect positive certificate',cert,positive)
print(json.dumps(dict(global_certificate_verified=True)),flush=True)
