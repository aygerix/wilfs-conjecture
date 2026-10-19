"""Exact polynomial certificates for a general cubic-defect theorem.
fejer only.  No conjectural ambient packing input.
"""
from fractions import Fraction as F
from math import comb,isqrt
from pathlib import Path
import json

def add(*ps):
    z=[F(0)]*max(map(len,ps))
    for p in ps:
        for j,x in enumerate(p):z[j]+=x
    while len(z)>1 and not z[-1]:z.pop()
    return z
def mul(a,b):
    z=[F(0)]*(len(a)+len(b)-1)
    for j,x in enumerate(a):
        for k,y in enumerate(b):z[j+k]+=x*y
    return z
def scale(p,c):return [F(c)*x for x in p]
def shift(p,A):return [sum(p[j]*comb(j,i)*A**(j-i) for j in range(i,len(p))) for i in range(len(p))]
Q=[0,F(1,2),F(1,2)];U=[0,F(1,3),F(1,2),F(1,6)]

out={}
for label,c,g in [('D14',F(1,14),F(1,12)),('D075',F(3,40),F(2,25))]:
    assert g-g*g/2>c
    v=1-g
    # j=Q-p <= g*k, hence a<=g*k and a missing-pair cover deletes <=g*k
    # directions. The retained full pair set has at least v*k directions.
    n=[0,v];H=[1,F(3,2)*v,v*v,F(1,2)*v**3]
    N=[1,F(3,2)-g,F(1,2)];J=scale(mul(N,add(N,[-1])),F(1,2))
    ends={};largest=0
    for tag,r in [('zero',[0]),('max',[0,0,c])]:
        M=add(H,scale(mul(add(scale(n,3),[-3]),r),-1))
        t=add(U,scale(r,-1));B=add([0,g],scale(t,2))
        # Drop a*t + C(a,2), nonnegative for integral a>=0.
        P=add(mul(add(M,scale(add(Q,t),-1)),J),
              scale(mul(B,add(M,[-1])),-1),mul(t,add(t,[-1])))
        for A in range(3,101):
            cf=shift(P,A)
            if all(x>=0 for x in cf):break
        else:raise AssertionError(label)
        largest=max(largest,A)
        ends[tag]=dict(poly=list(map(str,P)),shift=A,coeff=list(map(str,cf)))
        print('GENERIC_ENDPOINT',label,tag,'shift',A,'poly',list(map(str,P)),'coeff',list(map(str,cf)))
    small=[]
    # Actual Bonferroni bound j <= j_max(r), not just the linear surrogate.
    # q<=Q, a<=j and p>=Q-j give a valid lower CR bound by decreasing q to
    # its worst upper bound, N to its lower bound and B to its upper bound.
    for k in range(3,largest):
        for r in range(int(c*k*k)+1):
            jmax=max(j for j in range(3*r//k+1) if k*j-j*(j-1)//2<=r)
            h=k-jmax
            assert h>=2
            Hh=(h**3+2*h*h+3*h+2)//2
            m0=Hh-3*(h-1)*r
            t=comb(k+2,3)-r;q=comb(k+1,2);Nn=1+k+q-jmax;Jj=comb(Nn,2)
            # q=Q and a=j_max is relaxed: p actually depends jointly on q,a.
            # It is safe to decouple them using q+t<=Q+t, B<=j_max+2t.
            assert m0-q-t>=0,(label,k,r,jmax,m0-q-t)
            cr=(m0-q-t)*Jj-(jmax+2*t)*(m0-1)+t*(t-1)
            assert cr>=0,(label,k,r,jmax,m0,cr)
            small.append(dict(k=k,r=r,jmax=jmax,retained=h,m_lower=m0,CR_lower=cr))
    print('GENERIC_SMALL',label,'K',largest,'rows',len(small),'min',min((z['CR_lower'] for z in small),default=None))
    out[label]=dict(c=str(c),g=str(g),K=largest,endpoints=ends,small=small)
Path('generic_density.json').write_text(json.dumps(out,indent=2)+'\n')
print('GENERIC_DENSITY_ALL_PASS')
