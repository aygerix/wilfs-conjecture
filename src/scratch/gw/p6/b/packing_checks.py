"""Actual core+spike tiles: P6b packing, shadow, flat-window payments.
fejer only, nice single core. All witnesses and phase slacks use integers.
"""
from itertools import combinations_with_replacement as cwr
from collections import Counter
from math import comb
from pathlib import Path
import random,json,sys

seed=int(sys.argv[1]) if len(sys.argv)>1 else 2026101991
trials=int(sys.argv[2]) if len(sys.argv)>2 else 1200
rng=random.Random(seed);stats=Counter();saved=[];worst=None;unpaid=[]
def divisors(y):return {y[:j]+y[j+1:] for j in range(len(y))}
def phi(y,P,m):return sum(P[a] for a in y)%m
def cover(E,k):
    # Iterate subsets by cardinality; loops force their vertex.
    for mask in sorted(range(1<<k),key=int.bit_count):
        if all(any(mask>>a&1 for a in z) for z in E):return {a for a in range(k) if mask>>a&1}
    raise AssertionError('cover')
def check(C,P,m,name=None):
    global worst
    C=set(C);k=len(P);assert () in C and all((a,) in C for a in range(k))
    assert all(divisors(y)<=C for y in C if y)
    lab={x:phi(x,P,m) for x in C};assert len(set(lab.values()))==len(C)
    N={x for x in C if any(tuple(sorted(x+(a,))) in C for a in range(k))};A=C-N
    assert all((a,) in N for a in range(k))
    Q={x for x in C if len(x)==2};T={x for x in C if len(x)==3};N2=Q&N
    q=len(Q);t=len(T);p=len(N2);a=q-p;s=m-len(C);d=k+s;assert s>=0
    J=comb(1+k+p,2);B=a+2*t
    cr=(d+1)*J-B*(m-1)+t*(t-1)+a*t+a*(a-1)//2
    fc=s*comb(k,2)+(d+2)*comb(p,2)-3*t*(m-1)+t*(t-1)
    allQ=set(cwr(range(k),2));missing=allQ-Q;bad=allQ-N2;j=len(bad)
    r=comb(k+2,3)-t
    assert k*j<=3*r and k*j-j*(j-1)//2<=r
    if k<=8:
        cv=cover(bad,k);assert k*len(cv)<=r;stats['SHADOW_COVER']+=1
    if k<=10:gone=cover(missing,k)
    else:
        gone=set();left=set(missing)
        while left:
            v=max(range(k),key=lambda a:sum(a in z for z in left));gone.add(v)
            left={z for z in left if v not in z}
    I=set(range(k))-gone;h=len(I)
    pack=0
    if h>=2:
        vals={0};AI=[-1,*sorted(I)]
        pp=lambda a:0 if a==-1 else P[a]
        base=[(pp(a)-pp(b))%m for a in AI for b in AI if a!=b]
        assert len(set(base))==h*(h+1) and 0 not in base;vals.update(base)
        FQ=[z for z in cwr(sorted(I),2) if all(tuple(sorted(z+(v,))) in T for v in I)]
        nf=0
        for z in FQ:
            for c in AI:
                if c not in z:
                    x=(phi(z,P,m)-pp(c))%m
                    assert x not in vals,dict(name=name,P=P,m=m,C=sorted(C),I=sorted(I),z=z,c=c)
                    vals.add(x);nf+=1
        pack=1+h*(h+1)+nf
        rr=comb(h+2,3)-sum(set(y)<=I for y in T)
        assert pack==len(vals)<=m and pack>=(h**3+2*h*h+3*h+2)//2-3*(h-1)*rr
        stats['SIGNED_PACK']+=1
        stats['SIGNED_PACK_mod3']+=m%3==0
    if not missing:
        assert m>=k*k+k+1
        if k>=3 and r<=k*k//9:assert cr>=0;stats['DENSE9']+=1
        if t==1:assert k<=4 or fc>=0;stats['ONE_CUBIC']+=1
        if k>=19 and t<=k*k//16:assert fc>=0;stats['FEW_CUBIC']+=1
    if k>=3 and r<=3*k*k//40:assert cr>=0;stats['DENSE075']+=1
    # Min-phase lemma: every worst phase has zero cell non-maximal. This is
    # an exact all-phase test even if an integer B3 example has huge modulus.
    sigmas=range(m) if m<=500 else sorted({lab[x] for x in N})
    deg=[sum(z.count(v) for z in Q) for v in range(k)]
    mn=None;minsigma=None
    for sig in sigmas:
        R={x:(lab[x]-sig)%m for x in C};r0=R[()]
        S=(d+1)*sum(R[x] for x in N)-sum((len(x)-1)*R[x] for x in A)
        if S<0:
            out=dict(name=name,C=sorted(C),P=P,m=m,d=d,sigma=sig,S=S)
            Path('MAXCL_COUNTEREXAMPLE.json').write_text(json.dumps(out,indent=2)+'\n')
            print('MAXCL_COUNTEREXAMPLE',out,flush=True);raise SystemExit(2)
        assert S>=cr and S>=fc
        K={z:(sum(R[(v,)] for v in z)-r0-R[z])//m for z in Q}
        b=sum(K[z]<0 for z in Q);pos=sum(K[z]>0 for z in Q)
        assert b<=r0
        U=sum((d+1-deg[v])*R[(v,)] for v in range(k))
        F=U-t*r0+(d+2)*sum(R[z] for z in N2)-2*sum(R[y] for y in T)+m*(r0-b+pos)
        assert S==F
        if mn is None or S<mn:mn=S;minsigma=sig
        stats['phase_checks']+=1
    stats['tiles']+=1;stats['height3_tiles']+=bool(T);stats['CR']+=cr>=0;stats['FLAT_CR']+=fc>=0
    stats['large_modulus_minphase']+=m>500
    if cr<0 and fc<0 and k>=4 and d>=6:
        stats['BOTH_BOUNDS_FAIL']+=1
        if len(unpaid)<5:
            sig=minsigma;R={x:(lab[x]-sig)%m for x in C};r0=R[()]
            KK={z:(sum(R[(v,)] for v in z)-r0-R[z])//m for z in Q}
            PZ=all(KK[z]==0 for z in N2) and all(KK[z]>=0 for z in Q-N2)
            CP=m-r0<=d+1 and all(KK[z]==-1 for z in N2)
            unpaid.append(dict(P=P,m=m,C=sorted(C),k=k,d=d,s=s,sigma=sig,min_slack=mn,
                               CR=cr,FLAT_CR=fc,packing=pack,r0=r0,PAIR_ZERO=PZ,CENTERED_PAIR=CP))
    if worst is None or mn*worst['m']**2 < worst['slack']*m*m:
        worst=dict(name=name,m=m,P=P,C=sorted(C),slack=mn,sigma=minsigma,k=k,d=d)
    if name:saved.append(dict(name=name,k=k,m=m,d=d,P=P,C=sorted(C),min_slack=mn,sigma=minsigma,CR=cr,FLAT_CR=fc,packing=pack))

for P,name in [([8,9],'E47'),([5,6],'E51')]:
    check({(),(0,),(1,),*cwr(range(2),2),*cwr(range(2),3)},P,14,name)
for P,m,name in [([13,3,5],14,'CORE3_PURE_MIN'),([13,14,2],17,'CORE3_BINARY_MIN')]:
    cubes={(0,0,0)} if 'PURE' in name else set(cwr(range(2),3))
    check({(),*[(v,) for v in range(3)],*cwr(range(3),2),*cubes},P,m,name)
check({(),(0,),(1,),(0,0),(0,1),(0,0,0)},[1,4],6,'NO_FULL_Q_FALSE_B2')
check({(),*[(v,) for v in range(4)],*cwr(range(4),2),(0,0,0),(3,3,3)},
      [2,7,8,11],21,'CR_TABLE_CORRECTION')
check({(),*[(v,) for v in range(5)],*cwr(range(5),2),(4,4,4),(3,4,4)},
      [1,3,8,12,18],31,'HYBRID_UNPAID')

for k in (3,6,10,16,20):
    P=[4**a for a in range(k)];m=4**k
    QQ=set(cwr(range(k),2));TT=set(cwr(range(k),3))
    for mode in ('full','cube_defect','pair_defect','one')+(('few',) if k>=19 else ()):
        Q=set(QQ);T=set(TT)
        if mode=='pair_defect':Q.remove((0,0));T={y for y in T if divisors(y)<=Q}
        if mode=='cube_defect':
            remove=rng.sample(sorted(T),min(len(T)-1,k*k//9));T-=set(remove)
        if mode=='one':T={(0,0,0)}
        if mode=='few':T=set(rng.sample(sorted(T),k*k//16))
        check({(),*[(v,) for v in range(k)],*Q,*T},P,m,'B3_'+str(k)+'_'+mode)

for trial in range(trials):
    k=rng.randint(3,14);m=rng.randint(max(k+5,3*k),max(3*k+1,2*k*k))
    P=sorted(rng.sample(range(1,m),k));used={0,*P};Q=set()
    pairs=list(cwr(range(k),2));rng.shuffle(pairs)
    for z in pairs:
        r=phi(z,P,m)
        if r not in used and rng.random()<.94:Q.add(z);used.add(r)
    T=set();cubes=list(cwr(range(k),3));rng.shuffle(cubes)
    for y in cubes:
        r=phi(y,P,m)
        if divisors(y)<=Q and r not in used and rng.random()<.9:T.add(y);used.add(r)
    active=sorted({a for z in Q for a in z})
    if not active:continue
    idx={v:i for i,v in enumerate(active)}
    C={(),*[(idx[v],) for v in active],*[tuple(idx[v] for v in z) for z in Q],*[tuple(idx[v] for v in y) for y in T]}
    check(C,[P[v] for v in active],m)

out=dict(seed=seed,trials=trials,stats=dict(stats),named=saved,worst=worst,unpaid=unpaid)
Path('packing_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print('PACKING_CHECKS',json.dumps(dict(seed=seed,trials=trials,stats=dict(stats),worst=worst),sort_keys=True),flush=True)
print('PACKING_CHECKS_ALL_PASS')
