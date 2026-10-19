"""Try the next full-pair CR/FLAT-CR obstruction, not a theorem input.
k=4, full binary cubic face, m=21..24. fejer only, exact arithmetic.
"""
from itertools import combinations,combinations_with_replacement as cwr
from math import comb
from pathlib import Path
import json

rows=[];witnesses=[]
for m in range(21,25):
    count=0;bases=0;mn=None
    for P in combinations(range(1,m),4):
        low={(),*[(v,) for v in range(4)],*cwr(range(4),2)}
        lab={x:sum(P[v] for v in x)%m for x in low}
        if len(set(lab.values()))<len(low):continue
        bases+=1
        for I in combinations(range(4),2):
            T=set(cwr(I,3));C=low|T
            lab={x:sum(P[v] for v in x)%m for x in C}
            if len(set(lab.values()))<len(C):continue
            count+=1;s=m-len(C);d=4+s
            N={x for x in C if any(tuple(sorted(x+(v,))) in C for v in range(4))};A=C-N
            vals=[]
            for sig in range(m):
                R={x:(lab[x]-sig)%m for x in C}
                S=(d+1)*sum(R[x] for x in N)-sum((len(x)-1)*R[x] for x in A)
                if S<0:
                    z=dict(m=m,P=P,I=I,C=sorted(C),sigma=sig,S=S)
                    Path('MAXCL_COUNTEREXAMPLE.json').write_text(json.dumps(z,indent=2)+'\n');print(z,flush=True);raise SystemExit(2)
                vals.append(S)
            q=10;p=3;t=4;a=7;J=comb(8,2);B=a+2*t
            CR=(d+1)*J-B*(m-1)+t*(t-1)+a*t+a*(a-1)//2
            FC=s*comb(4,2)+(d+2)*comb(3,2)-3*t*(m-1)+t*(t-1)
            if len(witnesses)<10:
                sig=vals.index(min(vals));R={x:(lab[x]-sig)%m for x in C};r0=R[()]
                Q={x for x in C if len(x)==2};N2=Q&N
                K={z:(sum(R[(v,)] for v in z)-r0-R[z])//m for z in Q}
                PZ=all(K[z]==0 for z in N2) and all(K[z]>=0 for z in Q-N2)
                CP=m-r0<=d+1 and all(K[z]==-1 for z in N2)
                witnesses.append(dict(m=m,P=P,I=I,C=sorted(C),d=d,s=s,CR=CR,FLAT_CR=FC,
                    min_slack=min(vals),sigma=sig,r0=r0,PAIR_ZERO=PZ,CENTERED_PAIR=CP))
            mn=min(vals) if mn is None else min(mn,min(vals))
    row=dict(m=m,pair_bases=bases,instances=count,min_slack=mn);rows.append(row)
    print('BINARY4_FRONTIER',json.dumps(row,sort_keys=True),flush=True)
Path('frontier_search.json').write_text(json.dumps(dict(rows=rows,witnesses=witnesses),indent=2)+'\n')
print('FRONTIER_SEARCH_FINISHED')
