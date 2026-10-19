"""Targeted residue-complete completions and independent a=4 checks.
Execute only on fejer. No external packages. Single core.
"""
import argparse
from collections import Counter
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
import json
import random
import sys
try:
    from explore import independent_verify
except ModuleNotFoundError:
    sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
    from explore import independent_verify


def monos(d,k):
    if d==0:
        yield ()
        return
    for first in range(k+1):
        for tail in monos(d-1,k-first):yield (first,)+tail


def a4_checks(D,n):
    m=len(D);d=len(n);V={x:sum(a*b for a,b in zip(x,n)) for x in D};M=max(V.values())
    if M//m!=4:return None
    rho=5*m-1-M;cl=[(ni+rho)//m for ni in n]
    if cl.count(1)!=4:return None
    As=[j for j in range(d) if cl[j]==1];Bs=[j for j in range(d) if cl[j]==2]
    b=len(Bs);c=cl.count(3);e=cl.count(4)
    ct=Counter();s3pairs=set();BB3=set();v2=v3=0
    for x,v in V.items():
        typ=tuple(sorted(cc for xi,cc in zip(x,cl) for _ in range(xi)))
        band=(v+rho)//m
        ct[typ,band]+=1
        if typ==(1,2) and band==3:
            s3pairs.add((next(j for j in As if x[j]),next(j for j in Bs if x[j])))
        if typ==(2,2) and band==3:BB3.add(tuple(j for j in Bs for _ in range(x[j])))
        if typ==(1,1,2):
            bv=sum(x[j]*n[j] for j in Bs)
            if (v-bv+rho)//m==2:v2+=1
            else:v3+=1
    q2=ct[(1,1),2];q3=ct[(1,1),3];u3=ct[(1,1,1),3];u4=ct[(1,1,1),4];k=ct[(1,1,1,1),4]
    WA=60+6*q2+q3+u3-4*(u4+k)
    if WA>=0:return dict(WA=WA)
    assert (q2,q3,u3,u4,k,WA) in {(0,10,0,20-t,0,-10+4*t) for t in range(3)}|{(1,9,0,20-t,0,-5+4*t) for t in range(2)}|{(1,9,1,19,1,-4)}
    s3=ct[(1,2),3];t3=ct[(2,2),3];t4=ct[(2,2),4];w=ct[(1,2,2),4];z=ct[(2,2,2),4]
    p=4*b-s3;B=comb(b+1,2);Z=comb(b+2,3)
    cap=sum(comb(1+sum((i,j) in s3pairs for i in As),2) for j in Bs)
    assert v2+v3<=cap
    Dv=2*b*q2+b*q3+5*s3-4*v2-3*v3
    assert 2*Dv>=5*p
    if p==1:assert Dv>=7
    if p==2 and q2==0:assert Dv>=11
    Dw=4*t3+(b+1)*s3-3*w
    if p==0:assert Dw>=8*(B-t3)
    if B>t3:assert Z-z>=b
    if p==1 and t3+t4==B:
        bad=next(j for j in Bs if sum((i,j) in s3pairs for i in As)==3)
        L=sum(bad in x for x in BB3)
        assert w<=4*t3-L
        assert Dw>=5*t4+2*b-1
    ell=sum((M-v)//m for v in V.values());W=(d+1)*ell-(4*m-rho)
    return dict(m=m,h=m-rho,rho=rho,d=d,a=4,b=b,c=c,e=e,WA=WA,W=W,ell=ell,
                q2=q2,q3=q3,u3=u3,u4=u4,k=k,p=p,Dv=Dv,Dw=Dw)


def a5_checks(D,n):
    m=len(D);d=len(n);V={x:sum(a*b for a,b in zip(x,n)) for x in D};M=max(V.values())
    if M//m!=4:return None
    rho=5*m-1-M;cl=[(ni+rho)//m for ni in n]
    A=[j for j in range(d) if cl[j]==1];Bs=[j for j in range(d) if cl[j]==2]
    if len(A)!=5:return None
    ct=Counter();adj={j:set() for j in Bs};v2=Counter();v3=Counter();lowpairs=[]
    for x,v in V.items():
        typ=tuple(sorted(cc for xi,cc in zip(x,cl) for _ in range(xi)));band=(v+rho)//m
        ct[typ,band]+=1
        if typ==(1,1) and band==2:lowpairs.append({j for j in A if x[j]})
        if typ==(1,2) and band==3:
            bj=next(j for j in Bs if x[j]);adj[bj].add(next(j for j in A if x[j]))
        if typ==(1,1,2):
            bj=next(j for j in Bs if x[j]);ab=(v-n[bj]+rho)//m
            if ab==2:v2[bj]+=1
            else:assert ab==3;v3[bj]+=1
    q2=ct[(1,1),2];q3=ct[(1,1),3];u3=ct[(1,1,1),3];u4=ct[(1,1,1),4];k=ct[(1,1,1,1),4]
    WA=90+8*q2+2*(q3+u3)-4*(u4+k)
    if WA>=0:return dict(WA=WA)
    Q=15;F=20
    from a4_stability import grow
    assert (6*(q2+u3)-4*k)>=min(6*q2,F)
    assert q2<=3
    assert q2+q3 in (14,15)
    allowed={(0,14,0,30,0,-2)}
    for low,uu,kk,ts in [(0,0,0,range(5)),(1,0,0,range(4)),(1,1,0,range(2)),
                         (1,1,1,range(3)),(2,0,0,range(2)),(2,1,0,range(1)),
                         (2,1,1,range(2)),(2,2,2,range(1)),(3,0,0,range(1))]:
        for tt in ts:
            ww=-20+6*(low+uu)-4*kk+4*tt
            allowed.add((low,15-low,uu,35-uu-tt,kk,ww))
    assert (q2,q3,u3,u4,k,WA) in allowed
    if q2+q3==14:assert (q2,q3,u3,u4,k,WA)==(0,14,0,30,0,-2)
    else:
        for bj in Bs:
            p=5-len(adj[bj]);qlow=sum(x<=adj[bj] for x in lowpairs)
            cost=p+2*q2+q3+6*len(adj[bj])-4*v2[bj]-3*v3[bj]
            assert cost>=p*(23-3*p)//2+q2-qlow
    independent=independent_verify(D,n)
    return dict(m=m,h=m-rho,rho=rho,d=d,a=5,b=len(Bs),c=cl.count(3),e=cl.count(4),
                WA=WA,W=independent['slack'],ell=sum((M-v)//m for v in V.values()),
                q2=q2,q3=q3,u3=u3,u4=u4,k=k,p=sum(5-len(x) for x in adj.values()))


def a6_checks(D,n):
    from a4_stability import grow
    from packing_fibers import coverage_bound
    m=len(D);d=len(n);V={x:sum(a*b for a,b in zip(x,n)) for x in D};M=max(V.values())
    if M//m!=4:return None
    rho=5*m-1-M;cl=[(ni+rho)//m for ni in n]
    A=[j for j in range(d) if cl[j]==1];Bs=[j for j in range(d) if cl[j]==2]
    if len(A)!=6:return None
    ct=Counter();adj={j:set() for j in Bs};v2=Counter();v3=Counter();lowpairs=[]
    for x,v in V.items():
        typ=tuple(sorted(cc for xi,cc in zip(x,cl) for _ in range(xi)));band=(v+rho)//m
        ct[typ,band]+=1
        if typ==(1,1) and band==2:lowpairs.append({j for j in A if x[j]})
        if typ==(1,2) and band==3:
            bj=next(j for j in Bs if x[j]);adj[bj].add(next(j for j in A if x[j]))
        if typ==(1,1,2):
            bj=next(j for j in Bs if x[j]);ab=(v-n[bj]+rho)//m
            if ab==2:v2[bj]+=1
            else:assert ab==3;v3[bj]+=1
    q2=ct[(1,1),2];q3=ct[(1,1),3];u3=ct[(1,1,1),3];u4=ct[(1,1,1),4];k=ct[(1,1,1,1),4]
    WA=126+10*q2+3*(q3+u3)-4*(u4+k)
    if WA>=0:return dict(WA=WA)
    low=7*(q2+u3)-4*k
    assert low>=min(7*q2,35) and q2<=4 and q2+q3 in (20,21)
    if q2+q3==20:
        assert (q2,u3,k,56-u3-u4) in {(0,0,0,j) for j in range(6,10)}|{(1,0,0,j) for j in (6,7)}|{(1,1,1,6)}
    else:
        assert u3<=grow(q2,2) and k<=grow(u3,3)
        residues=[0]+[n[j]%m for j in A]
        sums=[sum(residues[j] for j in ii)%m for ii in combinations_with_replacement(range(7),3)]
        excess=len(sums)-len(set(sums));assert m>=coverage_bound(7,m,excess)
        for bj in Bs:
            p=6-len(adj[bj]);qlow=sum(x<=adj[bj] for x in lowpairs)
            cost=p+2*q2+q3+7*len(adj[bj])-4*v2[bj]-3*v3[bj]
            assert cost>=p*(27-3*p)//2+q2-qlow
    original=independent_verify(D,n)
    return dict(m=m,h=m-rho,rho=rho,d=d,a=6,b=len(Bs),c=cl.count(3),e=cl.count(4),
                WA=WA,W=original['slack'],ell=sum((M-v)//m for v in V.values()),
                q2=q2,q3=q3,u3=u3,u4=u4,k=k,p=sum(6-len(x) for x in adj.values()))


def completed(core,n,m,h):
    M=4*m+h-1;seen={sum(xi*ni for xi,ni in zip(x,n))%m for x in core}
    extra=tuple(3*m+h+(r-h)%m for r in range(m) if r not in seen)
    nn=n+extra;d=len(nn)
    D={x+(0,)*len(extra) for x in core}
    D.update(tuple(int(j==k) for j in range(d)) for k in range(len(n),d))
    assert len(D)==m and max(sum(a*b for a,b in zip(x,nn)) for x in D)==M
    return D,nn


def objective(core,n,m,h):
    M=4*m+h-1
    ell=sum((M-sum(a*b for a,b in zip(x,n)))//m for x in core)
    d=len(n)+m-len(core)
    return (d+1)*ell-(3*m+h)


def extend(core,n,w,m,h,rng):
    M=4*m+h-1;reserve=(h-1)%m
    seen={sum(xi*ni for xi,ni in zip(x,n))%m for x in core}
    if w%m in seen or w%m==reserve:return None
    nn=n+(w,);d=len(nn);D={x+(0,) for x in core}
    candidates=[]
    for x in monos(d,4):
        if not x[-1]:continue
        v=sum(a*b for a,b in zip(x,nn))
        if v<=M:candidates.append((sum(x),rng.random(),v,x))
    candidates.sort()
    for deg,priority,v,x in candidates:
        if v%m in seen or v%m==reserve:continue
        if all(not x[j] or x[:j]+(x[j]-1,)+x[j+1:] in D for j in range(d)):
            D.add(x);seen.add(v%m)
    if not any(x[-1] for x in D):return None
    return D,nn


def search(trials,seed,amax=4):
    rng=random.Random(seed);hist=Counter();best=[];smallest_quartic=None
    for trial in range(trials):
        a=amax
        m=rng.randrange(60,241) if a==4 else rng.randrange(120,701) if a==5 else rng.randrange(180,1001)
        h=rng.randrange(2*a+6,m+1);flavor=trial%3
        if flavor==0:
            t=tuple(sorted(rng.sample(range((h+1)//2,h),a)))
        else:
            if flavor==1:
                lo=(h+2)//3;hi=(h-1)//2
            else:
                lo=a-1;hi=(h-1)//4
            if lo>hi:continue
            t0=rng.randrange(lo,hi+1)
            if t0<a-1:continue
            t=(t0,)+tuple(sorted(rng.sample(range(h-t0,h),a-1)))
        n=tuple(m+v for v in t);M=4*m+h-1
        core={x for x in monos(a,4) if sum(aa*bb for aa,bb in zip(x,n))<=M}
        if len(core)>m:continue
        vals=[sum(a*b for a,b in zip(x,n)) for x in core]
        if len({v%m for v in vals})!=len(core) or (h-1)%m in {v%m for v in vals}:continue
        checker={4:a4_checks,5:a5_checks,6:a6_checks}[a]
        D,nn=completed(core,n,m,h);st=checker(D,nn)
        if st is None or st['WA']>=0:continue
        hist['accepted_core']+=1;hist[f'profile_{st["q2"]}_{st["u3"]}_{st["k"]}']+=1
        for step in range(6 if a==4 else 3):
            cand=[]
            for w in rng.sample(range(m+h,2*m+h),min(18,m)):
                result=extend(core,n,w,m,h,rng)
                if result is None:continue
                DD,nnn=result;score=objective(DD,nnn,m,h)
                cand.append((score,rng.random(),DD,nnn))
            if not cand:break
            score,_,DD,nnn=min(cand,key=lambda x:(x[0],x[1]))
            core,n=DD,nnn;hist['B_added']+=1
            stepD,stepn=completed(core,n,m,h)
            independent_verify(stepD,stepn);stepstat=checker(stepD,stepn)
            hist[f'checked_b{stepstat["b"]}']+=1
        D,nn=completed(core,n,m,h)
        original=independent_verify(D,nn);st=checker(D,nn)
        assert st['W']==original['slack']>=0
        hist['verified']+=1;hist['rho_zero']+=st['rho']==0;hist['rho_near_m']+=st['rho']*5>=4*m
        if len(best)<8 or st['W']<best[-1]['stats']['W']:
            best.append(dict(stats=st,n=nn,D=sorted(D)));best.sort(key=lambda x:x['stats']['W']);best=best[:8]
        if st['k'] and (smallest_quartic is None or (m,st['W'])<(smallest_quartic['stats']['m'],smallest_quartic['stats']['W'])):
            smallest_quartic=dict(stats=st,n=nn,D=sorted(D))
        if trial%100==0:print(json.dumps(dict(progress=trial,counts=hist,best=best[0]['stats'] if best else None)),flush=True)
    artifact=dict(seed=seed,trials=trials,counts=hist,best=best,smallest_quartic=smallest_quartic)
    Path('completion_examples.json' if amax==4 else f'completion_examples_a{amax}.json').write_text(json.dumps(artifact,indent=2)+'\n')
    print(json.dumps(dict(mode='completions',seed=seed,trials=trials,counts=hist,best=[x['stats'] for x in best],smallest_quartic=smallest_quartic['stats'] if smallest_quartic else None)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=1000);p.add_argument('--seed',type=int,default=20261019);p.add_argument('--a',type=int,default=4)
    args=p.parse_args();search(args.trials,args.seed,args.a)
