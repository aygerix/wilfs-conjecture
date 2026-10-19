"""P6c exact actual-tile checks. fejer only, nice, one core.
No finite search in this file is used as a uniform proof.
"""
from itertools import combinations_with_replacement as cwr, combinations, product
from math import comb
from collections import Counter
from pathlib import Path
import random,json,sys

rng=random.Random(2026101941);stats=Counter();minima={};saved=[]
def pred(y):return {y[:j]+y[j+1:] for j in range(len(y))}
def phi(y,P,m):return sum(P[i] for i in y)%m
def record(key,value,witness=None):
    if key not in minima or value<minima[key]['slack']:
        minima[key]=dict(slack=value,witness=witness)
def check(C,P,m,name=None):
    C=set(C);k=len(P)
    assert () in C and all(pred(y)<=C for y in C if y)
    N={y for y in C if any(tuple(sorted(y+(i,))) in C for i in range(k))}
    assert all((i,) in N for i in range(k))
    Q={z for z in C if len(z)==2};T={y for y in C if len(y)==3}
    N2=Q&N;A2=Q-N2;a=len(A2);p=len(N2);t=len(T);q=len(Q)
    s=m-len(C);d=k+s;assert s>=0
    lab={y:phi(y,P,m) for y in C};assert len(set(lab.values()))==len(C)
    deg=[sum(z.count(i) for z in Q) for i in range(k)]
    delta=[k+1-v for v in deg];e=comb(k+1,2)-q
    psi={z:sum(z.count(i)+1 for i in range(k) if tuple(sorted(z+(i,))) in T) for z in N2}
    c=k+1;f,rem=divmod(2*e,c);FD=c*comb(f,2)+f*rem
    FG=sum(j*v for j,v in enumerate(sorted(delta,reverse=True)))
    assert FG>=FD
    # Common-denominator rectangles need no complete pair face.
    for h in sorted({1,min(2,k),max(1,k//2),k}):
        for rep in range(2):
            J=set(rng.sample(range(k),h))
            F={z for z in C if all(tuple(sorted(z+(i,))) in C for i in J)}
            labels=[]
            for z in F:
                labels.append(phi(z,P,m))
                labels.extend((phi(z,P,m)-P[i])%m for i in J if i not in z)
            assert len(set(labels))==len(labels)<=m
            assert len(labels)==sum(h+1-len(set(z)&J) for z in F)
            stats['RECTANGLE']+=1
    # All subsets: the binomial moment is the literal rectangle average.
    if k<=8:
        succ={z:{i for i in range(k) if tuple(sorted(z+(i,))) in C} for z in C}
        for h in range(1,k+1):
            numer=0;direct=0
            for z,I in succ.items():
                if len(I)>=h:
                    numer+=(h+1)*comb(len(I),h)-len(set(z)&I)*comb(len(I)-1,h-1)
            for jj in combinations(range(k),h):
                J=set(jj)
                direct+=sum(h+1-len(set(z)&J) for z,I in succ.items() if J<=I)
            assert numer==direct and numer<=m*comb(k,h)
            stats['ROW_MOMENT']+=1
    common=set.intersection(*[set(y) for y in T]) if T else set()
    phase_rows=[]
    for sig in range(m):
        R={y:(v-sig)%m for y,v in lab.items()};r0=R[()];nu=m-r0
        K={y:(sum(R[(i,)] for i in y)-(len(y)-1)*r0-R[y])//m for y in Q|T}
        L=sum((d+1-deg[i])*R[(i,)] for i in range(k))+sum((d+2-psi[z])*R[z] for z in N2)
        S=(d+1)*(r0+sum(R[(i,)] for i in range(k))+sum(R[z] for z in N2))-sum(R[z] for z in A2)-2*sum(R[y] for y in T)
        OW=r0-sum(K[z]==-1 for z in A2)
        H=S-m*sum(K[z]==1 for z in A2)
        B=2*sum(K[y] for y in T)-sum((psi[z]-1)*K[z] for z in N2)
        assert H==L+m*(OW+B)
        kappas={y:2*K[y]-sum(y.count(i)*K[y[:j]+y[j+1:]] for j,i in enumerate(y) if i not in y[:j]) for y in T}
        # Each distinct divisor is included with the deleted multiplicity y_i.
        nneg=sum(K[z]==-1 for z in N2);npos=sum(K[z]==1 for z in N2)
        nw=sum(R[y]>=nu for y in T)
        rest=OW-nneg-nw
        assert rest>=0
        adjusted=[kappas[y]+int(R[y]>=nu) for y in T]
        assert all(v>=-1 for v in adjusted)
        bad=sum(v==-1 for v in adjusted);gain=sum(max(0,v) for v in adjusted)
        assert H==L+m*(rest+npos+gain-bad)
        assert H>=L-m*t
        stats['WINDOW_ID']+=1
        assert S>=0,dict(P=P,m=m,C=sorted(C),sig=sig,S=S)
        U=sum((d+1-deg[i])*R[(i,)] for i in range(k))
        assert U>=s*comb(k,2)+FG>=s*comb(k,2)+FD
        bound=s*comb(k,2)+FD+(d+2)*comb(p,2)-3*t*(m-1)+t*(t-1)
        assert S>=bound
        stats['DEFECT_FLAT']+=1
        lm=min(R[(i,)] for i in range(k))
        assert OW>=min(r0,2*lm)
        stats['WINDOW_MIN']+=1
        high={i for i in range(k) if 2*R[(i,)]>=m+r0};g=len(high)
        ac=Counter(sum(i in high for i in z) for z in A2)
        tc=Counter(sum(i in high for i in y) for y in T)
        cost=ac[1]+2*ac[0]+4*tc[2]+6*tc[1]+8*tc[0]
        eta=(m+r0)%2
        carrybound=2*g-d-1+eta-cost
        assert r0+sum(K[z] for z in A2)+B>=carrybound
        upper=L+m*carrybound
        assert S>=upper
        if g>=2:
            simple=m*(2*g-k-1+eta-cost)+s*(g*((m+r0+1)//2)-m)
            assert S>=simple
            if cost<=2*g-k-1+eta:
                assert simple>=0;stats['UPPER_PAY']+=1
        stats['UPPER_ARC']+=1
        if any(sig==P[i] for i in common):
            assert OW+B>=0
            stats['CONE_PHASE']+=1
            record('CONE_PHASE',OW+B,dict(P=P,m=m,sig=sig,t=t))
        if sig in P:
            anchor=P.index(sig);inside={y for y in T if anchor in y}
            oldpairs={z for z in Q if any(tuple(sorted(z+(i,))) in inside for i in range(k))}
            out=t-len(inside);pnew=len(N2-oldpairs)
            assert H>=L-m*(7*out-pnew)
            stats['CONE_DEFECT']+=1
        if t==1:
            assert OW+B>=-1
            stats['ONE_LOSS']+=1;record('ONE_LOSS',OW+B+1)
            if any(R[z]==0 for z in N2):
                assert OW+B>=0;stats['ONE_PAIR_PHASE']+=1
            if OW+B<0:
                yy=next(iter(T));assert OW+B==-1 and OW==1 and K[yy]==-1
                assert R[yy]>=nu and all(K[z]==0 and R[z]>=2 for z in N2)
                assert 8<=r0 and 2*r0<m and m>=17
                for val in (0,1):
                    ii=next(i for i in range(k) if R[(i,)]==val)
                    assert ii not in yy
                stats['ONE_DEFICIT']+=1
            v=sum(dd>0 for dd in delta);gclean=k-v
            if v>=2 and s*(comb(v+1,2)-1)+e+k-6>=gclean*(2*k-gclean+1)//2:
                assert H>=0;stats['ONE_PARTIAL_COVER']+=1
            if gclean==0 and k>=4:
                assert H>=0;stats['ONE_COVERED_STRONG']+=1
            if all(v>=1 for v in delta) and s*(comb(k+1,2)-1)+e>=4:
                assert H>=0;stats['ONE_COVERED']+=1
            if k>=36 and e*e>=k**3:
                assert S>=0;stats['ONE_LARGE_DEFECT']+=1
        stats['phases']+=1
        phase_rows.append((S,H,sig))
    stats['tiles']+=1;stats['height3_tiles']+=bool(T)
    stats['one_cube_tiles']+=t==1;stats['cone_tiles']+=bool(common)
    if name:saved.append(dict(name=name,k=k,m=m,q=q,p=p,t=t,s=s,
                             minS=min(phase_rows),minHC=min(phase_rows,key=lambda x:x[1]),FD=FD))

for P,name in [([8,9],'E47'),([5,6],'E51')]:
    check({(),(0,),(1,),*cwr(range(2),2),*cwr(range(2),3)},P,14,name)
check({(),*[(i,) for i in range(4)],*cwr(range(4),2),(0,0,0)}-{(1,2),(3,3)},[1,4,6,9],16,'F3')
check({(),*[(i,) for i in range(5)],*cwr(range(5),2),(4,4,4),(3,4,4)},[1,3,8,12,18],31,'HYBRID_UNPAID')

# Infinite sharp one-cubic-loss family, smallest member (r,u)=(2,5).
for rr,uu in ((2,5),(2,6),(3,7),(4,9),(7,16)):
    rho=2*uu-rr;m=2*rho+1;special=uu+rr
    unit_res=[v for v in range(rho) if v not in (rr,special)]
    P=[(v-rho)%m for v in unit_res];ix={v:i for i,v in enumerate(unit_res)}
    Q={tuple(sorted((ix[0],ix[v]))) for v in range(rho) if v not in (rr,special)}
    Q.add(tuple(sorted((ix[1],ix[rr-1]))));Q.add((ix[uu],ix[uu]))
    C={(),*[(i,) for i in range(len(P))],*Q,(ix[uu],)*3}
    check(C,P,m,'ONE_LOSS_SHARP_'+str(rr)+'_'+str(uu))

trials=int(sys.argv[1]) if len(sys.argv)>1 else 1400
for tr in range(trials):
    k=rng.randint(3,18);m=rng.randint(3*k,min(300,3*k*k))
    P=sorted(rng.sample(range(1,m),k));used={0,*P};Q=set()
    pairs=list(cwr(range(k),2));rng.shuffle(pairs)
    for z in pairs:
        r=phi(z,P,m)
        if r not in used and rng.random()<.95:Q.add(z);used.add(r)
    eligible=[y for y in cwr(range(k),3) if pred(y)<=Q and phi(y,P,m) not in used]
    if not eligible:continue
    mode=tr%3;T=set()
    if mode==0:
        y=rng.choice(eligible);T.add(y)
    else:
        anchor=rng.randrange(k);rng.shuffle(eligible)
        for y in eligible:
            if mode==1 and anchor not in y:continue
            r=phi(y,P,m)
            if r not in used and rng.random()<.9:T.add(y);used.add(r)
    if not T:continue
    active=sorted({i for z in Q for i in z});index={i:j for j,i in enumerate(active)}
    C={(),*[(index[i],) for i in active],*[tuple(index[i] for i in z) for z in Q],*[tuple(index[i] for i in y) for y in T]}
    check(C,[P[i] for i in active],m)
    if tr%200==0:print('PROGRESS',tr,dict(stats),flush=True)

# Larger k one-cube examples in the analytical defect range.
for k in (36,40,48):
    m=8*k;P=sorted(rng.sample(range(1,m),k));used={0,*P};Q=set()
    for z in cwr(range(k),2):
        r=phi(z,P,m)
        if r not in used:Q.add(z);used.add(r)
    eligible=[y for y in cwr(range(k),3) if pred(y)<=Q and phi(y,P,m) not in used]
    if eligible:
        y=rng.choice(eligible);active=sorted({i for z in Q for i in z});idx={i:j for j,i in enumerate(active)}
        C={(),*[(idx[i],) for i in active],*[tuple(idx[i] for i in z) for z in Q],tuple(idx[i] for i in y)}
        check(C,[P[i] for i in active],m,'ONE_LARGE_'+str(k))

out=dict(seed=2026101941,trials=trials,stats=dict(stats),minima=minima,named=saved)
Path('checks.json').write_text(json.dumps(out,indent=2)+'\n')
print('DONE',json.dumps(dict(seed=out['seed'],trials=trials,stats=dict(stats),minima=minima),sort_keys=True),flush=True)
