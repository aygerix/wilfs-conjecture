"""Exact enumeration of the weighted difference collision census on integer sets."""
from itertools import combinations,combinations_with_replacement
from collections import Counter
import json

sets=0;mins=None;hole_sets=0
for n in range(2,9):
    for tail in combinations(range(1,19),n-1):
        T=(0,)+tail
        sums=Counter(x+y for x,y in combinations_with_replacement(T,2))
        diffs=Counter(x-y for x in T for y in T if x!=y)
        E=sum(g*(g-1)//2 for g in diffs.values())
        formula=0;A=0;e=0
        for S,g in sums.items():
            loop=int(S%2==0 and S//2 in T)
            formula+=4*(g*(g-1)//2)-2*loop*(g-1)
            A+=(g-1)*S;e+=g-1
        assert formula==E
        assert E<=A+e
        if 2 not in T:
            assert E<=A
            hole_sets+=1
        if mins is None or A+e-E<mins:mins=A+e-E
        sets+=1
print(json.dumps(dict(sets=sets,hole_sets=hole_sets,min_slack=mins,max_element=18,n_min=2,n_max=8)),flush=True)
