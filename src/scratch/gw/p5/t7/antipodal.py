"""Exact family refuting the SUPPORT version of MATCH-P, not ambient MATCH-P.
Run on fejer. Base-ten dominance proves the statements for every k.
"""
from collections import Counter
from itertools import combinations_with_replacement
from math import comb
for k in range(2,19):
    B=[a*10**i for i in range(k) for a in (-1,1)]
    n=2*k;H=n*(comb(n,2)+1)
    pairs=Counter(x+y for x,y in combinations_with_replacement(B,2))
    assert pairs[0]==k and all(v==1 for t,v in pairs.items() if t!=0)
    cubes=Counter(sum(T) for T in combinations_with_replacement(B,3))
    legal=Counter(sum(T) for T in combinations_with_replacement(B,3) if not any(-x in T for x in T))
    assert all(v==1 for v in legal.values())
    assert all(cubes[x]==k for x in B)
    assert all(v==1 for t,v in cubes.items() if t not in B)
    ex=comb(n+2,3)-len(cubes)
    assert ex==2*k*(k-1)
    signed=set(B)|{x+y-z for x,y in combinations_with_replacement(B,2) for z in B if z!=x and z!=y}
    assert signed==set(cubes)
    loss=H-len(signed)
    assert 3*loss==2*k*(k-1)*(4*k+1)
    s=max(B)-min(B)+1;assert s==2*10**(k-1)+1
    assert 3*s-2>=H
    print('k',k,'n',n,'r',k,'v',0,'s',s,'H',H,'ex',ex,'signed',len(signed),'loss',loss)
# Smallest member refuting the support bound with K=47.
def ratio_num(k):return 2*k*(k-1)*(4*k+1)
for k in range(2,10000):
    if ratio_num(k)>3*47*6*k*k:
        assert k==107
        print('FIRST_K47_SUPPORT_FAILURE',k,'loss',ratio_num(k)//3,'Kbudget',47*6*k*k)
        break
print('ANTIPODAL_EXACT_CHECKS_PASSED')
