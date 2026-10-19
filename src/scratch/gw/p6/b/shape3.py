"""Exact independent shadow and CR-profile table, k=3. fejer only."""
from itertools import combinations_with_replacement as cwr
from math import comb
from pathlib import Path
import json

Q=list(cwr(range(3),2));T=list(cwr(range(3),3))
div=lambda y:{y[:j]+y[j+1:] for j in range(3)}
maxT={};equality3=[]
for bits in range(1<<6):
    P={Q[j] for j in range(6) if bits>>j&1}
    legal=[y for y in T if div(y)<=P];p=len(P)
    maxT[p]=max(maxT.get(p,0),len(legal))
    if p==3 and len(legal)==4:equality3.append(sorted(P))
assert maxT=={0:0,1:1,2:2,3:4,4:5,5:7,6:10}
table=[];bad=[]
for p in range(1,7):
    j=comb(4+p,2)
    for q in range(p,7):
        for t in range(1,maxT[p]+1):
            a=q-p;b=a+2*t;size=4+q+t
            assert j>b
            # d=6 means s=3 and m=|C|+3. Larger s has positive slope.
            m=size+3
            cr=7*j-(t*t+(2*q+13)*t+a*(q+6)-a*(a-1)//2)
            threshold=(j*(q+t)-t*t-t-a*t-a*(a+1)//2+j-b-1)//(j-b)
            for mm in range(m,threshold):bad.append(dict(q=q,p=p,t=t,m=mm,s=mm-size,CR=cr+(mm-m)*(j-b)))
    q=5 if p<=5 else 6;t=maxT[p];a=q-p
    table.append(dict(p=p,tmax=t,q=q,CR_at_s3=7*j-(t*t+(2*q+13)*t+a*(q+6)-a*(a-1)//2)))
assert len(bad)==5
print('SHADOW3',json.dumps(maxT,sort_keys=True),'EQUALITY3',json.dumps(equality3))
print('CR3_TABLE',json.dumps(table,sort_keys=True))
print('CR3_BAD_CARDINALITIES',json.dumps(bad,sort_keys=True))
Path('shape3.json').write_text(json.dumps(dict(shadow=maxT,equality3=equality3,table=table,bad=bad),indent=2)+'\n')
print('SHAPE3_ALL_PASS')
