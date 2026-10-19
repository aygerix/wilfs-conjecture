"""LARGE-A' (lead, 2026-10-19): the threshold a >= 16*R0^2 of P5_REPORT section 46 is an artifact of crude
lower-order bounds.  Re-run the section 46 chain with exact Macaulay in step 1 and with the exact final comparison
    LHS(a) = n0^3 - n0^2 + 2 n0 - n0*K*a                      (2m >= ..., cyclic SP; n0 = a+1-K, 3*eps_M < K*a)
    RHS(a) = 2*[C(d0+3,3) + k0max + k1max + cmax*(d0+1) + emax] (2m <= ...; d0 = a+2K-1)
with R0 = C(alpha+1,2), K = R0-1, U0 = C(alpha+2,3), F = C(a+1,3),
    k0max = floor((alpha+3)U0/4), k1max = floor((alpha+2)*R0*a/3)   (u1 <= n0*p <= R0*a),
    cmax = max c with c(c+1) <= F-1,  emax = floor(F/(3a)).
For each alpha, find the least a0(alpha) such that LHS(a) > RHS(a) for ALL a in [a0, 40*a0] (checked exactly),
and report a0/R0.  Also checks the side conditions used in the chain at a0:
    a >= 2(1+2alpha+R0) (b coefficient >= a/2), a >= 2alpha+1, a+1 >= 5(alpha+3)/4,
    step 1: a-3 >= 4(j+2)/3 and a >= 2j+5 for all j < R0 (q small => W_A >= 3a(a+1) > 0),
    step 3: Delta-block minima >= K*a for j in [R0, a-1] (r <= K).
usage: python large_a_prime.py alphamax"""
import sys
from math import comb, isqrt
def C(n,k): return comb(n,k) if n>=k>=0 else 0
def mac2(x):
    if x<=0: return 0
    k2=2
    while C(k2+1,2)<=x: k2+=1
    return C(k2+1,3)+C(x-C(k2,2)+1,2)
def ok(al,a):
    R0=C(al+1,2); K=R0-1; U0=C(al+2,3); F=C(a+1,3)
    n0=a+1-K; d0=a+2*K-1
    lhs=n0**3-n0**2+2*n0-n0*K*a
    k0=(al+3)*U0//4; k1=(al+2)*R0*a//3
    c=isqrt(F); 
    while c*(c+1)>F-1: c-=1
    e=F//(3*a)
    rhs=2*(C(d0+3,3)+k0+k1+c*(d0+1)+e)
    return lhs>rhs
def side(al,a):
    R0=C(al+1,2); K=R0-1
    if not (a>=2*(1+2*al+R0) and a>=2*al+1 and 4*(a+1)>=5*(al+3)): return False
    j=R0-1   # step 1 conditions are monotone in j; check the largest j < R0
    if not (3*(a-3)>=4*(j+2) and a>=2*j+5): return False
    def D(j,z): return (a-j)*C(j+1,2)+(a+2)*z-3*C(z+1,2)
    for j in (R0, a-2):
        if R0<=j<=a-2:
            for z in (0,j):
                if D(j,z)<K*a: return False
    for r in (R0, a):     # block j=a-1: Delta=r(4a-3r-1)/2
        if r<=a and r*(4*a-3*r-1)<2*K*a: return False
    return True
amax=int(sys.argv[1]); worst=0
for al in range(4,amax+1):
    R0=C(al+1,2)
    a=2*R0
    while not (ok(al,a) and side(al,a)): a+=1
    # verify all a in [a, 40a] exactly (coarse step beyond 4a, the difference is a cubic with positive lead)
    st=max(1,a//2000)
    good=all(ok(al,x) and side(al,x) for x in range(a,4*a+1,st)) and all(ok(al,x) for x in range(4*a,40*a,max(1,a//50)))
    worst=max(worst,a/R0)
    if al<=12 or al%25==0 or not good: print(f"alpha={al} R0={R0} a0={a} a0/R0={a/R0:.3f} range_ok={good}",flush=True)
print("max a0/R0 over alpha in [4,%d] = %.4f"%(amax,worst))
