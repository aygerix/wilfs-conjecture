"""Replay a surviving count profile, not a tile; execute only on fejer."""
from pathlib import Path
ns={}
exec(Path('frontier_counts.py').read_text().split('amin=')[0],ns)
C,H,L2,cover,sp2,mixpack=(ns[k] for k in ('C','H','L2','cover','sp2','mixpack'))
a,al,r,n0,l,t,u,k,c0,beta,R,b,de=17,7,4,28,0,80,0,0,84,0,10,0,247
Q=C(a+1,2);q=Q-r;tf=C(a+2,3)-ns['mac'](q);ep=t-tf
D3=3*t-(a+2)*r;WA=-C(a+1,3)+(a+1)*n0-(a-3)*r+4*t
mm=C(a+3,3)-r-t;zt=t-a*r+C(r,2);er=C(r+1,2)
E=min(a-al,l+r);CH=al+n0+c0+l+E+C(E+2,3)+(n0+al*E)*(a-al)
bf=a-1+n0-2*al-2*beta
bh=a-1+n0-2*(al+E+l)
fix=a-1-2*al-2*beta-2*c0+(a+3)*n0+D3-2*n0*R
upper=2*CH-(a-1)-(a+3)*n0-D3-b*bh-1
low=ns['cd']((a-1)*(b+1)+(a+1)*n0+D3+(b+2)*n0+1,3)
assert fix+b*bf<0 and low<=de<=upper
cv0=4;ek=min(ep,zt-C(cv0,2));nn=a+1-cv0
assert ns['cd'](sp2(nn,ek),2)<=mm
sj=(3*de+1)//2;ss=(de+1)//2
nj=al+R-cv0;nw=R-cv0;ns0=max(0,R-l-r-cv0)
assert H(nj)<=3*sj-2 and H(nw)<=3*de-2 and H(ns0)<=3*ss-2
assert mixpack(a,b,r,q,n0,t,u,k,WA,0,D3)
print(dict(kind='relaxed count vector, NOT an actual residue-complete instance',a=a,alpha=al,r=r,n0=n0,l=l,t=t,eps=ep,c0=c0,beta=beta,R=R,b=b,delta=de,m=mm,WA=WA,D3=D3,kcover=cv0,legal_defect=ek,global_SP=ns['cd'](sp2(nn,ek),2),joint_H=H(nj),joint_capacity=3*sj-2,delta_bounds=[low,upper],fixed_payment=fix))
assert ns['mac'](118)==651
assert -C(18,3)-14*35+4*318==-34
assert min(2*35,2*17-35)==-1
for rr,tt,em,mp in ((4,80,18,1056),(5,85,10,1050),(5,86,11,1049)):
    bounds=[]
    for kk in range(1,rr):
        ek=em-C(kk,2);bound=ns['cd'](sp2(18-kk,ek),2)
        assert bound>mp
        bounds.append(bound)
    print(dict(matching_forced=dict(r=rr,t=tt,m=mp),smaller_cover_lower_bounds=bounds))
for rr,tt,mp,wa,vl,dm,expected in ((4,80,1056,-48,12,247,283),(5,85,1050,-42,0,246,277),(5,86,1049,-38,1,247,276)):
    core=min(C(10-ee+2,3)-(10-ee)*(rr-ee)-vl for ee in (0,1))
    hm=mp+wa+1
    assert core>mp-hm
    du=(2*mp-hm-2*core)//3
    assert du==expected
    print(dict(hot_window=dict(r=rr,t=tt,m=mp),core_min=core,h_min=hm,delta=[dm,du]))
for rr,tt,cc,lower,expected in ((4,80,84,247,201),(5,85,84,246,205),(5,86,83,247,200),(5,86,84,247,202)):
    ch=7+28+cc+1+C(3,3)+(28+7)*10
    dg=3*tt-19*rr
    upper=2*ch-16-20*28-dg-1
    assert upper==expected and upper<lower
    print(dict(E_REPAIR_exclusion=dict(r=rr,t=tt,c0=cc),delta_lower=lower,delta_upper=upper))
