"""JOINT-SP and missing-pair packing audit. Run on fejer only.

Uses local LP on the high window in addition to the proved arc bounds.
Not an enumeration of semigroups. All arithmetic is integral.
"""
from math import comb
from collections import Counter
import json,sys
amin=int(sys.argv[1]) if len(sys.argv)>1 else 13
assert amin in (13,14)
def H(n):return n*(n*(n-1)//2+1)
def L2(n):
    if n<=1:return 0
    if n<=4:return [0,0,2,4,8][n]
    return 3*n if n%3==0 else 3*(n-1)
def ceildiv(n,d):return -((-n)//d)
rows=[];survivors=[];after_partial=[]
for a in range(amin,41):
    num=Counter();ss=[]
    for r in range(3):
        for l in range(5-2*r):
            stars=l*(a+2-l)
            for n0 in range(6-r,7):
                q2=n0+l;LC=(a+1)*q2
                tmin=[0,a,2*a-1][r]
                tmax=min((comb(a+1,3)-LC+(a-3)*r-1)//4,
                         (5*a-16-stars+(a+2)*r)//3)
                for t in range(tmin,tmax+1):
                    D3=3*t-(a+2)*r
                    local=t-tmin
                    for R in range(a-2):
                        fixed=max(15-5*a+stars+D3,
                            a-27+(a+3)*n0+stars-2*n0*R-(a+2)*r,
                            a-39+(a+3)*n0+stars-2*n0*R+D3)
                        if fixed>=0:continue
                        bf=max(1,a-7-n0+l) if a==13 else a-7-n0+l
                        assert bf>0
                        e=l+r;p=a-3
                        B=2*(13+n0+l+e+comb(e+2,3)+(n0+3*e)*p)-(a-1)-(a+3)*(n0+l)
                        bh=a-7-n0-3*l-2*r
                        nn=max(0,R-l-r);npair=max(0,R-l-2*r)
                        dmin=max(1,nn*(nn-1)+1-2*r*(r+1),
                            2*ceildiv(2*H(npair)-L2(npair)*local+4,6)-1,
                            2*ceildiv(comb(nn+2,3)-t+2,3)-1,
                            ceildiv(2*H(max(0,R-r))-L2(max(0,R-r))*local+4,6),
                            ceildiv(comb(R+2,3)-t+2,3),
                            ceildiv(R*(R-1)+2-2*r*(r+1),2))
                        nj=max(0,3+R-r)
                        dmin=max(dmin,ceildiv(2*ceildiv(2*H(nj)-L2(nj)*local+4,6)-1,3),
                            ceildiv(2*ceildiv(comb(3+R+2,3)-t+2,3)-1,3))
                        for b in range((-fixed-1)//bf+1):
                            dmax=B-D3-b*bh-1
                            num['profiles']+=1
                            if dmin<=dmax:
                                num['survive']+=1
                                z=dict(a=a,r=r,l=l,n0=n0,t=t,R=R,b=b,delta=[dmin,dmax],fixed=fixed)
                                ss.append(z)
                                # All new survivors have R=a-3: use all a offsets.
                                assert R==a-3
                                if r==1:
                                    eps=t-a
                                    lower=H(a)-4-9*(a+2*eps+comb(eps,2))
                                elif r==2 and t==2*a-1:
                                    # Two missing pairs share a factor; at most three
                                    # nontrivial collisions between their translates.
                                    lower=H(a)-12-9*(2*a+2)
                                elif r==2:
                                    # Covers disjoint pairs (eps=0) and intersecting
                                    # pairs (eps=t-(2a-1)) simultaneously here.
                                    eps=t-(2*a-1)
                                    lower=min(H(a)-12-9*(3*a),
                                        H(a)-12-9*(2*a+2+3*eps+comb(eps,2)))
                                else:
                                    raise AssertionError(z)
                                z['partial_lower']=lower
                                z['joint_span_max']=3*((3*dmax+1)//2)-2
                                z['cold_lower']=a-27+(a+3)*n0+stars-2*n0*R+D3
                                assert z['cold_lower']>=0
                                if lower<=z['joint_span_max']:after_partial.append(z)
    rows.append(dict(a=a,**num))
    survivors.extend(ss)
with open('joint_profiles_survivors.json','w') as f:json.dump(survivors,f,indent=2)
hh=1469598103934665603;expanded=0
for z in survivors:
    expanded+=z['delta'][1]-z['delta'][0]+1
    for k in ('a','r','l','n0','t','R','b'):
        hh=((hh^z[k])*1099511628211)&((1<<64)-1)
    for v in z['delta']:hh=((hh^v)*1099511628211)&((1<<64)-1)
assert all(not z.get('survive',0) for z in rows if z['a']>=14)
assert not after_partial
print(json.dumps(dict(amin=amin,rows=rows,total_profiles=sum(z.get('profiles',0) for z in rows),
    profiles_a_ge16=sum(z.get('profiles',0) for z in rows if z['a']>=16),
    total_survivors=len(survivors),expanded=expanded,hash=hh,
    max_b=max((z['b'] for z in survivors),default=0),
    max_d=max((z['a']+z['b'] for z in survivors),default=0),
    max_m_bound=max((comb(z['a']+z['b']+3,3)+comb(z['a']+3,4) for z in survivors),default=0),
    first=survivors[:30])),flush=True)
