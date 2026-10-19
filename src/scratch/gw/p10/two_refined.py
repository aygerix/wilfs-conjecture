#!/usr/bin/env python3
"""Finite support-two certificate, retaining face antichain sizes."""
from boundary import degree_floor,axis_floor
import json,math

def parts(n,k,lo=0):
    if k==1:
        if n>=lo:yield (n,)
        return
    for a in range(lo,n//k+1):
        for b in parts(n-a,k-1,a):yield (a,)+b

def main():
    mx=143; cache={};pc=0
    for t2 in range(math.isqrt(12*mx)+1):
        vals=[]
        for a in parts(t2,6):
            vol=sum(v*(v+1)//2 for v in a)
            if vol>mx-5:continue
            weights=sorted((v+5 for v in a for j in range(v)),reverse=True)
            R=sum(i*w for i,w in enumerate(weights)); vals.append((vol,R));pc+=1
        for n2 in range(mx):
            rr=[R for v,R in vals if v<=n2]
            if rr:cache[t2,n2]=min(rr)
    tested=0;surv=[];minclear=None
    for m in range(64,144):
        rows=[]
        for n2 in range(m-4):
            n1=m-1-n2;base=degree_floor(n2,2,6)+axis_floor(n1,n2)
            for t1 in range(5):
                for t2 in range(math.isqrt(12*n2)+1):
                    if (t2,n2) not in cache:continue
                    tested+=1
                    H=max(base,0,(12*m-15*t1-24*t2+3)//4)
                    R=cache[t2,n2]+5*(t2*t1+t1*(t1-1)//2)
                    slack=(m+1)*H+R-3*m*(m-1)//2
                    if minclear is None or slack<minclear[0]:minclear=[slack,m,n1,n2,t1,t2,H,R]
                    if slack<0:rows.append([n1,n2,t1,t2,H,R,slack])
        if rows:surv.append([m,len(rows),rows[:8]])
    print(json.dumps(dict(partitions=pc,tested=tested,minclear=minclear,survivors=surv)))

if __name__=='__main__':main()
