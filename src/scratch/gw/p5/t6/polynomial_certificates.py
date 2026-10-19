"""Exact P5f certificates in Q[X], N=480+120X. Fejer only.

No interpolation or symbolic package. Positive coefficients certify
each displayed relaxed-profile inequality for every integer X>=0.
"""
from fractions import Fraction as F
import json

class P:
    def __init__(self,v=0):
        self.c=dict(v) if isinstance(v,dict) else {0:F(v)}
        self.c={k:F(x) for k,x in self.c.items() if x}
    def __add__(self,o):
        o=poly(o);c=self.c.copy()
        for k,v in o.c.items():c[k]=c.get(k,F(0))+v
        return P(c)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.c.items()})
    def __sub__(self,o):return self+-poly(o)
    def __rsub__(self,o):return poly(o)+-self
    def __mul__(self,o):
        o=poly(o);c={}
        for k,v in self.c.items():
            for j,w in o.c.items():c[k+j]=c.get(k+j,F(0))+v*w
        return P(c)
    __rmul__=__mul__
    def __truediv__(self,o):return self*F(1,o)
    def __pow__(self,k):
        r=P(1)
        for _ in range(k):r=r*self
        return r
    def at0(self):return self.c.get(0,F(0))
    def dump(self):return [str(self.c.get(k,F(0))) for k in range(max(self.c,default=0)+1)]
def poly(o):return o if isinstance(o,P) else P(o)
def C(n,k):
    z=P(1)
    for j in range(k):z=z*(n-j)/(j+1)
    return z
def H(n):return n*(C(n,2)+1)

