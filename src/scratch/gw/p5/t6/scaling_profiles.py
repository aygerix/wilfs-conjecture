"""P5f: exact checks of specified relaxed profiles, not tiles. Run on fejer.

The P5e helpers are read only up to their enumeration driver. All new
arithmetic is integral or Fraction. No ambient packing hypothesis is used.
"""
from pathlib import Path
from math import comb, isqrt
from fractions import Fraction as F
import sys, json

hp = Path(sys.argv[1])
h = {}
exec(hp.read_text().split('\namin=int')[0], h)

def C(n,d): return comb(n,d) if n>=d else 0
def mac(q,d=2):
    out=0; top=None
    for j in range(d,0,-1):
        lo=j-1; hi=1
        while C(hi,j)<=q: hi*=2
        if top is not None: hi=min(hi,top)
        while hi-lo>1:
            mid=(lo+hi)//2
            if C(mid,j)<=q: lo=mid
            else: hi=mid
        out+=C(lo+1,j+1); q-=C(lo,j); top=lo
    assert q==0
    return out
h['mac']=mac

def check_profile(N, B=False, LL=False, RR=False):
    # Corrected base limit: theta=3, t/N^3=1/24,
    # delta/N^3=57/100, h/N^3=43/25, R/N=29/20.
    assert N%120==0
    al=N; a=3*N; b=N//8 if B else 0
    Q=C(a+1,2); U=C(a+2,3); QA=C(al+1,2); UA=C(al+2,3)
    r=N if RR else 0
    q=Q-r
    n0=QA; l=N//10 if LL else 0
    q2=n0+l; u0=u1=k0=k1=k=0; c0=UA; beta=betah=0
    t=U-mac(q)+N**3//24
    eps=t-(U-mac(q)); D3=3*t-(a+2)*r
    LC=(a+1)*q2; WA=-C(a+1,3)+LC-(a-3)*r+4*t
    R=29*N//20; p=a-al
    # A matching absent-pair graph when r=N; if r=0 cover=0.
    cv=r; zeta=t-a*r+C(r,2)
    ep0=min(eps,zeta-C(cv,2))
    ex=h['exception_cover'](a,al,r,0,l,cv)
    S=h['star'](a,p,l)
    bf=a-1+q2-2*al
    bh=a-1+q2-2*(al+ex+l)
    CH=al+n0+c0+l+ex+C(ex+2,3)+(n0+al*ex)*p
    jlo=h['cd'](l,al)
    def chpair(j):
        return al+n0+c0+l+j+C(j+2,3)+n0*p+l*(p-j)+al*C(j+1,2)
    CHpair=max(chpair(jlo),chpair(ex))
    fix=D3+a-1-2*al-2*c0+(a+3)*n0+S-2*n0*R+b*bf
    upper=2*CH-(a-1)-(a+3)*q2-D3-b*bh-1
    low=h['cd']((a-1)*(b+1)+(a+1)*q2+D3+(b+2)*q2+1,3)
    delta=57*N**3//100
    m=C(a+b+3,3)-r*(1+b)-t
    hh=43*N**3//25
    L=(hh-delta)//2
    rho=m-hh
    # Full mixed I3 face. All mixed cubics retained except those
    # with one of the r absent A pairs; these cost 2br in D_mix.
    v3=b*(q-q2); w=a*C(b+1,2); z=C(b+2,3)
    sr_base=C(b+1,2)+v3+w+z
    wilf=WA+2*b*r+rho-sr_base
    core=max(0,C(p-ex+2,3)-p*r-ep0)
    hot=max(0,core-max(0,(hh-3*delta)//2))
    K=q-q2+b
    Jfix=al+c0+n0*R+h['C'](l+1,2)+b*al
    JH=CHpair+b*(al+ex+l)
    er=C(r+1,2); Nall=a+1
    def pack(n,cap):
        return h['sp2'](max(0,n),ep0)<=2*cap
    checks={
      'WA_negative':WA<0,
      'LC_minus':3*(a+1)*q2+(a+17)*r<3*C(a+1,3),
      'LP_low':QA<=q2+r,
      'MAC_minus':WA<0,
      'LOC_LOW':UA-c0<=ep0,
      'COLD_MAC':UA-mac(QA-beta)<=0,
      'COVER':ex>=0 and C(cv,2)<=zeta,
      'FIX':fix<=-1,
      'DELTA':delta<=upper,
      'DELTA_PAIR':jlo<=ex and delta<=upper-2*(CH-CHpair),
      'RAW_FIXED':hh<=2*(K+Jfix)+2,
      'RAW_H0':(hh+delta)//2<=K+JH+1,
      'low_loop_range':3*L>=hh,
      'LOW_FIN':delta>=low,
      'W_negative_formal':wilf<0,
      'HOT_WINDOW':core<=rho+max(0,(hh-3*delta)//2),
      'ASR_HOT':WA+2*b*r+hot<0 and rho>=sr_base+hot+1+a+q2,
      'global_SP_Q':pack(a+1-cv,m),
      'global_PSP':h['H'](Nall)-4*er-9*(Nall*er+(r+1)*ep0+C(ep0,2))<=m,
      'joint_SP_Q':pack(al+R-cv,3*((3*delta+1)//2)-2),
      'joint_COUNT':C(al+R+2,3)-t<=3*((3*delta+1)//2)-2,
      'wide_SP_Q':pack(R-cv,3*delta-2),
      'wide_COUNT':C(R+2,3)-t<=3*delta-2,
      'short_SP_Q':pack(R-ex-cv,3*((delta+1)//2)-2),
      'short_COUNT':C(max(0,R-ex)+2,3)-t<=3*((delta+1)//2)-2,
      'pair_window':R*(R-1)<=2*delta-2+2*r*(r+1),
      'height':1<=L and 2*L+delta==hh and hh<=m,
    }
    # A full mixed face supplies one witness to MIX-PACK's existential
    # q_g/k_g tests, avoiding a growing q_g enumeration.
    dg=a+b; qg=C(dg+1,2)-r; gap=(dg+2)*qg-3*mac(qg)
    M=-WA-1
    eg=(D3+M-gap)//3
    zg=C(dg+2,3)-mac(qg)+eg-dg*r+C(r,2)
    eg0=min(eg,zg-C(cv,2))
    mixlower=max(h['cd'](h['sp2'](dg+1-cv,eg0),2),
       h['H'](dg+1)-4*er-9*((dg+1)*er+(r+1)*eg0+C(eg0,2)))
    mixupper=min(m,1+dg+C(dg+1,2)-r+mac(qg))
    checks.update(MIX_RANGE=gap<=min(M+2*(a-1)*r,D3+M),
       MIX_COVER=zg-max(0,t-a*r)>=C(cv,2),
       MIX_PACK=mixlower<=mixupper)
    return dict(N=N,B=B,LL=LL,RR=RR,checks=checks,
       failed=[s for s,ok in checks.items() if not ok],
       data=dict(a=a,alpha=al,b=b,r=r,n0=n0,l=l,t=t,epsilon=eps,
       R=R,E=ex,D3=D3,WA=WA,delta=delta,delta_low=low,
       delta_up=upper,fixed=fix,m=m,h=hh,L=L,W_formal=wilf,
       delta_pair_up=upper-2*(CH-CHpair),
       joint_excess_budget=ep0,hot_lower=hot))

if __name__=='__main__':
    for N in (480,960,1920,3840):
        for B,LL,RR in ((False,False,False),(True,False,False),
                        (False,True,False),(False,False,True)):
            print(json.dumps(check_profile(N,B,LL,RR)),flush=True)
