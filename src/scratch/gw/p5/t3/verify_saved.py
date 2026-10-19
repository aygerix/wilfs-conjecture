"""Independent tuple verifier and deliberate boundary fixtures. fejer only."""
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
from collections import Counter
import json,sys

def make_fixtures():
    m,h=8,8
    o=dict(m=m,h=h,weights=[9,11,12,39],D=[[],[0],[0,0],[2],[0,2],[0,0,2],[1],[3]])
    Path('cold_mixed_minimal.json').write_text(json.dumps(o)+'\n')
    m,h=16000,4000;t=[400,600,3601,3604,3616,3664,3856]
    weights=[m+z for z in t]+[m+h]
    D=[()]+[(i,) for i in range(7)]+list(combinations_with_replacement(range(7),2))
    D+=[v for v in combinations_with_replacement(range(7),3) if sum(t[j] for j in v)>=h]
    D += [(7,),(0,7),(1,7),(0,0,7),(0,1,7),(1,1,7)]
    used={sum(weights[j] for j in v)%m for v in D}
    assert len(used)==len(D) and h-1 not in used
    for r in range(m):
        if r in used:continue
        j=len(weights);weights.append(3*m+h+(r-h)%m);D.append((j,))
    Path('a7_beta3.json').write_text(json.dumps(dict(m=m,h=h,weights=weights,D=D))+'\n')

