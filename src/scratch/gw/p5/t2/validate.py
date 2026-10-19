"""Independent validation of saved actual completions; fejer only."""
import json,itertools as it
from pathlib import Path
from math import comb,isqrt

def validate(path):
    data=json.loads(Path(path).read_text());m=data['m'];h=data['h'];a=data['a'];n=tuple(data['weights']);core=data['cells'];d0=len(n)
    D={tuple(x.count(j) for j in range(d0)) for x in core}
    seen={sum(x*y for x,y in zip(v,n))%m for v in D}
    extra=tuple(3*m+h+(r-h)%m for r in range(m) if r not in seen)
    D={x+(0,)*len(extra) for x in D};n+=extra;d=len(n)
    D.update(tuple(int(j==k) for j in range(d)) for k in range(d0,d))
    assert len(D)==m and all(v>m for v in n)
    V={x:sum(v*w for v,w in zip(x,n)) for x in D};assert len({v%m for v in V.values()})==m
    for x in D:
        for j in range(d):
            if x[j]:assert x[:j]+(x[j]-1,)+x[j+1:] in D
    M=max(V.values());assert M==4*m+h-1
    cl=[(v+m-h)//m for v in n];aa,b,c,e=[cl.count(i) for i in range(1,5)];assert aa==a
    ct={};J=JA=hot=SR=0;theta=(3*h+1)//2
    for x,v in V.items():
        typ=tuple(i for j,i in enumerate(cl) for _ in range(x[j]));band=(v+m-h)//m
        ct[typ,band]=ct.get((typ,band),0)+1
        dg=sum(x);tau=v-dg*m;rr=v%m
        inside=(h<=rr<min(theta,m)) or (1<=rr<theta-m)
        allowed=(dg==1 and typ!=(1,)) or (typ==(1,1) and band==3) or (typ in {(1,2),(2,2)} and band==4)
        if inside and not allowed:J+=1;JA+=all(k==1 for k in typ)
        hot+=typ==(1,1,1) and tau>=2*h
    def count(typ,band):return ct.get((typ,band),0)
    q2=count((1,1),2);q3=count((1,1),3);u3=count((1,1,1),3);u4=count((1,1,1),4);k=count((1,1,1,1),4);s=count((1,2),3);t=count((2,2),3)
    ell=sum((M-v)//m for v in V.values());g=sum(v//m for v in V.values());W=d*ell-g
    LC=(a+1)*(q2+u3)-4*k;ra=comb(a+1,2)-q2-q3;ta=comb(a+2,3)-u3-u4;D3=3*ta-(a+2)*ra
    T=a*b-s+c*(c+1)+e*(3*a+2*b+c)+(c+e)*(2*q2+q3+s+t+u3)+b*u3
    WA=-comb(a+1,3)+LC-(a-3)*ra+4*ta
    p=sum(cl[j]==1 and 3*(n[j]-m)>=2*h for j in range(d))
    assert W>=WA+T+hot
    uniform=LC+comb(p+2,3)-comb(a+1,3)+5*ra+D3+T
    assert W>=uniform
    L=min(n[j]-m for j in range(d) if cl[j]==1);delta=max(0,h-2*L);alpha=sum(cl[j]==1 and 2*(n[j]-m)<h for j in range(d))
    G=c*(c+e+1)+e*(3*a+2*b-1)+(c+e)*(q3+s+t)
    Mq=a*b-count((1,2),3)-count((1,2),4)+comb(b+1,2)-count((2,2),3)-count((2,2),4)
    Cdef=D3+4*Mq+3*(a*c-count((1,3),4))+3*(b*c-count((2,3),4))
    eta=min(3*delta,2*J);high_arcs=[]
    for H in sorted({n[j]-m for j in range(d) if cl[j]==1 and 2*(n[j]-m)>=h}):
        th=h+H;JH=0;K=0
        for x,v in V.items():
            typ=tuple(i for j,i in enumerate(cl) for _ in range(x[j]));band=(v+m-h)//m;dg=sum(x);rr=v%m
            allowed=(dg==1 and typ!=(1,)) or (typ==(1,1) and band==3) or (typ in {(1,2),(2,2)} and band==4)
            K+=allowed
            if ((h<=rr<min(th,m)) or (1<=rr<th-m)) and not allowed:
                JH+=1
                assert any(x[j] and cl[j]==1 and n[j]-m<H for j in range(d))
        assert H<=K+JH+1
        loss=h-2*H+2*JH;eta=min(eta,loss);high_arcs.append([H,JH,loss])
    R=(a-1)*(b+1)+G+LC+b*u3+(c+e)*(2*q2+u3)+Cdef-max(0,eta-(b+2)*q2-k)
    assert W>=R
    if alpha==1 and a>=6:assert 2*JA<=a-1+LC+2*q2+k
    print(json.dumps(dict(path=str(path),m=m,h=h,a=a,b=b,c=c,e=e,alpha=alpha,W=W,WA=WA,q2=q2,q3=q3,u3=u3,u4=u4,k=k,delta=delta,J=J,JA=JA,hot=hot,D3=D3,T=T,eta=eta,high_arcs=high_arcs,new_lower=R,high_lower=uniform)),flush=True)

def relaxation():
    a=12;m=455;h=317;t=[106]*4+[257]*8
    n=[m+x for x in t];D=[x for deg in range(4) for x in it.combinations_with_replacement(range(a),deg)]
    vals=[sum(n[j] for j in x) for x in D];M=max(vals);assert len(D)==m and M==4*m+h-1
    ell=sum((M-v)//m for v in vals);g=sum(v//m for v in vals)
    assert a*ell-g==-104
    bandW=(a+1)*(ell-4)-4*(m-a-1)+(m-h);assert bandW==-18
    print(json.dumps(dict(relaxation='full cubic, two weight levels',a=a,m=m,h=h,t=t,ell=ell,g=g,actual_P4_slack=a*ell-g,band_expression=bandW,distinct_residues=len({v%m for v in vals}))),flush=True)
    n=[m+x for x in list(range(106,110))+list(range(250,258))]
    vals=[sum(n[j] for j in x) for x in D];M=max(vals)
    ell=sum((M-v)//m for v in vals);g=sum(v//m for v in vals)
    assert a*ell-g==-104 and len(n)==len(set(n))
    print(json.dumps(dict(relaxation='same phase, distinct weights',distinct_residues=len({v%m for v in vals}),P4_slack=a*ell-g)),flush=True)
    # False pure-payment extension for a>=7, with exact maximum scale.
    from arc_intruders import evaluate
    A=7;T=[2,2]+[3]*5;DD={x for deg in range(1,4) for x in it.combinations_with_replacement(range(A),deg)}
    out=evaluate(T,5,5,DD);assert out['slack']==-6
    print(json.dumps(dict(false_unrestricted_payment=out)),flush=True)
    first=None
    for mm in range(2,6):
        for HH in range(1,mm):
            hh=3*HH-mm+1
            if not(1<=hh<=mm and HH<hh):continue
            for LL in range(1,HH):
                if not(2*LL<hh<=2*HH):continue
                for al in range(2,A):
                    out=evaluate([LL]*al+[HH]*(A-al),mm,hh,DD)
                    if out['slack']<0 and first is None:first=out
    assert first['m']==5 and first['h']==5 and first['t']==T
    print('Smallest scale in the a=7 full-cubic two-level exact-maximum family: m=5.')

if __name__=='__main__':
    relaxation()
    if Path('tile_best.json').exists():validate('tile_best.json')
