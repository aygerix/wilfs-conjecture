"""Unbounded-t missing-degree criterion. fejer only, nice, one core."""
from itertools import combinations_with_replacement as cwr
from math import comb
from collections import Counter
from pathlib import Path
import random,json
rng=random.Random(2026101961);stats=Counter();minmargin=None
for trial in range(450):
    k=rng.randint(5,32);m=rng.randint(3*k,12*k)
    P=sorted(rng.sample(range(1,m),k));used={0,*P};Q=set()
    pairs=list(cwr(range(k),2));rng.shuffle(pairs)
    for z in pairs:
        r=sum(P[i] for i in z)%m
        if r not in used and rng.random()<.55:Q.add(z);used.add(r)
    T=set();need=rng.randint(2,max(2,k//3))
    yy=list(cwr(range(k),3));rng.shuffle(yy)
    for y in yy:
        if len(T)==need:break
        div={y[:j]+y[j+1:] for j in range(3)};r=sum(P[i] for i in y)%m
        if div<=Q and r not in used:T.add(y);used.add(r)
    if len(T)<2:continue
    active=sorted({i for z in Q for i in z});ix={i:j for j,i in enumerate(active)}
    P=[P[i] for i in active];k=len(P)
    Q={tuple(ix[i] for i in z) for z in Q};T={tuple(ix[i] for i in y) for y in T}
    t=len(T);N2={z for z in Q if any(tuple(sorted(z+(i,))) in T for i in range(k))}
    psi={z:sum(z.count(i)+1 for i in range(k) if tuple(sorted(z+(i,))) in T) for z in N2}
    deg=[sum(z.count(i) for z in Q) for i in range(k)];delta=[k+1-v for v in deg]
    if k<2*t or min(delta)<t:continue
    C={(),*[(i,) for i in range(k)],*Q,*T};s=m-len(C);d=k+s
    assert s>=0 and len({sum(P[i] for i in y)%m for y in C})==len(C)
    stats['tiles']+=1;stats['t_'+str(t)]+=1
    bound=(d-t)+(s+t)*(comb(k+1,2)+k)
    assert bound>=m*t
    for sig in range(m):
        R={y:(sum(P[i] for i in y)-sig)%m for y in C};r0=R[()]
        L=sum((s+delta[i])*R[(i,)] for i in range(k))+sum((d+2-psi[z])*R[z] for z in N2)
        S=(d+1)*(r0+sum(R[(i,)] for i in range(k))+sum(R[z] for z in N2))-sum(R[z] for z in Q-N2)-2*sum(R[y] for y in T)
        H=S-m*sum((sum(R[(i,)] for i in z)-r0-R[z])//m==1 for z in Q-N2)
        assert L>=bound>=m*t and H>=L-m*t>=0
        if minmargin is None or H<minmargin:minmargin=H
        stats['phases']+=1
out=dict(seed=2026101961,trials=450,stats=dict(stats),minHCprime=minmargin)
Path('degree_check.json').write_text(json.dumps(out,indent=2)+'\n')
print('DEGREE_CHECK_ALL_PASS',json.dumps(out,sort_keys=True),flush=True)
