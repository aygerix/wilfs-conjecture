"""Finite TWO-CUBICS bases k=4,m=21 and k=5,m=31,32.
All increasing residue vectors, both possible two-pair-shadow face types.
fejer only, exact integers. Direct cell maximality and phase sums.
"""
from itertools import combinations,combinations_with_replacement as cwr
from math import comb
from pathlib import Path
import json

rows=[];witnesses=[]
for k,ms in [(4,[21]),(5,[31,32])]:
    low={(),*[(i,) for i in range(k)],*cwr(range(k),2)}
    faces=[((i,i,i),(j,j,j)) for i,j in combinations(range(k),2)]
    faces += [((i,i,i),tuple(sorted((i,i,j)))) for i in range(k) for j in range(k) if i!=j]
    for m in ms:
        count=0;phase=0;bases=0;mn=None;best=None
        for P in combinations(range(1,m),k):
            lowlab={x:sum(P[i] for i in x)%m for x in low}
            if len(set(lowlab.values()))<len(low):continue
            bases+=1
            for face in faces:
                C=low|set(face);lab={x:sum(P[i] for i in x)%m for x in C}
                if len(set(lab.values()))<len(C):continue
                count+=1;s=m-len(C);d=k+s
                N={x for x in C if any(tuple(sorted(x+(i,))) in C for i in range(k))};A=C-N
                for sig in range(m):
                    R={x:(lab[x]-sig)%m for x in C}
                    S=(d+1)*sum(R[x] for x in N)-sum((len(x)-1)*R[x] for x in A)
                    if S<0:
                        z=dict(k=k,m=m,P=P,C=sorted(C),sigma=sig,S=S)
                        Path('MAXCL_COUNTEREXAMPLE.json').write_text(json.dumps(z,indent=2)+'\n');print(z,flush=True);raise SystemExit(2)
                    phase+=1
                    if mn is None or S<mn:mn=S;best=dict(P=P,T=face,sigma=sig)
                if k==4 and len(witnesses)<2:
                    q=comb(k+1,2);p=2;t=2;a=q-p;J=comb(1+k+p,2);B=a+2*t
                    CR=(d+1)*J-B*(m-1)+t*(t-1)+a*t+a*(a-1)//2
                    witnesses.append(dict(k=k,m=m,P=P,T=face,CR=CR))
        z=dict(k=k,m=m,bases=bases,injections=count,phases=phase,min_slack=mn,best=best);rows.append(z)
        print('TWO45',json.dumps(z,sort_keys=True),flush=True)
Path('two_cubic45.json').write_text(json.dumps(dict(rows=rows,witnesses=witnesses),indent=2)+'\n')
print('TWO45_ALL_PASS')
