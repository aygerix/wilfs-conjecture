"""P6 exact carry identities and analytic charging lemmas. fejer only.
Contains independent Dijkstra/grlex construction and mandatory E47/E51 tiles.
"""
import heapq,json,random,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

stats=Counter();worst=None;failrange=None;named=[];witnesses={}

def check(D,p,m,name=None):
    global worst,failrange
    D=set(D);d=len(p);zero=(0,)*d
    E=[tuple(int(a==b) for a in range(d)) for b in range(d)]
    assert zero in D and all(e in D for e in E)
    assert len(D)==m and max(map(sum,D))<=3
    def add(x,a):return tuple(x[b]+(a==b) for b in range(d))
    def sub(x,a):return tuple(x[b]-(a==b) for b in range(d))
    for x in D:
        for a in range(d):
            if x[a]:assert sub(x,a) in D
    ph={x:sum(a*b for a,b in zip(x,p))%m for x in D};assert len(set(ph.values()))==m
    byres={r:x for x,r in ph.items()}
    A={x for x in D if all(add(x,a) not in D for a in range(d))};N=D-A
    pairs=[x for x in D if sum(x)==2];T=[x for x in D if sum(x)==3]
    A2=[x for x in pairs if x in A];N2=[x for x in pairs if x in N]
    psi={z:sum(z[a]+1 for a in range(d) if add(z,a) in D) for z in N2}
    deg=[sum(z[a] for z in pairs) for a in range(d)]
    adeg=[sum(z[a] for z in A2) for a in range(d)]
    tc=[sum(y[a] for y in T) for a in range(d)]
    assert all(2*tc[a]==sum(z[a]*psi[z] for z in N2) for a in range(d))
    assert max(deg,default=0)<=d+1 and max(psi.values(),default=0)<=d+2
    UL=all(3*adeg[a]+2*tc[a]<=3*(d+1) for a in range(d))
    assert not (max(psi.values(),default=0)<=3) or UL
    ss=[];trapvals=[];phaseparts=[];brsum=0
    stats['height3_tiles']+=bool(T)
    for sig in range(m):
        rr={x:(ph[x]-sig)%m for x in D};r0=rr[zero];ru=[rr[e] for e in E];nu=m-r0
        ell={x:(1-sum(x))*r0+sum(x[a]*ru[a] for a in range(d)) for x in D}
        K={x:(ell[x]-rr[x])//m for x in D}
        assert all(ell[x]-rr[x]==m*K[x] for x in D)
        S=(d+1)*sum(rr[x] for x in N)-sum((sum(x)-1)*rr[x] for x in A)
        L=sum((d+1-deg[a])*ru[a] for a in range(d) if E[a] in N)
        L+=sum((d+2-psi[z])*rr[z] for z in N2)
        B=sum(K[z] for z in A2)+2*sum(K[y] for y in T)-sum((psi[z]-1)*K[z] for z in N2)
        assert L>=0 and S==L+m*(r0+B)
        K1={x:K[x]+sum(x)-1 for x in D}
        B1=sum(K1[z] for z in A2)+2*sum(K1[y] for y in T)-sum((psi[z]-1)*K1[z] for z in N2)
        assert B1==B+m-1-d
        assert S==L+m*(d+1-nu+B1)
        stats['tile_sigma']+=1;brsum+=B
        stats['height3_phases']+=bool(T)
        trapvals.append(r0+B)
        if B+r0<0:stats['TileCL_trap']+=1
        if B<0:stats['negative_bracket']+=1
        if all(K[z]==0 for z in N2) and all(K[z]>=0 for z in A2):
            stats['PAIR_ZERO']+=1
            neg=[y for y in T if K[y]<0]
            assert all(K[y]==-1 and rr[y]>=m-r0//2 for y in neg)
            assert 2*len(neg)<=r0 and S>=L+m*(r0%2)
            if neg:
                stats['PAIR_ZERO_negative_cubic']+=1
                witnesses.setdefault('PAIR_ZERO_negative_cubic',dict(name=name,m=m,p=p,sigma=sig,r0=r0,D=sorted(D),slack=S))
        if nu<=d+1 and all(K1[z]==0 for z in N2):
            stats['CENTERED_PAIR']+=1
            assert all(K1[z]>=0 for z in A2) and all(K1[y]>=0 for y in T)
            assert B1>=0 and S>=L+m*(d+1-nu)
            if B<0:
                stats['CENTERED_PAIR_negative_bracket']+=1
                stats['CENTERED_PAIR_h3_negative_bracket']+=bool(T)
                witnesses.setdefault('CENTERED_PAIR_negative_bracket',dict(name=name,m=m,p=p,sigma=sig,r0=r0,D=sorted(D),slack=S))
        if sig==0 and UL:
            stats['UNIT_LOAD_at0']+=1;assert S>=0
            load_remainder=sum((3*(d+1)-3*adeg[a]-2*tc[a])*ru[a] for a in range(d) if E[a] in N)
            load_remainder+=sum((3*(d+1)-2*psi[z])*rr[z] for z in N2)
            assert 3*S>=load_remainder>=0
        for y in T:
            num=sum(y[a]*rr[sub(y,a)] for a in range(d) if y[a])-r0-2*rr[y]
            assert num%m==0;kap=num//m
            if kap < -1:
                stats['pairform_kappa_below_minus1']+=1
                z=dict(m=m,p=p,sigma=sig,r0=r0,cubic=y,kappa=kap,D=sorted(D))
                if failrange is None or (m,d,sig)<(failrange['m'],len(failrange['p']),failrange['sigma']):failrange=z
        assert S>=0,dict(name=name,m=m,p=p,sigma=sig,D=sorted(D),slack=S)
        ss.append(S)
        if name:phaseparts.append(dict(sigma=sig,r0=r0,slack=S,Lplus=L,Br0=B,Br1=B1,
                                      nonmax_pair_carries=[K[z] for z in N2]))
        if worst is None or Fraction(S,m*m)<worst[0]:worst=(Fraction(S,m*m),name,m,d,sig,S)
    assert brsum==0
    C=(d+1)*len(N)-sum(sum(y)-1 for y in A)
    for sig in range(m):
        x=byres[sig];c=(d+1) if x in N else 1-sum(x)
        assert ss[(sig+1)%m]-ss[sig]==m*c-C
    if T:
        mn=min(ss)
        for sig,S in enumerate(ss):
            if S==mn:
                assert byres[sig] in N and byres[(sig-1)%m] in A
                stats['minimum_boundary']+=1
    if name:named.append(dict(name=name,m=m,p=p,D=sorted(D),min_slack=min(ss),slacks=ss,UL3=UL,trap_min=min(trapvals),phaseparts=phaseparts))
    stats['tiles']+=1

def apery(m,gens):
    d=len(gens);zero=(0,)*d;best={0:(0,0,zero)};queue=[(0,0,zero,zero)];done={}
    while queue:
        w,h,neg,x=heapq.heappop(queue);r=w%m
        if r in done or best.get(r)!=(w,h,neg):continue
        done[r]=x
        for a,g in enumerate(gens):
            y=tuple(x[b]+(a==b) for b in range(d));ny=tuple(-z for z in y);ww=w+g;rr=ww%m;key=(ww,h+1,ny)
            if rr not in done and (rr not in best or key<best[rr]):
                best[rr]=key;heapq.heappush(queue,(ww,h+1,ny,y))
    if len(done)!=m or max(map(sum,done.values()))>3:return None
    E=[tuple(int(a==b) for b in range(d)) for a in range(d)]
    if any(e not in done.values() for e in E):return None
    return set(done.values())

# Every named tile, every sigma, including both failures of dropping L+.
for m,g,name in [(4,[7],'range_min_m4'),(14,[22,23,57,61,62,63],'E47'),
                 (14,[16,17,19],'centered_worst'),(16,[17,20,21],'postage16')]:
    D=apery(m,g);assert D is not None;check(D,[x%m for x in g],m,name)
for pc,name in [((5,6),'E51'),((8,9),'E47_core_fill')]:
    core=[(a,b) for a in range(4) for b in range(4-a)];res={sum(a*b for a,b in zip(x,pc))%14 for x in core}
    miss=sorted(set(range(14))-res);d=2+len(miss)
    D=[x+(0,)*len(miss) for x in core]+[tuple(int(a==j) for a in range(d)) for j in range(2,d)]
    check(D,list(pc)+miss,14,name)

seed=int(sys.argv[1]) if len(sys.argv)>1 else 2026101981
trials=int(sys.argv[2]) if len(sys.argv)>2 else 1200
rng=random.Random(seed)
for it in range(trials):
    m=rng.randint(5,250);d=rng.randint(2,min(12,m-1));mode=it%3
    if mode==0:gens=sorted(set(rng.randint(m+1,2*m-1) for _ in range(d)))
    elif mode==1:
        a=rng.randint(m+1,2*m);step=rng.randint(1,max(1,m//(2*d)));gens=[a+j*step for j in range(d)]
    else:gens=sorted(set(rng.randint(m+1,4*m-1) for _ in range(d)))
    # Remove redundant generators, independently of normal-form tie-breaking.
    if not gens:continue
    coins=[m]+gens;ok=[False]*(max(gens)+1);ok[0]=True
    for v in range(1,len(ok)):ok[v]=any(v>=a and ok[v-a] for a in coins)
    gens=[g for g in gens if not any(a<g and ok[g-a] for a in coins)]
    if len(gens)<2 or len(set(g%m for g in gens))!=len(gens) or any(g%m==0 for g in gens):continue
    D=apery(m,gens)
    if D is not None:check(D,[g%m for g in gens],m)
print('CHARGING_COUNTS',json.dumps(dict(stats),sort_keys=True))
print('WORST',str(worst))
print('PAIRFORM_RANGE_COUNTEREXAMPLE',json.dumps(failrange,sort_keys=True))
assert failrange['m']==4 and failrange['kappa']==-2
Path('charging_named.json').write_text(json.dumps(named,indent=2)+'\n')
Path('charging_witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')
Path('charging_summary.json').write_text(json.dumps(dict(seed=seed,trials=trials,counts=dict(stats),pairform_counterexample=failrange,worst=str(worst)),indent=2)+'\n')
print('CHARGING_ALL_PASS')