def verify(path):
    o=json.loads(Path(path).read_text());m=o['m'];h=o['h'];n=o['weights'];d=len(n)
    D={tuple(sorted(x)) for x in o['D']};assert len(D)==len(o['D'])==m and () in D
    assert all((j,) in D for j in range(d)) and all(z>m for z in n)
    for x in D:
        assert all(x[:j]+x[j+1:] in D for j in range(len(x)))
    val={x:sum(n[j] for j in x) for x in D};M=max(val.values())
    assert M==4*m+h-1
    assert len({z%m for z in val.values()})==m
    ap=[0]*m
    for x,z in val.items():ap[z%m]=z
    cl=[(z+m-h)//m for z in n];assert all(1<=z<=4 for z in cl)
    a,b,c,e=[cl.count(j) for j in (1,2,3,4)]
    low={j for j in range(d) if cl[j]==1 and 2*(n[j]-m)<h}
    alpha=len(low);Aids={j for j in range(d) if cl[j]==1};L=min((n[j]-m for j in Aids),default=h)
    theta=(3*h+1)//2;HH=h-L
    def inside(r,th):return h<=r<th or 1<=r<th-m
    counts=Counter();JA=J=JH=JHA=JE=0;n0=beta=c0=u0=u1=k0=k1=0;links=Counter();qcold=0
    sr=set();hot=set();extra=set();bad={}
    for x,z in val.items():
        dg=len(x);tau=z-dg*m;band=(z+m-h)//m;r=z%m
        A=sum(cl[j]==1 for j in x);B=sum(cl[j]==2 for j in x);C=sum(cl[j]==3 for j in x);ll=sum(j in low for j in x)
        if dg==2 and A==2:counts['q2' if band==2 else 'q3']+=1
        if dg==3 and A==3:counts['u3' if band==3 else 'u4']+=1
        if dg==4:counts['k']+=1
        if dg==2 and A==1 and B==1:counts['s' if band==3 else 'S']+=1
        if dg==2 and B==2:counts['t' if band==3 else 'T']+=1
        if dg==2 and A==2 and band==2:
            if ll==2:n0+=1;beta+=tau<theta-h;qcold+=inside(r,theta)
            else:
                for j in x:
                    if j in low:links[j]+=1
        c0+=dg==3 and ll==3
        if dg==3 and A==3 and band==3:
            if ll==3:u0+=1
            else:u1+=1
        if dg==4:
            if ll==4:k0+=1
            else:k1+=1
        allowed=(dg==1 and not A) or (dg==2 and A==2 and band==3) or (dg==2 and A==1 and B==1 and band==4) or (dg==2 and B==2 and band==4)
        bad[r]=not allowed
        if not allowed and inside(r,theta):J+=1;JA+=A==dg
        if not allowed and inside(r,h+HH):JH+=1;JHA+=A==dg
        if not allowed and inside(r,2*h-1):JE+=1
        if dg==2 and ((B==2 and band==3) or (B==1 and C==1)):sr.add(x)
        if dg==3 and A==2 and B==1:
            aa=sum(n[j] for j in x if cl[j]==1)
            if (aa+m-h)//m==3:sr.add(x)
        if dg==3 and ((A==1 and B==2) or B==3):sr.add(x)
        if dg==3 and A==3 and tau>=2*h:hot.add(x)
        if (dg==0 or A==dg and tau<h) and tau>=max(0,2*h-m):extra.add(x)
    q2,q3,u3,u4,k=(counts[z] for z in ('q2','q3','u3','u4','k'))
    q=q2+q3;Q=comb(a+1,2);ra=Q-q;D3=(a+2)*q-3*(u3+u4);LC=(a+1)*(q2+u3)-4*k
    WA=3*a*(a+1)+(a-3)*q-4*(u3+u4)+LC
    W=d*sum((M-z)//m for z in val.values())-sum(z//m for z in val.values())
    G=c*(c+e+1)+e*(3*a+2*b-1)+(c+e)*(q3+counts['s']+counts['t'])
    Trans=a*b-counts['s']+c*(c+1)+e*(3*a+2*b+c)+(c+e)*(2*q2+q3+counts['s']+counts['t']+u3)+b*u3
    phi=D3+a-1-2*alpha-2*c0+(2*alpha+1-a)*n0+sum(z*(a+2-z) for z in links.values())+(a+1)*u0-5*k0+(a+3)*u1-3*k1+b*(a-1+q2+u3-2*alpha-2*n0)+G+(c+e)*(2*q2+u3)-2*alpha*c
    assert not(sr&hot or sr&extra or hot&extra)
    assert len(sr)+len(hot)+len(extra)<=m-h
    assert W>=WA+Trans+len(hot)+len(extra)
    eta=min(3*max(0,h-2*L),2-h+2*JE) if h>=2 else 0
    A2=(a-1)*(b+1)+G+LC+b*u3+(c+e)*(2*q2+u3)+D3
    if a>=3:assert W>=A2-max(0,eta-(b+2)*q2-k)
    P=a-1+LC+2*q2+k-2*JA;PH=a-1+LC+2*q2+k+h-2*L-2*JHA
    if a>=7 and alpha==2:
        assert P>=2-2*a
        if ra and q>=2:assert D3>=2*a-2 and P+D3>=0
        l=sum(links.values())
        if not ra and l<=1:
            R=sum(n[j]-m<theta-2*L for j in Aids-low);nn=max(0,R-l)
            assert nn*(nn-1)<=h-2*L-1
            assert P+D3>=4*a-4+(a+1)*l-6*R
            assert PH>=h-2*L-(2*a-2)-(3*a-5)*l
        assert W>=0
    if alpha==3 and a>=13 and ra<=2:
        l=sum(links.values());R=sum(n[j]-m<theta-2*L for j in Aids-low);delta=h-2*L
        tt=comb(a+2,3)-u3-u4;forced=[0,a,2*a-1][ra];local=tt-forced;assert local>=0
        def L2(s):
            if s<=1:return 0
            if s<=4:return [0,0,2,4,8][s]
            return 3*s if s%3==0 else 3*(s-1)
        for s,w in ((max(0,R-l-2*ra),(delta+1)//2),(max(0,R-ra),delta)):
            assert 2*(3*w-2)>=2*s*(comb(s,2)+1)-L2(s)*local
    assert W>=0
    smallgens=[z for z in n if z<M-m+1]
    apery_closed=all(ap[(r+z)%m]<=ar+z for z in smallgens for r,ar in enumerate(ap))
    minimal=None
    if apery_closed:
        small_ap=[z for z in ap if 0<z<M-m+1]
        minimal=all(not any(z-ar>0 and ap[(z-ar)%m]<=z-ar for ar in small_ap if ar<z) for z in n)
    if Path(path).name.startswith('semigroup_'):assert apery_closed and minimal
    result=dict(file=path,m=m,h=h,a=a,b=b,c=c,e=e,alpha=alpha,q2=q2,q3=q3,u3=u3,u4=u4,k=k,r_A=ra,D3=D3,LC=LC,WA=WA,W=W,J=J,JA=JA,P=P,P_plus_D3=P+D3,PH=PH,beta=beta,l=sum(links.values()),eta_end=eta,X_SR=len(extra),Phi=phi,apery_closed=apery_closed,minimal_units=minimal,A_offsets=sorted(n[j]-m for j in Aids))
    print(json.dumps(result,sort_keys=True),flush=True)
    dat=Path(path).with_suffix('.dat')
    with dat.open('w') as f:
        f.write(f'{m} {d}\n'+' '.join(map(str,n))+'\n')
        for x in sorted(D):f.write(str(len(x))+' '+ ' '.join(map(str,x))+'\n')
    return result

if __name__=='__main__':
    args=sys.argv[1:]
    if '--fixtures' in args:make_fixtures();args.remove('--fixtures');args+=['cold_mixed_minimal.json','a7_beta3.json']
    for path in args:verify(path)
