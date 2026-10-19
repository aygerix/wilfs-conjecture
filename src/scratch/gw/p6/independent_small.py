"""Independent explicit-cell brute force, d=2,3, height<=3. fejer only.
No forced-cover or DP pruning; every actual cubic choice is constructed.
"""
from itertools import combinations, combinations_with_replacement, product
from math import comb
from collections import Counter
import json
from pathlib import Path

def vector(T,d):
    return tuple(T.count(a) for a in range(d))

def direct(D,p,m):
    D=set(D);d=len(p)
    A=[y for y in D if all(tuple(y[a]+(a==b) for a in range(d)) not in D for b in range(d))]
    assert len(D)==m
    residues={x:sum(x[a]*p[a] for a in range(d))%m for x in D}
    assert len(set(residues.values()))==m
    for x in D:
        for a in range(d):
            if x[a]:assert tuple(x[b]-(b==a) for b in range(d)) in D
    sl=[]
    for sig in range(m):
        rr={x:(residues[x]-sig)%m for x in D}
        value=(d+1)*sum(rr[x] for x in D if x not in A)-sum((sum(x)-1)*rr[x] for x in A)
        assert value>=0,dict(m=m,p=p,D=sorted(D),sigma=sig,slack=value)
        sl.append(value)
    return min(sl)

out=[]
for d in (2,3):
    z=(0,)*d;E=[vector((a,),d) for a in range(d)]
    pairs=[vector(T,d) for T in combinations_with_replacement(range(d),2)]
    triples=[vector(T,d) for T in combinations_with_replacement(range(d),3)]
    for m in range(d+1,comb(d+3,3)+1):
        faces=tiles=sigmas=flat=0;mn=None
        for p in combinations(range(1,m),d):
            def res(x):return sum(a*b for a,b in zip(x,p))%m
            units={0,*p}
            for mask in range(1<<len(pairs)):
                Q=[pairs[j] for j in range(len(pairs)) if mask>>j&1]
                qr=[res(x) for x in Q]
                if len(set(qr)|units)!=d+1+len(Q):continue
                rem=sorted(set(range(m))-units-set(qr))
                if not rem:flat+=1;continue
                qset=set(Q);opts={r:[] for r in rem}
                for y in triples:
                    if res(y) not in opts:continue
                    if all(tuple(y[b]-(b==a) for b in range(d)) in qset for a in range(d) if y[a]):
                        opts[res(y)].append(y)
                if any(not opts[r] for r in rem):continue
                faces+=1
                for selected in product(*(opts[r] for r in rem)):
                    val=direct([z]+E+Q+list(selected),p,m)
                    tiles+=1;sigmas+=m;mn=val if mn is None else min(mn,val)
        row=dict(d=d,m=m,pairfaces=faces,flat=flat,actual_tiles=tiles,sigma_pairs=sigmas,min_slack=mn)
        print(json.dumps(row,sort_keys=True),flush=True);out.append(row)
Path('independent_small.json').write_text(json.dumps(out,indent=2)+'\n')
print('INDEPENDENT_EXPLICIT_TILES_PASS')
