"""Exact count relaxation for 7<=a<=13; run on fejer only.

GLOC/HLOC use actual low-cubic counts and refined cold-pair outside
costs. It is a necessary-profile search, not a semigroup enumeration.
"""
from math import comb,isqrt
from collections import Counter
import json,sys
from functools import lru_cache

def C(n,k):return comb(n,k) if n>=k else 0
def mac(q,d=2):
    out=0;top=1000
    for j in range(d,0,-1):
        z=j-1
        while C(z+1,j)<=q and z+1<top:z+=1
        out+=C(z+1,j+1);q-=C(z,j);top=z
    assert q==0
    return out
def H(n):return n*(C(n,2)+1)
def L2(n):
    if n<=4:return (0,0,2,4,8)[n]
    return 3*n if n%3==0 else 3*(n-1)
def cd(x,d):return -((-x)//d)
def star(a,p,l):
    if p==0:return 0
    k,z=divmod(l,p)
    return k*p*(a+2-p)+z*(a+2-z)
@lru_cache(None)
def mingap(d,qlo,qhi):
    if qlo>qhi:return 10**50
    out=10**50
    for j in range(d+1):
        base=C(j+1,2);lo=max(0,qlo-base);hi=min(j,qhi-base)
        if lo>hi:continue
        for z in (lo,hi):out=min(out,(d-j)*base+(d+2)*z-3*C(z+1,2))
    return out

amin=int(sys.argv[1]) if len(sys.argv)>1 else 7
amax=int(sys.argv[2]) if len(sys.argv)>2 else 13
out=[];stats=Counter();unbounded=[]
for a in range(amin,amax+1):
    Q=C(a+1,2);U=C(a+2,3);F=C(a+1,3);counts=Counter()
    for al in range(3,a+1):
      p=a-al;QA=C(al+1,2);UA=C(al+2,3)
      cold=[UA-mac(QA-be) for be in range(QA+1)]
      for r in range(Q+1):
       q=Q-r;tf=U-mac(q);gap=(a+2)*q-3*mac(q)
       for n0 in range(max(0,QA-r),QA+1):
        for l in range(al*p+1):
         q2=n0+l
         if q2>q or 3*(a+1)*q2+(a+17)*r>=3*F:continue
         tm=(F-(a+1)*q2+(a-3)*r-1)//4
         if tf>tm:continue
         counts['base']+=1
         S=star(a,p,l);E=min(p,l+r)
         assert q+q2+2>=2*(al+E),(a,al,r,n0,l)
         for t in range(tf,tm+1):
          D3=3*t-(a+2)*r;eps=t-tf
          for u0 in range(UA+1):
           k0=min(mac(u0,3),(al+3)*u0//4)
           for u1 in range(min(p*n0,(al+1)*l//2,U-t-u0,mac(q2)-u0)+1):
            u=u0+u1;k1=(al+2)*u1//3;k=k0+k1
            LC=(a+1)*(q2+u)-4*k
            assert LC>=(a+1)*q2,(a,al,r,n0,l,u0,u1)
            WA=-F+LC-(a-3)*r+4*t
            if WA>=0:continue
            counts['u']+=1
            # Transfer pays each B at least u+min(2r,2a-r).
            bc=u+min(2*r,2*a-r)
            assert bc>=0,(a,al,r,n0,l,u0,u1)
            for c0 in range(max(u0,UA-t,UA-al*(QA-n0)-eps),min(mac(n0),U-t-u1)+1):
             t0=UA-c0
             betamax=max(be for be in range(n0+1) if cold[be]<=u0+t0)
             # All beta>=1 are dominated by betamax in the fixed payment.
             for beta in ([0,betamax] if betamax else [0]):
              hot=0
              if beta:
               hot=max(0,C(p-E+2,3)-t+t0,
                   min(C(p-ee+2,3)-(p-ee)*max(0,r-(QA-n0)-max(0,ee-l))-eps for ee in range(E+1)))
               if WA+hot>=0:continue
              bcut=max(3,(-WA-hot+1)//2,isqrt(2*F+1)-a)
              btrans=min((-WA-hot-1)//bc,bcut) if bc else bcut
              betah=min(n0,u0+t0)
              bf=a-1+q2+u-2*al-2*beta
              bh=a-1+q2+u-2*(al+E+l+betah)
              CH=al+n0+c0+l+E+C(E+2,3)+(n0+al*E)*p
              B=2*CH-(a-1)-(a+3)*q2-(a+1)*u+5*k
              const=a-1-2*al-2*beta-2*c0+(a+3)*n0+S+(a+1)*u0-5*k0+(a+3)*u1-3*k1+D3
              for R in range(p+1):
               fix=const-2*n0*R
               if fix>=0 and bf>=0:continue
               bmax=btrans
               if bf>0:
                if fix>=0:continue
                z=(-fix-1)//bf;bmax=z if bmax is None else min(bmax,z)
               if bmax is None:
                unbounded.append(dict(a=a,alpha=al,r=r,n0=n0,l=l,t=t,u0=u0,u1=u1,c0=c0,beta=beta,R=R,fixed=fix,bf=bf,bh=bh,B=B,D3=D3,hot=hot,WA=WA))
                counts['unbounded']+=1
                continue
               ns=max(0,R-l-2*r);nw=max(0,R-r);nc=max(0,R-l-r);nj=max(0,al+R-r)
               dm=max(1,nc*(nc-1)+1-2*r*(r+1),
                  2*cd(2*H(ns)-L2(ns)*eps+4,6)-1,
                  2*cd(C(nc+2,3)-t+2,3)-1,
                  cd(2*H(nw)-L2(nw)*eps+4,6),cd(C(R+2,3)-t+2,3),
                  cd(R*(R-1)+2-2*r*(r+1),2),
                  cd(2*cd(2*H(nj)-L2(nj)*eps+4,6)-1,3),
                  cd(2*cd(C(al+R+2,3)-t+2,3)-1,3))
               N=al+R;er=C(r+1,2)
               psp=H(N)-4*er-9*(N*er+(r+1)*eps+C(eps,2))
               dm=max(dm,cd(2*cd(psp+2,3)-1,3))
               for b in range(bmax+1):
                if fix+b*bf>=0:continue
                upper=B-D3-b*bh-1
                counts['packing_profiles']+=1
                budget=-WA-hot-b*bc-1
                fullbudget=-WA-hot-1
                if fullbudget<mingap(a+b,q,C(a+b+1,2)-r-1)-2*(a-1)*r:
                 # MIX-GAP forces every AB/BB pair into I3.
                 rem=fullbudget-b*u-2*b*r
                 if rem<0:continue
                 maxfull=-1
                 basecost=q+q2+u+a*b+C(b+1,2)
                 for cc in range(rem//(basecost+2)+1):
                  left=rem-cc*(cc+1+basecost)
                  if left<0:continue
                  ee=left//(3*a+2*b+cc+basecost)
                  maxfull=max(maxfull,C(a+b+3,3)-r*(1+b)-t+k+cc*(a+b+1)+ee)
                 allmissing=t+b*r+rem//3
                 emall=allmissing-(C(a+b+2,3)-mac(C(a+b+1,2)-r))
                 if emall<0:continue
                 nf=max(0,a+b+1-r);nf0=a+b+1
                 minfull=max(cd(2*H(nf)-L2(nf)*emall,2),H(nf0)-4*er-9*(nf0*er+(r+1)*emall+C(emall,2)))
                 if minfull>maxfull:continue
                maxm=-1
                for cc in range(budget//(q+q2+u+2)+1):
                 left=budget-cc*(cc+1+q+q2+u)
                 if left<0:continue
                 ee=left//(3*a+2*b+cc+q+q2+u)
                 maxm=max(maxm,C(a+b+3,3)-r*(1+b)-t+k+cc*(a+b+1)+ee)
                ng=max(0,a+1-r)
                ml=max(cd(2*H(ng)-L2(ng)*eps,2),H(a+1)-4*er-9*((a+1)*er+(r+1)*eps+C(eps,2)))
                if ml>maxm:continue
                upper=min(upper,maxm-2)
                low=cd((a-1)*(b+1)+(a+1)*(q2+u)+D3+(b+2)*q2+b*u-3*k+1,3)
                dd=max(dm,low)
                if dd<=upper:
                 counts['survive']+=1
                 out.append(dict(a=a,alpha=al,r=r,n0=n0,l=l,t=t,u0=u0,u1=u1,k0=k0,k1=k1,c0=c0,beta=beta,R=R,b=b,delta=[dd,upper],fixed=fix,bf=bf,bh=bh,WA=WA,hot=hot,m_upper=maxm,m_lower=ml))
    stats.update(counts)
    print(json.dumps(dict(a=a,**counts)),flush=True)
with open('small_survivors.json','w') as f:json.dump(out,f)
with open('small_unbounded.json','w') as f:json.dump(unbounded,f)
print(json.dumps(dict(total=dict(stats),survivors=len(out),unbounded=len(unbounded),first=out[:5],first_unbounded=unbounded[:5])),flush=True)
