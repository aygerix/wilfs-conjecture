#!/usr/bin/env python3
"""Exact checks of two explicit unbounded e=5 families and algebra constants."""
import json,math
from fractions import Fraction as F
from boundary import apery,check,stats

def support_two(N):
    m=N*N+N+1;a=2*m-N;b=a-1
    A=(N,0);B=(N-1,N)
    ga=N*a-m;gb=(N-1)*a+N*b-m
    gens=[a,b,ga,gb]
    D={(x,y,0,0) for x in range(N+1) for y in range(N+1) if not(x==N and y>=1) and (x,y) not in [A,B]}
    D|={(0,0,1,0),(0,0,0,1)}
    actual=apery(m,gens)
    assert actual is not None
    DD,w=actual;assert D==DD
    H,t,n=check(D)
    c=max(w)-m+1;assert c==(4*N-4)*m-2*N*N+1
    assert (c+m-1)==gb and (c+m-1)+sum(gens)<6*(sum(gens)+m-1)
    ell=c-sum((v-r)//m for r,v in enumerate(w))
    assert 5*ell-c>=0
    assert 2*(a-m)>m
    return dict(N=N,m=m,q=(c+m-1)//m,height=max(map(sum,D)),W=5*ell-c,H=H,t=t)

def spike_box(N):
    m=N**3;core=[2*m-1,2*m-N,2*m-N*N]
    M=(N-1)*sum(core);g=M-m
    D={(a,b,c,0) for a in range(N) for b in range(N) for c in range(N) if (a,b,c)!=(N-1,)*3}
    D.add((0,0,0,1))
    actual=apery(m,core+[g]);assert actual is not None
    DD,w=actual;assert D==DD
    H,t,n=check(D);c=max(w)-m+1;assert c==M-2*m+1
    assert sum(core+[g])>=c+m
    ell=c-sum((v-r)//m for r,v in enumerate(w));assert 5*ell-c>=0
    return dict(N=N,m=m,q=(c+m-1)//m,height=max(map(sum,D)),W=5*ell-c,H=H,t=t)

def balanced_L(N):
    m=N*(N+2);a=2*m-N-1;b=2*m-1
    ga=(4*N-4)*m+1;gb=ga+N
    D={(x,y,0,0) for x in range(N+1) for y in range(N+1)
       if (x,y) not in [(N,N),(N,N-1),(N-1,N)]}
    D|={(0,0,1,0),(0,0,0,1)}
    ap=apery(m,[a,b,ga,gb]);assert ap is not None
    DD,w=ap;assert DD==D
    H,t,n=check(D);c=max(w)-m+1
    assert c==(4*N-5)*m+N+2 and a+b+ga>=c+m
    ell=c-sum((v-r)//m for r,v in enumerate(w))
    W=5*ell-c;assert W==(6*N-15)*m+14*N+13
    assert W>=0 and 2*(a-m)>m
    return dict(N=N,m=m,q=(c+m-1)//m,height=max(map(sum,D)),W=W,H=H,t=t,
                LKYZ=8*(N-1)**2,LKYZ_covers=5*8*(N-1)**2>=c)

def algebra():
    # P(12+u), with sqrt(12) replaced by 52/15 in its negative terms.
    c=[F(39),-F(468,5),F(87,2),-F(104,5),F(3,2)]
    out=[sum(c[j]*math.comb(j,i)*12**(j-i) for j in range(i,5)) for i in range(5)]
    assert out==[F(1707,5),F(11664,5),F(5907,10),F(256,5),F(3,2)]
    assert F(9,16)>F(9,11)**3
    assert F(81,32)<F(11,8)**3
    assert F(1,1000)+F(7,60)+F(3,8)<F(1,2)
    print(json.dumps(dict(polynomial=[str(x) for x in out],boundary_constants='exact OK')))

if __name__=='__main__':
    algebra()
    for N in range(3,41):print(json.dumps(dict(family='support_two',**support_two(N))))
    for N in range(3,41):print(json.dumps(dict(family='balanced_L',**balanced_L(N))))
    for N in [4,8,12,24]:print(json.dumps(dict(family='spike_box',**spike_box(N))))
