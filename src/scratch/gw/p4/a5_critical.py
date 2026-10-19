"""Exact count relaxation for the a=5 proof, executed only on fejer.
Tests every nonnegative count vector surviving the proof inequalities
for b in the given finite range. It does not assert that such vectors
are realized by down-sets. Every surviving vector is excluded by one
of the explicitly recorded packing inequalities.
"""
from a4_stability import catalog
from math import comb
from collections import Counter
import argparse
import json


def ceildiv(x,y):return -((-x)//y)
def P(d):return comb(d+3,3)
def H(d):return P(d)+2*comb(d+1,3)


def test(last):
    profiles=catalog(5);hist=Counter();survivors=[]
    for q2,q3,u3,u4,k,WA in profiles:
        if q2+q3!=15:continue  # the one-missing-AA case is separate
        a=5;t=35-u3-u4;budget=-WA-1
        for b in range(last+1):
            B=comb(b+1,2);Z=comb(b+2,3);d=a+b
            for p in range(3):
                if p and not b:continue
                if p==2 and q2:continue
                # All critical missing AB neighbors are in one B direction.
                s3=a*b-p
                if s3<0:continue
                for lowlost in (range(q2+1) if p==1 else [0]):
                    lv=0 if p==0 else (a if p==1 else 2*a-1)
                    v2cap=q2*b-lowlost
                    v3cap=q3*b-lv+lowlost
                    if v2cap<0 or v3cap<0:continue
                    for rab in range(p+1):
                        for rbb in range(min(B,budget//4)+1):
                            for t4 in range(B-rbb+1):
                                t3=B-rbb-t4
                                # ABB neighbor stability, as proved in text.
                                L=max(0,b-(B-t3)) if p else 0
                                wcap=min(a*t3,(b+1)*s3//2,a*t3-p*L)
                                zcap=min(Z-b if B>t3 else Z,(b+2)*t3//3)
                                if wcap<0 or zcap<0:continue
                                for v2 in range(max(0,v2cap-budget//4-1),v2cap+1):
                                    baseDv=2*b*q2+b*q3+(a+1)*s3-4*v2
                                    v3lo=max(0,ceildiv(baseDv-budget,3))
                                    v3hi=min(v3cap,baseDv//3)
                                    for v3 in range(v3lo,v3hi+1):
                                        Dv=baseDv-3*v3
                                        for w in range(max(0,ceildiv(a*t3+(b+1)*s3-budget,3)),wcap+1):
                                            Dw=a*t3+(b+1)*s3-3*w
                                            if Dw<0:continue
                                            zlo=max(0,ceildiv((b+2)*t3-budget,3))
                                            for z in range(zlo,zcap+1):
                                                Dz=(b+2)*t3-3*z
                                                if Dz<0:continue
                                                S=p+b*u3+4*rab+4*rbb+Dv+Dw+Dz
                                                if S>budget:continue
                                                hist['critical_vectors']+=1
                                                assert rab+rbb<=1
                                                r=t+(q2*b-v2)+(q3*b-v3)+(a*B-w)+(Z-z)
                                                m=P(d)-rab-rbb-r+k
                                                assert m>0
                                                # Cubic packing in A itself.
                                                if 2*(H(a)-m)>3*(a+1)*t:
                                                    hist['A_face_packing']+=1;continue
                                                # Full-pair packing on all directions.
                                                if rab+rbb==0 and 2*(H(d)-m)>3*(d+1)*r:
                                                    hist['global_packing']+=1;continue
                                                # Delete an endpoint of the sole missing pair.
                                                if rab+rbb==1:
                                                    extra=r-d
                                                    assert extra>=0
                                                    if 2*(H(d-1)-m)>3*d*extra:
                                                        hist['deleted_variable_packing']+=1;continue
                                                survivors.append(dict(profile=(q2,q3,u3,u4,k,WA),b=b,p=p,rab=rab,rbb=rbb,t4=t4,v2=v2,v3=v3,w=w,z=z,S=S,m=m,r=r))
    print(json.dumps(dict(mode='critical_a5',bmax=last,counts=hist,survivors=survivors[:20],survivor_count=len(survivors))),flush=True)
    assert not survivors


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bmax',type=int,default=20);args=p.parse_args();test(args.bmax)
