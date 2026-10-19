"""Coupled LARGE-A (lead, 2026-10-19, exploratory): instead of spending the GLOC budget separately on r, eps and b
(LARGE-A'), enumerate q (r = Q - q) and b exactly and take the largest eps allowed jointly by
  (GLOC)  Delta(q) + 3*eps + b*B1 <= M_A(a) - 1,   B1 = a-1-2alpha-R0 >= 0,
          Delta(q) = (a+2)q - 3 q^<2>,  M_A(a) = (a-2alpha-1)R0 + 2U0 + 2alpha + 1 - a,
  (W_A<0) 4(q^<2> - eps) >= 3a(a+1) + (a-3)q + 1,      0 <= eps <= q^<2>.
Then test cyclic SP on n = a+1-r residues against the cardinality bound:
  n^3 - n^2 + 2n - 3n*eps  >  2[C(a+b+3,3) + k0max + k1max + cmax(a+b+1) + emax]   (as in LARGE-A').
For each alpha report the least a0 >= 1+2alpha+R0 from which every (q,b) passes, for all a in [a0, 10 R0).
usage: python coupled_large_a.py alphamin alphamax"""
import sys
from math import comb, isqrt
def C(n,k): return comb(n,k) if n>=k>=0 else 0
def mac2(x):
    if x<=0: return 0
    k2=2
    while C(k2+1,2)<=x: k2+=1
    return C(k2+1,3)+C(x-C(k2,2)+1,2)
def closes(al,a):
    R0=C(al+1,2); U0=C(al+2,3); Q=C(a+1,2); F=C(a+1,3)
    B1=a-1-2*al-R0
    if B1<0 or a<2*al+1 or 4*(a+1)<5*(al+3): return False
    M=(a-2*al-1)*R0+2*U0+2*al+1-a
    k0=(al+3)*U0//4; k1=(al+2)*R0*a//3
    c=isqrt(F)
    while c*(c+1)>F-1: c-=1
    e=F//(3*a)
    for q in range(Q,-1,-1):
        r=Q-q; m2=mac2(q); D=(a+2)*q-3*m2
        if D>M-1: continue
        epsW=m2-(3*a*(a+1)+(a-3)*q+1+3)//4          # eps <= m2 - ceil((3a(a+1)+(a-3)q+1)/4)
        if epsW<0: continue
        bmax=(M-1-D)//B1 if B1>0 else 0
        n=a+1-r
        for b in range(0,bmax+1):
            eps=min((M-1-D-b*B1)//3, epsW, m2)
            if eps<0: break
            if n<5: return False
            lhs=n**3-n**2+2*n-3*n*eps
            rhs=2*(C(a+b+3,3)+k0+k1+c*(a+b+1)+e)
            if lhs<=rhs: return False
    return True
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for al in range(lo,hi+1):
    R0=C(al+1,2); top=10*R0
    a0=None
    for a in range(top-1, 1+2*al+R0-1, -1):   # scan downward: a0 = least a with closes() for all a in [a0, top)
        if not closes(al,a): break
        a0=a
    print(f"alpha={al} R0={R0} coupled a0={a0} a0/R0={(a0/R0 if a0 else float('nan')):.3f}  (LARGE-A' needs 10R0={top})",flush=True)
