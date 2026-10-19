"""Small actual non-complete quadratic core; scalar-payment failure.
Also checks whether the elementary shape relaxation can fail CR at m<=15.
fejer only, nice, exact integers. No MaxCL counterexample is accepted.
"""
from math import comb
from pathlib import Path
import json

profiles=0;bad=[]
for m in range(1,16):
    for k in range(4,m):
        for q in range(1,min(comb(k+1,2),m-k-2)+1):
            if 2*q<k:continue
            for t in range(1,m-k-q):
                s=m-1-k-q-t;d=k+s
                if s<0 or d<6:continue
                for p in range(1,q+1):
                    if not p<=3*t<=p*(k+2):continue
                    profiles+=1;a=q-p;J=comb(1+k+p,2);B=a+2*t
                    R=(d+1)*J-B*(m-1)+t*(t-1)+a*t+a*(a-1)//2
                    if R<0:bad.append(dict(m=m,k=k,q=q,t=t,p=p,s=s,CR=R))

P=[1,4,6,9];m=16
Q={(0,0),(0,1),(0,2),(0,3),(1,1),(1,3),(2,2),(2,3)}
T={(0,0,0)};C={(),(0,),(1,),(2,),(3,),*Q,*T}
lab={x:sum(P[i] for i in x)%m for x in C};assert len(set(lab.values()))==len(C)==14
N={x for x in C if any(tuple(sorted(x+(i,))) in C for i in range(4))};A=C-N
vals=[]
for sig in range(m):
    r={x:(lab[x]-sig)%m for x in C}
    S=7*sum(r[x] for x in N)-sum((len(x)-1)*r[x] for x in A)
    assert S>=0,(sig,S);vals.append(S)
p=len(Q&N);q=len(Q);t=len(T);J=comb(len(N),2);B=q-p+2*t;a=q-p
cr=7*J-B*(m-1)+t*(t-1)+a*t+a*(a-1)//2
fc=2*comb(4,2)+8*comb(p,2)-3*t*(m-1)+t*(t-1)
assert cr==-2 and fc==-33
z=dict(P=P,m=m,k=4,d=6,s=2,C=sorted(C),CR=cr,FLAT_CR=fc,
       min_slack=min(vals),sigma=vals.index(min(vals)),slacks=vals,
       elementary_profiles_below16=profiles,negative_profiles_below16=bad)
Path('adversary_min.json').write_text(json.dumps(z,indent=2)+'\n')
print('ADVERSARY_MIN',json.dumps(z,sort_keys=True))
print('ADVERSARY_MIN_PASS')
