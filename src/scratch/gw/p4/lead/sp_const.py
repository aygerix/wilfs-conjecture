# Lead check of P4_REPORT sec.17: max over g>=2, t_i in {1,2,3}, sum t_i<=s of sum_{i<j}t_it_j/(g-1)
from fractions import Fraction as Fr
def best(s):
    b=Fr(0)
    for n1 in range(s+1):
        for n2 in range((s-n1)//2+1):
            for n3 in range((s-n1-2*n2)//3+1):
                g=n1+n2+n3
                if g<2: continue
                S1=n1+2*n2+3*n3; S2=n1+4*n2+9*n3
                b=max(b,Fr(S1*S1-S2,2*(g-1)))
    return b
def claim(s):
    if s==2: return Fr(1)
    if s==3: return Fr(2)
    if s==4: return Fr(4)
    return Fr(3*s,2) if s%3==0 else Fr(3*(s-1),2)
bad=[s for s in range(2,101) if best(s)!=claim(s)]
print("SP constant mismatches s=2..100:",bad)