certs={}
for mode in ('base','B','l','matching'):
    N=P({0:480,1:120});a=3*N;al=N;p=2*N
    b=N/8 if mode=='B' else P(0)
    l=N/10 if mode=='l' else P(0)
    r=N if mode=='matching' else P(0)
    cv=r
    ex=N/10 if mode=='l' else P(1 if mode=='matching' else 0)
    Q=C(a+1,2);QA=C(N+1,2);q=Q-r;q2=QA+l
    tf=a*r-C(r,2);eps=N**3/24;t=tf+eps;ep=eps-C(cv,2)
    c0=C(N+2,3);D3=3*t-(a+2)*r
    LC=(a+1)*q2;FF=C(a+1,3)
    WA=-FF+LC-(a-3)*r+4*t
    R=29*N/20;delta=57*N**3/100;hh=43*N**3/25
    L=(hh-delta)/2;rho=None
    S=l*(a+2-l)
    bf=a-1+q2-2*N;bh=a-1+q2-2*(N+ex+l)
    CH=N+QA+c0+l+ex+C(ex+2,3)+(QA+N*ex)*p
    CP=N+QA+c0+l+ex+C(ex+2,3)+QA*p+l*(p-ex)+N*C(ex+1,2)
    jlo=P(1 if mode=='l' else 0)
    CPlo=N+QA+c0+l+jlo+C(jlo+2,3)+QA*p+l*(p-jlo)+N*C(jlo+1,2)
    fix=D3+a-1-2*N-2*c0+(a+3)*QA+S-2*QA*R+b*bf
    delta_up=2*CP-a-(a+3)*q2-D3-b*bh
    payment=(a-1)*(b+1)+LC+D3+(b+2)*q2
    d=a+b;m=C(d+3,3)-r*(1+b)-t;rho=m-hh
    v3=b*(q-q2);ww=a*C(b+1,2);zz=C(b+2,3)
    sr=C(b+1,2)+v3+ww+zz
    W=WA+2*b*r+rho-sr
    core=C(p-ex+2,3)-p*r-ep
    hot=core-(hh-3*delta)/2
    K=q-q2+b
    Jfix=N+c0+QA*R+C(l+1,2)+b*N
    JH=CP+b*(N+ex+l)
    Z=t-a*r+C(r,2)
    checks={
      'negative_WA':-WA-1,'negative_W_formal':-W-1,
      'LC_minus':3*FF-3*(a+1)*q2-(a+17)*r-1,
      'q2_le_q':q-q2,'legal_e_positive':ep,
      'cover_budget':Z-C(cv,2),'HPAIR_dominates':CH-CP,
      'convex_endpoint':CP-CPlo,
      'fixed_payment':-fix-1,'LOW_FIN':3*delta-payment-1,
      'DELTA_PAIR':delta_up-delta,
      'raw_fixed':2*(K+Jfix)+2-hh,
      'raw_H0':K+JH+1-(hh+delta)/2,
      'low_loop_range':3*L-hh,
      'end_test_fails':hh-2*K-payment-1,
      'nonwrapping_end':m-2*hh,
      'ASR_HOT':rho-sr-hot-(1+a+q2),
      'HOT_payment':-WA-2*b*r-hot-1,
      'HIGH_payment':-(LC+C(p-R+2,3)-FF+5*r+D3+2*b*r+1+a+q2)-1,
      'height':m-hh,'hot_nonnegative':hot,
      'joint_COUNT':9*delta/2-2-C(N+R+2,3)+t,
      'wide_COUNT':3*delta-2-C(R+2,3)+t,
      'short_COUNT':3*delta/2-2-C(R-ex+2,3)+t,
    }
    er=C(r+1,2)
    for name,n,cap in [('global',a+1-cv,m),
       ('joint',N+R-cv,9*delta/2-2),('wide',R-cv,3*delta-2),
       ('short',R-ex-cv,3*delta/2-2)]:
        n0=n.at0(); assert n0.denominator==1
        n3=int(n0)%3
        lam2=3*n if n3==0 else 3*(n-1)
        checks[name+'_SP']=2*cap-2*H(n)+lam2*ep
        checks[name+'_Q']=2*cap-2*H(n)+18*C(ep+1,2)
    checks['global_PSP']=m-H(a+1)+4*er+9*((a+1)*er+(r+1)*ep+C(ep,2))
    for key,nn,cap in [('joint',N+R,9*delta/2-2),
        ('wide',R,3*delta-2),('short',R-ex,3*delta/2-2)]:
        checks[key+'_PSP']=cap-H(nn)+4*er+9*(nn*er+(r+1)*ep+C(ep,2))
    # One explicit full q_g witness suffices for the MIX-PACK existential.
    gap=r*(4*d-3*r-1)/2
    M=-WA-1;eg=(D3-WA)/3-1
    # gap vanishes in modes with b>0; d=a in matching mode.
    eg=eg-gap/3
    Zg=(d*r-C(r,2))+eg-d*r+C(r,2)
    V=t-a*r
    epg=eg-C(cv,2)
    checks['MIX_RANGE_1']=M+2*(a-1)*r-gap
    checks['MIX_RANGE_2']=D3+M-gap
    checks['MIX_COVER']=Zg-V-C(cv,2)
    ng=d+1-cv
    lm=3*ng if int(ng.at0())%3==0 else 3*(ng-1)
    checks['MIX_SP']=2*m-2*H(ng)+lm*epg
    checks['MIX_Q']=2*m-2*H(ng)+18*C(epg+1,2)
    checks['MIX_PSP']=m-H(d+1)+4*er+9*((d+1)*er+(r+1)*epg+C(epg,2))
    failed={key:v.dump() for key,v in checks.items() if any(x<0 for x in v.c.values())}
    certs[mode]={'checks':len(checks),'failed_positive_coefficient_test':failed,
       'coefficients':{key:v.dump() for key,v in checks.items()}}
    print(mode,len(checks),'all_coefficients_nonnegative',not failed,flush=True)
with open('polynomial_certificates.json','w') as fp:json.dump(certs,fp,indent=2)
assert all(not v['failed_positive_coefficient_test'] for v in certs.values())

# Numerical constants in the two unconditional theorems; these rational
# inequalities are the only numerical comparisons in their paper proofs.
assert F(729,3072)<F(1,4)
assert F(1,4)+F(1,120)+F(3,64)+F(1,2880)<F(1,3)
assert F(3135,8192)>F(1,3)
assert F(291,256)**3<F(3,2)
assert F(67,2048)<F(1,24)
assert F(4,3)*(F(9,8)+F(1,256))/256<F(1,128)
assert F(161,512)-F(257,256)**2/512>F(3,10)
assert F(1,4)+F(1,24)+F(1,128)<F(3,10)
assert F(4,3)*(F(9,8)+F(1,160))/160<F(1,96)
assert F(1,4)+F(1,120)+F(1,96)<F(1,3)
print('10 exact constant comparisons passed')

