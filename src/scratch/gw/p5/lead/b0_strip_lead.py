"""Lead's re-implementation of the B-free strip check (P5_REPORT section 47, last paragraph), from the text.
Branch r=l=b=0, alpha>=4.  Analytic ends: U-B0 closes a<=2alpha+2; a>=2Q+38 is closed analytically (section 45);
joint n<=32 is closed by LSP (lambda_n<=47 there) together with P47-B0.  For 33<=a<2Q+38, a>=2alpha+3 and every
joint size n=alpha+R with max(alpha,33)<=n<=a, a counterexample needs some integer eps in [e_min,e_max] with
    2H(n)-9B0+10+(27-L2(n))*eps <= 0       (JOINT-SP with 2(3ceil(3delta/2)-2)<=9delta-1, DELTA-UP delta<=B0-3eps-1)
    e_min = floor(Q/4)+1                    (U-SMALL)
    e_max = min( floor(((a-2alpha-1)Q-2a+3alpha)/6)        (MID-B0)
               , floor((B0-2)/3)                           (delta>=1)
               , floor((2Q(n-alpha)-a+2alpha+2U-(a+3)Q)/3) )  (R-LOW with D3=3eps, R=n-alpha)
usage: python b0_strip_lead.py alphamin alphamax"""
import sys
from math import comb

def lam2(n):
    if n <= 1: return 0
    if n == 2: return 2
    if n == 3: return 4
    if n == 4: return 8
    return 3*n if n % 3 == 0 else 3*(n-1)

def Hn(n): return n*(comb(n, 2)+1)

def run(al):
    Q = comb(al+1, 2); U = comb(al+2, 3)
    surv = []; tested = 0
    for a in range(max(33, 2*al+3), 2*Q+38):
        B0 = (a-2*al-1)*Q+2*U+2*al-a+1
        for n in range(max(al, 33), a+1):
            tested += 1
            emin = Q//4+1
            emax = min(((a-2*al-1)*Q-2*a+3*al)//6, (B0-2)//3, (2*Q*(n-al)-a+2*al+2*U-(a+3)*Q)//3)
            if emin > emax: continue
            coef = 27-lam2(n); base = 2*Hn(n)-9*B0+10
            if min(base+coef*emin, base+coef*emax) <= 0:
                surv.append((a, n, emin, emax))
    return tested, surv

if __name__ == '__main__':
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for al in range(lo, hi+1):
        tested, surv = run(al)
        print(f"alpha={al}: (a,n) pairs tested={tested} surviving={len(surv)}" + (f" first={surv[:3]}" if surv else ""))
