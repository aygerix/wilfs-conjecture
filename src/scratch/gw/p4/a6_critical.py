"""Necessary integer-count relaxation for a=6; execute only on fejer.
No bounded b enumeration is itself claimed as a proof for arbitrary b.
"""
from a4_stability import catalog,grow
from packing_fibers import bound,coverage_bound
from itertools import combinations_with_replacement
from collections import Counter
from math import comb
import json,argparse

def ceildiv(x,y):return -((-x)//y)
def P(d):return comb(d+3,3)
def H(d):return P(d)+2*comb(d+1,3)

def two_B_face(m,pd,t,t3,v2,v3,w,z):
    """For every compatible I3 BB shape, test its A+one-good-B face.
    Neighbor sets may be nested to maximize w. An overestimate of this
    maximum only weakens the bound on omitted cubics in that face.
    """
    if len(pd)>2:return False
    missing=list(pd)+[0]*(2-len(pd))
    pairs=[(0,0),(0,1),(1,1)]
    vcap=sum(comb(7-p,2) for p in missing)
    from itertools import combinations
    for shape in combinations(pairs,t3):
        shape=set(shape)
        wc=sum(6-max(missing[j],missing[k]) for j,k in shape)
        zc=0
        for triple in combinations_with_replacement(range(2),3):
            if all(pair in shape for pair in combinations(triple,2)):zc+=1
        if wc<w or zc<z:continue
        faces=[j for j in range(2) if missing[j]==0 and (j,j) in shape]
        if not faces:return False
        omitted=t+(vcap-v2-v3)+(wc-w)+(zc-z)
        if m>=coverage_bound(8,m,omitted):return False
    return True

def run(bmax):
    profiles=catalog(6);hist=Counter();survivors=[];groups=Counter()
    distributions=[()]+[(i,) for i in range(1,7)]+[(1,1),(1,2)]
    for q2,q3,u3,u4,k,WA in profiles:
        if q2+q3!=21:continue
        a=6;t=56-u3-u4;budget=-WA-1
        for b in range(bmax+1):
            B=comb(b+1,2);Z=comb(b+2,3);d=a+b
            for pd in distributions:
                if len(pd)>b:continue
                p=sum(pd);s3=a*b-p
                neighbor=sum(x*(4*a+3-3*x)//2 for x in pd)
                if neighbor+b*u3>budget:continue
                lost=sum(21-comb(a-x+1,2) for x in pd)
                missing=list(pd)+[0]*(b-len(pd))
                losses=sorted([max(missing[j],missing[k]) for j in range(b) for k in range(j,b)],reverse=True)
                suffix=[0]*(B+1)
                for j in range(B-1,-1,-1):suffix[j]=suffix[j+1]+losses[j]
                for lowlost in range(min(len(pd)*q2,lost)+1):
                    v2cap=b*q2-lowlost;v3cap=b*q3-lost+lowlost
                    if min(v2cap,v3cap)<0:continue
                    for rab in range(p+1):
                        if neighbor+b*u3+4*rab>budget:continue
                        for rbb in range(min(B,budget//4)+1):
                            for t4 in range(B-rbb+1):
                                q=rbb+t4;t3=B-q
                                wcap=min(a*t3-suffix[q],(b+1)*s3//2)
                                zcap=min(grow(t3,2),Z-b if q else Z)
                                if min(wcap,zcap)<0:continue
                                dwmin=a*t3+(b+1)*s3-3*wcap
                                dzmin=(b+2)*t3-3*zcap
                                fixed=p+b*u3+4*rab+4*rbb
                                dvmin=2*b*q2+b*q3+(a+1)*s3-4*v2cap-3*v3cap
                                if fixed+dvmin+dwmin+dzmin>budget:continue
                                for v2 in range(max(0,v2cap-budget//4),v2cap+1):
                                    vb=2*b*q2+b*q3+(a+1)*s3-4*v2
                                    for v3 in range(max(0,ceildiv(vb+fixed+dwmin+dzmin-budget,3)),min(v3cap,vb//3)+1):
                                        Dv=vb-3*v3
                                        for w in range(max(0,ceildiv(a*t3+(b+1)*s3+fixed+Dv+dzmin-budget,3)),wcap+1):
                                            Dw=a*t3+(b+1)*s3-3*w
                                            for z in range(max(0,ceildiv((b+2)*t3+fixed+Dv+Dw-budget,3)),zcap+1):
                                                Dz=(b+2)*t3-3*z
                                                S=fixed+Dv+Dw+Dz
                                                if S>budget:continue
                                                hist['critical_vectors']+=1
                                                r=t+(b*q2-v2)+(b*q3-v3)+(a*B-w)+(Z-z)
                                                quad=rab+rbb;m=P(d)-quad-r+k
                                                if m<H(a)-bound(a+1)*t:
                                                    hist['A_packing']+=1;continue
                                                if quad==0 and m<H(d)-bound(d+1)*r:
                                                    hist['global_packing']+=1;continue
                                                if quad==0 and m<coverage_bound(d+1,m,r):
                                                    hist['complete_support_packing']+=1;continue
                                                if quad:
                                                    forced=quad*d-comb(quad,2)
                                                    if r<forced:
                                                        hist['forced_cubic_count']+=1;continue
                                                    if d-quad>=1 and m<H(d-quad)-bound(d-quad+1)*(r-forced):
                                                        hist['delete_pair_endpoints']+=1;continue
                                                if b==2 and two_B_face(m,pd,t,t3,v2,v3,w,z):
                                                    hist['one_good_B_face']+=1;continue
                                                item=dict(profile=(q2,q3,u3,u4,k,WA),b=b,pd=pd,rab=rab,rbb=rbb,t4=t4,
                                                          lowlost=lowlost,v2=v2,v3=v3,w=w,z=z,S=S,m=m,r=r)
                                                survivors.append(item);groups[(q2,q3,u3,u4,k,WA,b,pd,rab,rbb,t4)]+=1
    result=dict(mode='a6_critical',bmax=bmax,counts=hist,survivor_count=len(survivors),
                survivor_group_count=len(groups),groups=[dict(key=key,count=value) for key,value in groups.items()],survivors=survivors)
    print(json.dumps(result),flush=True)
    with open('a6_critical.json','w') as f:json.dump(result,f,indent=2)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bmax',type=int,default=20);args=p.parse_args();run(args.bmax)
