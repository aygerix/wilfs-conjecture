"""Independent endpoint certificate with analytic GLOC pruning.
Run on fejer only; argv amin amax. alpha=3 at a>=13 is GW-26e.

GLOC/HLOC use actual low-cubic counts and refined cold-pair outside
costs. It is a necessary-profile search, not a semigroup enumeration.
"""
from math import comb,isqrt
from collections import Counter
import json,sys,os
from functools import lru_cache

@lru_cache(None)
def C(n,k):return comb(n,k) if n>=k else 0
@lru_cache(None)
def mac(q,d=2):
    out=0;top=1000
    for j in range(d,0,-1):
        z=j-1
        while C(z+1,j)<=q and z+1<top:z+=1
        out+=C(z+1,j+1);q-=C(z,j);top=z
    assert q==0
    return out
@lru_cache(None)
def H(n):return n*(C(n,2)+1)
def L2(n):
    if n<=4:return (0,0,2,4,8)[n]
    return 3*n if n%3==0 else 3*(n-1)
def cd(x,d):return -((-x)//d)
def sp2(n,ep):
    lin=2*H(n)-L2(n)*ep
    return max(lin,2*H(n)-18*C(ep+1,2)) if os.environ.get('P5E_QUADRATIC','1')!='0' else lin
@lru_cache(None)
def cover(r,z):
    assert z>=0
    if not r:return 0
    if not z:return 1
    out=min(r,(1+isqrt(1+8*z))//2)
    dm=1+cd(C(r,2)-z,r)
    if dm>=3:out=min(out,1+z//(dm-2))
    return out
@lru_cache(None)
def exception_cover(a,al,r,rll,l,k):
    if r==0:return min(a-al,l) if k==0 and rll==0 else -1
    if r>a*k-C(k,2):return -1
    out=-1;p=a-al
    def f(c):return al*c-C(c,2)
    for cl in range(max(0,k-p),min(al,k)+1):
        if rll>f(cl):continue
        if cl<al:out=max(out,min(p,l+min(k-cl,r-rll,r-k+1)))
        if cl:
            dl=max(0,rll-f(cl-1));rem=r-k+1-dl
            if rem>=0:out=max(out,min(p,l+min(r-rll,rem)))
    return out
@lru_cache(None)
def mixpack(a,b,r,q,q2,t,u,k,wa,hot,D3):
    d=a+b;Qd=C(d+1,2);M=-wa-hot-1-b*u
    if M<0:return False
    smin=max(0,a*b-M);tmin=max(0,cd(b*smin+a*b-M,2*a))
    for qg in range(q+smin+tmin,Qd-r+1):
        mg=mac(qg);gap=(d+2)*qg-3*mg
        if gap>M+2*(a-1)*r or gap>D3+M:continue
        ep=(D3+M-gap)//3;rg=Qd-qg
        zt=C(d+2,3)-mg+ep-d*rg+C(rg,2)
        z=zt-max(0,t-a*r)
        if z<0:continue
        cv=min(d,cover(rg,z));nn=d+1;er=C(rg+1,2);lower=10**50
        for cv0 in range(1 if rg else 0,cv+1):
            ep0=min(ep,zt-C(cv0,2))
            if ep0<0:continue
            n=nn-cv0
            lower=min(lower,max(cd(sp2(n,ep0),2),H(nn)-4*er-9*(nn*er+(rg+1)*ep0+C(ep0,2))))
        co=qg+q2+u;upper=-1
        ub0=min(C(d+3,3)-r*(1+b)-t+k,1+d+Qd-r+mg+k)
        for cc in range(M//(co+2)+1):
            left=M-cc*(cc+1+co)
            if left<0:break
            ee=left//(3*a+2*b+cc+co)
            upper=max(upper,ub0+cc*(d+1)+ee)
        if lower<=upper:return True
    return False
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
    for al in range(4 if a>=13 else 3,a+1):
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
          allowance=F-(a+1)*q2+(a-3)*r-4*t-1
          coef0=a-al-2;coef1num=3*a-4*al-5
          gbase=D3+a-1-2*al-2*UA+(2*al+1-a)*n0+S
          gcoef0=4*a-5*al-11;gcoef1=a+1-al
          gloc_valid=gcoef0>=0 and gcoef1>=0 and a-1-2*al-n0+l>=0 and q+q2+1>=2*al
          if gloc_valid and gbase>=0:
           counts['GLOC_t_closed']+=1
           continue
          # LCbar-(a+1)q2 >= coef0*u0+(coef1num/3)*u1.
          # Omitted states have WAbar>=0 and never contribute to u counts.
          u0max=min(UA,allowance//coef0) if coef0>0 and coef1num>=0 else UA
          if gloc_valid and gcoef0>0:u0max=min(u0max,4*(-gbase-1)//gcoef0)
          for u0 in range(u0max+1):
           k0=min(mac(u0,3),(al+3)*u0//4)
           u1max=min(p*n0,(al+1)*l//2,U-t-u0,mac(q2)-u0)
           lc0=(a+1)*u0-4*k0
           if coef1num>0:u1max=min(u1max,3*(allowance-lc0)//coef1num)
           elif coef1num==0 and lc0>allowance:continue
           if gloc_valid and gcoef1>0:u1max=min(u1max,(4*(-gbase-1)-gcoef0*u0)//(4*gcoef1))
           for u1 in range(u1max+1):
            u=u0+u1;k1=(al+2)*u1//3;k=k0+k1
            LC=(a+1)*(q2+u)-4*k
            assert LC>=(a+1)*q2,(a,al,r,n0,l,u0,u1)
            WA=-F+LC-(a-3)*r+4*t
            if WA>=0:continue
            counts['u']+=1
            # Transfer pays each B at least u+min(2r,2a-r).
            bc=u+max(0,min(2*r,2*a-r))
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
               cv=cover(r,t-a*r+C(r,2)-max(0,t0-al*(QA-n0)))
               ns=max(0,R-l-r-cv);nw=max(0,R-cv);nc=max(0,R-l-r);nj=max(0,al+R-cv)
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
                ng=max(0,a+1-cv)
                ml=max(cd(2*H(ng)-L2(ng)*eps,2),H(a+1)-4*er-9*((a+1)*er+(r+1)*eps+C(eps,2)))
                if ml>maxm:continue
                upper=min(upper,maxm-2)
                low=cd((a-1)*(b+1)+(a+1)*(q2+u)+D3+(b+2)*q2+b*u-3*k+1,3)
                dd=max(dm,low)
                if dd<=upper:
                 linked=10**50
                 for cv0 in range(1 if r else 0,min(a,cv)+1):
                  ep0=min(eps,t-a*r+C(r,2)-C(cv0,2))
                  if ep0<0:continue
                  level=int(os.environ.get('P5E_EREPAIR','3'))
                  ex0=E if level==0 else min(p,l+(r-cv0+1 if r else 0)) if level==1 else min(p,l+(min(r-(QA-n0),r-cv0+1) if r else 0)) if level==2 else exception_cover(a,al,r,QA-n0,l,cv0)
                  if ex0<0:continue
                  ch0=al+n0+c0+l+ex0+C(ex0+2,3)+(n0+al*ex0)*p
                  bh0=a-1+q2+u-2*(al+ex0+l+min(n0,u0+t0))
                  up0=2*ch0-(a-1)-(a+3)*q2-(a+1)*u+5*k-D3-b*bh0-1
                  nn0=a+1-cv0
                  ml0=max(cd(sp2(nn0,ep0),2),H(a+1)-4*er-9*((a+1)*er+(r+1)*ep0+C(ep0,2)))
                  if ml0>maxm:continue
                  ns0=max(0,R-l-r-cv0);nw0=max(0,R-cv0);nj0=max(0,al+R-cv0)
                  ps0=H(N)-4*er-9*(N*er+(r+1)*ep0+C(ep0,2))
                  lk=max(1,2*cd(sp2(ns0,ep0)+4,6)-1,
                       cd(sp2(nw0,ep0)+4,6),
                       cd(2*cd(sp2(nj0,ep0)+4,6)-1,3),
                       cd(2*cd(ps0+2,3)-1,3))
                  if max(dd,lk)<=min(upper,up0):linked=min(linked,lk)
                 dd=max(dd,linked)
                 if dd>upper:continue
                 if not mixpack(a,b,r,q,q2,t,u,k,WA,hot,D3):continue
                 counts['survive']+=1
                 out.append(dict(a=a,alpha=al,r=r,n0=n0,l=l,t=t,u0=u0,u1=u1,k0=k0,k1=k1,c0=c0,beta=beta,R=R,b=b,delta=[dd,upper],fixed=fix,bf=bf,bh=bh,WA=WA,hot=hot,m_upper=maxm,m_lower=ml))
    stats.update(counts)
    print(json.dumps(dict(a=a,**counts)),flush=True)
with open('small_survivors.json','w') as f:json.dump(out,f)
with open('small_unbounded.json','w') as f:json.dump(unbounded,f)
print(json.dumps(dict(total=dict(stats),survivors=len(out),unbounded=len(unbounded),first=out[:5],first_unbounded=unbounded[:5])),flush=True)
