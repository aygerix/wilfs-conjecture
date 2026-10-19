#!/usr/bin/env python3
"""Exact data for failed extensions. These are down-sets, not semigroups."""
import itertools,json
from boundary import stats,degree_floor

for h in range(1,9):
    for boundary in [False,True]:
        D={x for x in itertools.product(range(h+1),repeat=4)
           if sum(x)<=h and (not boundary or 0 in x)}
        H,t,n,ht,local=stats(D);m=len(D)
        data=dict(degree=h,boundary=boundary,m=m,H=H,t=t,n=n,
                  BH2x6=6*H-12*m+15*t[1]+20*t[2]+36*t[3],
                  pair_degree_floor=degree_floor(n[2],2,6),
                  H_plus_3t_minus_2m=H+3*sum(t)-2*m)
        print(json.dumps(data))
        if h==3:
            assert m==35 and H==0 and n[2]==18
            assert degree_floor(n[2],2,6)==12
        if h==4 and boundary:assert (m,H,n[2])==(69,4,36)
        if h==5 and not boundary:assert data['BH2x6']==-108
