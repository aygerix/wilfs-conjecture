"""Independent sparse audit of the P8 inequalities. Run only on fejer."""
import argparse
import json
import random
from collections import Counter
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement as cwr
from math import comb
from pathlib import Path


def evaluate(m,P,Q,T,rho):
    Q=set(map(tuple,Q));T=set(map(tuple,T));k=len(P)
    faces=Counter(y[:j]+y[j+1:] for y in T for j in range(3))
    assert faces.keys()<=Q
    assert {i for z in Q for i in z}==set(range(k))
    base=[0,*P]+[sum(P[i] for i in z)%m for z in Q|T]
    assert len(set(base))==len(base)
    s=m-len(base);assert s>=0;d=k+s
    U=[(u+rho)%m for u in P]
    rp={z:(sum(U[i] for i in z)-rho)%m for z in Q}
    rt={y:(sum(U[i] for i in y)-2*rho)%m for y in T}
    kp={z:(sum(U[i] for i in z)-rho)//m for z in Q}
    kt={y:(sum(U[i] for i in y)-2*rho)//m for y in T}
    deg=Counter(i for z in Q for i in z)
    delta=[k+1-deg[i] for i in range(k)]
    A=sum(a*u for a,u in zip(delta,U))
    pairmass=sum((d+2-n)*rp[z] for z,n in faces.items())
    L=A+s*sum(U)+pairmass
    pp=sum(kp[z]==1 for z in Q if z not in faces)
    ow=rho-sum(kp[z]==-1 for z in Q if z not in faces)
    br=2*sum(kt.values())-sum((n-1)*kp[z] for z,n in faces.items())
    HC=L+m*(ow+br)
    S=(d+1)*(rho+sum(U)+sum(rp[z] for z in faces)) \
       -sum(rp[z] for z in Q if z not in faces)-2*sum(rt.values())
    assert S==HC+m*pp
    if S<0:
        print('STOP MAXCL COUNTEREXAMPLE',json.dumps(dict(m=m,P=P,Q=sorted(Q),T=sorted(T),rho=rho,S=S,HC=HC)),flush=True)
        raise SystemExit(2)
    t=len(T);p=len(faces);w=3*t-p
    assert sum(faces.values())==3*t and all(1<=n<=k+2 for n in faces.values())
    rankpair=(d+1)*comb(p,2)-w*(p-1)
    assert pairmass>=rankpair
    bound=A+s*comb(k,2)+rankpair-m*t
    assert HC>=bound
    v=sum(a>0 for a in delta);e=comb(k+1,2)-len(Q)
    assert m>=k*(k-v+1)+1
    assert m>=k*(k+1)+1-v*(v-1)-4*e
    linked_slack=None
    if v:
        qD=v*(v+1)//2-e;X=2*e-v
        numerator=4*v*qD*(qD-1)+4*(v+1)*(X*X-v*X)
        linked_slack=8*v*v*A-numerator
        assert linked_slack>=0
    beta=0;gain=0;ncw=0
    for y in T:
        b=2*kt[y]-sum(kp[y[:j]+y[j+1:]] for j in range(3))+int(rt[y]>=m-rho)
        assert b>=-1
        beta+=b==-1;gain+=max(b,0);ncw+=rt[y]>=m-rho
    pminus=sum(kp[z]==-1 for z in faces)
    pplus=sum(kp[z]==1 for z in faces)
    orest=ow-pminus-ncw
    assert orest>=0 and HC==L+m*(orest+pplus+gain-beta)
    if 25*p>=72*t and k>=150:
        h=F(72,25)
        # Independent check of the h-polynomial pair-mass deduction.
        shadowbound=(A+s*comb(k,2)
                     +(d+1)*(h*h*t*t-h*t)/2-h*(3-h)*t*t-m*t)
        assert HC>=shadowbound
    return dict(k=k,s=s,d=d,q=len(Q),p=p,t=t,w=w,e=e,v=v,
                S=S,HC=HC,L=L,pairmass=pairmass,rankpair=rankpair,
                paid_bound=bound,linked_slack=linked_slack,
                naive_pair_slack=pairmass-(d+1)*comb(p,2),
                L_minus_mt=L-m*t,beta=beta)


def random_core(rng,m,P,low_overlap):
    k=len(P);used={0,*P};Q=set();T=set();faceuse=Counter()
    if low_overlap:
        cand=list(combinations(range(k),3));rng.shuffle(cand)
        target=rng.randint(2,max(2,k))
        for y in cand:
            fs={y[:j]+y[j+1:] for j in range(3)}
            old=sum(z in faceuse for z in fs)
            w=3*len(T)-len(faceuse)
            if w+old>(len(T)+1)//10:continue
            nf=fs-Q
            nr=[sum(P[i] for i in z)%m for z in nf]
            yr=sum(P[i] for i in y)%m
            fresh=nr+[yr]
            if len(set(fresh))!=len(fresh) or any(r in used for r in fresh):continue
            Q.update(nf);T.add(y);used.update(fresh);faceuse.update(fs)
            if len(T)>=target:break
    pairs=list(cwr(range(k),2));rng.shuffle(pairs)
    for z in pairs:
        if z in Q:continue
        r=sum(P[i] for i in z)%m
        if r not in used and rng.random()<.98:Q.add(z);used.add(r)
    if not low_overlap:
        triples=list(cwr(range(k),3));rng.shuffle(triples)
        for y in triples:
            if not all(y[:j]+y[j+1:] in Q for j in range(3)):continue
            r=sum(P[i] for i in y)%m
            if r not in used and rng.random()<.96:T.add(y);used.add(r)
    active=sorted({i for z in Q for i in z})
    if not T or not active:return None
    ren={i:j for j,i in enumerate(active)}
    return ([P[i] for i in active],{tuple(ren[i] for i in z) for z in Q},
            {tuple(ren[i] for i in y) for y in T})


def fixtures(path):
    for line in Path(path).read_text().splitlines():
        cols=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(cols)!=13 or not cols[0].isdigit():continue
        m=int(cols[1]);P=list(map(int,cols[11].split(',')))
        cells=[tuple(i for i,ch in enumerate(c) for _ in range(int(ch))) for c in cols[12].split()]
        yield m,P,{z for z in cells if len(z)==2},{z for z in cells if len(z)==3},int(cols[10].split()[0])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trials',type=int,default=700)
    ap.add_argument('--seed',type=int,default=2026101981)
    ap.add_argument('--stress-source',default='stress.md')
    ap.add_argument('--output',default='results/audit.json')
    args=ap.parse_args();rng=random.Random(args.seed)
    counts=Counter();mins={};failures={};stress=[]
    def check(m,P,Q,T,phases):
        local=[]
        for rho in phases:
            a=evaluate(m,P,Q,T,rho)
            counts['phases']+=1;counts['many_cubic_phases']+=a['t']>=2 and a['k']<40*a['t']+8
            counts['p_ge_2.9t_phases']+=10*a['p']>=29*a['t']
            counts['p_eq_3t_phases']+=a['p']==3*a['t']
            for key in ['S','HC','paid_bound','pairmass','L_minus_mt']:
                if key not in mins or a[key]<mins[key]['value']:
                    mins[key]=dict(value=a[key],m=m,P=P,Q=sorted(Q),T=sorted(T),rho=rho,data=a)
            for key in ['naive_pair_slack','L_minus_mt']:
                if a[key]<0:
                    counts[key+'_failures']+=1
                    if key not in failures or (m,len(P),P,rho)<(failures[key]['m'],len(failures[key]['P']),failures[key]['P'],failures[key]['rho']):
                        failures[key]=dict(m=m,P=P,Q=sorted(Q),T=sorted(T),rho=rho,data=a)
            local.append(a['S'])
        counts['cores']+=1
        return min(local)
    for m,P,Q,T,expected in fixtures(args.stress_source):
        val=check(m,P,Q,T,range(m));assert val==expected
        stress.append(dict(m=m,P=P,minS=val))
    for P in [[5,6],[8,9]]:
        check(14,P,set(cwr(range(2),2)),set(cwr(range(2),3)),range(14))
    for i in range(args.trials):
        low=i%2==0
        m=rng.randint(40,900) if low else rng.randint(10,180)
        k=rng.randint(5,min(32,m-1)) if low else rng.randint(2,min(12,m-1))
        P=sorted(rng.sample(range(1,m),k))
        made=random_core(rng,m,P,low)
        if made is None:continue
        P,Q,T=made
        phases=range(m) if m<=180 else sorted({0,m-1,*rng.sample(range(m),min(m,40))})
        check(m,P,Q,T,phases)
        if i%100==0:print('progress',i,dict(counts),flush=True)
    out=dict(status='FINITE ACTUAL-TILE AUDIT',seed=args.seed,trials=args.trials,
             counts=counts,minima=mins,stress=stress,preserved_failures=failures)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print('DONE',json.dumps(dict(counts=counts,minima={k:v['value'] for k,v in mins.items()},
                               preserved_failures=list(failures))),flush=True)


if __name__=='__main__':main()