# A second blow-up: b has order alpha^(3/2), and all missing mixed
# quadratic monomials are B loops. No pair repair of this graph can
# retain a B direction. This is an abstract profile certificate only.
s=P({0:1,1:1});N=14400*s**2;b=216000*s**3;a=3*N;d=a+b
Q=C(a+1,2);QA=C(N+1,2);UA=C(N+2,3);UP=C(2*N+2,3)
U=C(a+2,3);q2=QA;q3=Q-QA;R=2*N
t=UA;D3=3*UA;LC=(a+1)*QA;WA=-C(a+1,3)+LC+4*UA
t3=C(b,2);v3=b*q3;ww=a*t3;zz=C(b,3)
m=1+d+Q+a*b+t3+U-UA+b*Q+ww+zz
SR=t3+v3+ww+zz;Xsr=1+a+QA
hh=m-SR-UP-Xsr;delta=3*hh/5;L=hh/5
ell=4+3*a+2*b+2*QA+q3+a*b+t3
Ncells=m-1-d
W=(d+1)*(ell-4)-4*Ncells+(m-hh)
Dm=2*a*b+2*b*(b-1)
assert not (W-(WA+4*b+Dm+UP+Xsr)).c
gap=b*(4*d-3*b-1)/2;epg=UA+C(b,2)
assert not (D3+Dm-gap-3*epg).c
assert not (m-(C(d+3,3)-b-d*b-UA)).c
K=q3+b;beta=QA;bf=a-1+QA-2*N-2*QA
CP=N+QA+QA*2*N
payment=(a-1)*(b+1)+LC+D3+4*b+(b+2)*QA
fix=D3+a-1-2*N-2*QA+(a+3)*QA-2*QA*R+b*bf+4*b
upper=2*CP-a-(a+3)*QA-D3-4*b-b*bf
checks={
 'WA_negative':-WA-1,'W_negative':-W-1,
 'LC_minus':3*C(a+1,3)-3*(a+1)*QA-1,
 'FIX':-fix-1,'DELTA_PAIR':upper-delta,
 'LOW_plus_fails':3*delta-payment-1,
 'END_fails':hh-2*K-payment-1,
 'RAW_FIXED':2*(K+N+QA+QA*R+b*(N+QA))+2-hh,
 'RAW_H0':K+CP+b*(N+QA)+1-(hh+delta)/2,
 'ASR_hot_payment':-WA-4*b-Dm-UP-Xsr-1,
 'HIGH_payment':-(LC+UP-C(a+1,3)+D3+Xsr)-1,
 'nonwrapping_END':m-2*hh,
 'B_shadow':C(b+1,3)-C(b,3),
 'MIX_budget':-WA-4*b-Dm-UP-Xsr-1,
 'joint_COUNT':9*delta/2-2-C(3*N+2,3)+UA,
 'short_COUNT':3*delta/2-2-C(2*N+2,3)+UA,
 'wide_COUNT':3*delta-2-C(2*N+2,3)+UA,
 'global_SP':2*m-2*H(a+1)+3*a*UA,
 'global_Q':2*m-2*H(a+1)+18*C(UA+1,2),
 'MIX_SP_after_B_loop_cover':2*m-2*H(a+1)+3*a*UA,
 # These stronger, hypothetical zero-defect bounds also pass. They
 # identify the limitation of endpoint deletion, not a proof of P(0).
 'global_H_perfect':m-H(a+1),
 'joint_H_perfect':9*delta/2-2-H(3*N),
 'short_H_perfect':3*delta/2-2-H(2*N),
 'wide_H_perfect':3*delta-2-H(2*N),
}
bad={k:v.dump() for k,v in checks.items() if any(x<0 for x in v.c.values())}
print('B-heavy',len(checks),'all_coefficients_nonnegative',not bad)
with open('heavy_certificates.json','w') as fp:
    json.dump(dict(checks=len(checks),failed=bad,
       coefficients={k:v.dump() for k,v in checks.items()}),fp,indent=2)
assert not bad
