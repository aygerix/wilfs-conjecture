"""Independent Fraction-free endpoint replay, alpha=4..14; fejer only."""
from math import comb
total=0
for A in range(4,15):
    Q=comb(A+1,2);U=comb(A+2,3);checks=0
    for a in range(max(33,2*A+3),2*Q+38):
        B=(a-2*A-1)*Q+2*U+2*A-a+1
        emin=Q//4+1
        for n in range(A,a+1):
            emax=min(((a-2*A-1)*Q-2*a+3*A)//6,(B-2)//3,
                     (2*Q*(n-A)-a+2*A+2*U-(a+3)*Q)//3)
            if emax<emin:continue
            L=3*n if n%3==0 else 3*(n-1)
            if n==2:L=2
            if n==3:L=4
            if n==4:L=8
            H=n*(comb(n,2)+1)
            # Check both endpoints, rather than selecting the adverse one.
            assert min(2*H-9*B+10+(27-L)*e for e in (emin,emax))>0,(A,a,n,emin,emax)
            checks+=1
    total+=checks
    print(dict(alpha=A,endpoint_intervals=checks,survivors=0),flush=True)
print(dict(total=total))
