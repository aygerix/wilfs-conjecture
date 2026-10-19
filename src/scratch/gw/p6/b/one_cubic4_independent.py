"""Ordered-label independent base, k=4, Q complete, T={x_0^3}.
fejer only. Direct cells/maximality and direct phase sums.
"""
from itertools import permutations,combinations_with_replacement as cwr
from math import comb
from pathlib import Path
import json

C=[(),*[(a,) for a in range(4)],*list(cwr(range(4),2)),(0,0,0)]
CS=set(C)
N=[x for x in C if any(tuple(sorted(x+(a,))) in CS for a in range(4))]
A=CS-set(N);out=[]
for m in range(21,28):
    d=4+m-len(C);cnt=0;ph=0;mn=None;witness=None
    for P in permutations(range(1,m),4):
        lab={x:sum(P[a] for a in x)%m for x in C}
        if len(set(lab.values()))!=len(C):continue
        cnt+=1
        for sig in range(m):
            r={x:(lab[x]-sig)%m for x in C}
            S=(d+1)*sum(r[x] for x in N)-sum((len(y)-1)*r[y] for y in A)
            assert S>=0,(m,P,sig,S)
            ph+=1
            if mn is None or S<mn:mn=S;witness=dict(P=P,sigma=sig)
    row=dict(m=m,ordered_injections=cnt,phases=ph,min_slack=mn,witness=witness)
    out.append(row);print('ONE4_INDEPENDENT',json.dumps(row,sort_keys=True),flush=True)
Path('one_cubic4_independent.json').write_text(json.dumps(out,indent=2)+'\n')
print('ONE4_INDEPENDENT_PASS',sum(z['ordered_injections'] for z in out),sum(z['phases'] for z in out))
