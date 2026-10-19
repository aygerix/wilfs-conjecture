#!/usr/bin/env python3
"""Exact count relaxation for support-at-most-two down-sets in N^4."""
import json,math
from boundary import degree_floor,axis_floor

def main():
    tested=0; survivors=[]; margin=None
    for m in range(40,225):
        rows=[]
        for n2 in range(m-4):
            n1=m-1-n2
            base=degree_floor(n2,2,6)+axis_floor(n1,n2)
            for t1 in range(5):
                for t2 in range(math.isqrt(12*n2)+1):
                    if t2*t2+6*t2>12*n2:continue
                    tested+=1
                    hb=max(base,0,(12*m-15*t1-24*t2+3)//4)
                    R=6*t2*(t2-1)//2+5*(t2*t1+t1*(t1-1)//2)
                    slack=(m+1)*hb+R-3*m*(m-1)//2
                    if margin is None or slack<margin[0]:margin=[slack,m,n1,n2,t1,t2,hb,R]
                    if slack<0:rows.append([n1,n2,t1,t2,hb,R,slack])
        if rows:survivors.append([m,len(rows),rows[:12]])
    print(json.dumps(dict(tested=tested,min_margin=margin,survivors=survivors)))

if __name__=='__main__':main()
