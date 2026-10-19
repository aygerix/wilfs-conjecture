"""Actual remaining payment profiles: k=5, full Q, two-cubic shadow p=2.
Only the CR-failing m=31,32; all sorted bases and both possible face types.
Not an input to a universal theorem. fejer only, nice, exact integers.
"""
from itertools import combinations,combinations_with_replacement as cwr
from math import comb
from pathlib import Path
import json

out=[];saved=[]
for m in (31,32):
    bases=0;instances=0;phases=0;mn=None
    low={(),*[(i,) for i in range(5)],*cwr(range(5),2)}
    faces=[((i,i,i),(j,j,j)) for i,j in combinations(range(5),2)]
    faces += [((i,i,i),tuple(sorted((i,i,j)))) for i in range(5) for j in range(5) if i!=j]
    for P in combinations(range(1,m),5):
        lab={x:sum(P[i] for i in x)%m for x in low}
        if len(set(lab.values()))<len(low):continue
        bases+=1
        for face in faces:
            C=low|set(face);lab={x:sum(P[i] for i in x)%m for x in C}
            if len(set(lab.values()))<len(C):continue
            instances+=1;s=m-len(C);d=5+s
            N={x for x in C if any(tuple(sorted(x+(i,))) in C for i in range(5))};A=C-N
            vals=[]
            for sig in range(m):
                R={x:(lab[x]-sig)%m for x in C}
                S=(d+1)*sum(R[x] for x in N)-sum((len(x)-1)*R[x] for x in A)
                if S<0:
                    w=dict(m=m,P=P,C=sorted(C),sigma=sig,S=S)
                    Path('MAXCL_COUNTEREXAMPLE.json').write_text(json.dumps(w,indent=2)+'\n');print(w,flush=True);raise SystemExit(2)
                vals.append(S);phases+=1
            vv=min(vals);mn=vv if mn is None else min(mn,vv)
            if len(saved)<8:
                sig=vals.index(vv);R={x:(lab[x]-sig)%m for x in C};r0=R[()]
                Q={x for x in C if len(x)==2};N2=Q&N
                K={z:(sum(R[(i,)] for i in z)-r0-R[z])//m for z in Q}
                PZ=all(K[z]==0 for z in N2) and all(K[z]>=0 for z in Q-N2)
                CP=m-r0<=d+1 and all(K[z]==-1 for z in N2)
                p=len(N2);q=15;t=2;a=q-p;J=comb(1+5+p,2);B=a+2*t
                CR=(d+1)*J-B*(m-1)+t*(t-1)+a*t+a*(a-1)//2
                FC=s*comb(5,2)+(d+2)*comb(p,2)-3*t*(m-1)+t*(t-1)
                saved.append(dict(m=m,P=P,C=sorted(C),T=face,d=d,s=s,p=p,CR=CR,FLAT_CR=FC,
                    min_slack=vv,sigma=sig,r0=r0,PAIR_ZERO=PZ,CENTERED_PAIR=CP))
    row=dict(m=m,bases=bases,instances=instances,phases=phases,min_slack=mn);out.append(row)
    print('FRONTIER_TWO5',json.dumps(row,sort_keys=True),flush=True)
Path('frontier_two5.json').write_text(json.dumps(dict(rows=out,witnesses=saved),indent=2)+'\n')
print('FRONTIER_TWO5_FINISHED')
