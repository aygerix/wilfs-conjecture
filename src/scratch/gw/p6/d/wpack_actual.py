"""Check the cyclic collision census and conditional WDP on actual cores.

One budget-one test is added to independently generated cores; all arithmetic
is exact. This is an audit, not an exhaustive proof of arbitrary tiles.
"""
from itertools import combinations_with_replacement as cwr
from collections import defaultdict,Counter
from math import comb
import random,json
from core import evaluate,optimal_one
from window_h import random_core

rng=random.Random(2026101971);stats=Counter();smallest=None
def check(m,P,Q,T,sig):
    global smallest
    rho=(-sig)%m;U=[(p-sig)%m for p in P]
    ans=evaluate(m,U,Q,T,rho);k=len(U);e=ans['e']
    V=[rho]+U
    diffs=Counter((x-y)%m for x in V for y in V if x!=y)
    Ec=sum(comb(g,2) for g in diffs.values())
    allpairs=list(cwr(range(k+1),2));groups=defaultdict(list)
    for i,j in allpairs:groups[(V[i]+V[j])%m].append((i,j))
    Dtot=0;A=0;absents=0;omega=0;unwrapped=True
    for pairs in groups.values():
        miss=[(i,j) for i,j in pairs if i and j and tuple(sorted((i-1,j-1))) not in Q]
        j=len(miss);g=len(pairs);ell=sum(i==h for i,h in pairs)
        D=4*comb(g,2)-2*ell*(g-1)+comb(ell,2)
        cost=sum(V[i]+V[h] for i,h in miss)
        assert g-j<=1
        Dtot+=D;A+=cost;absents+=j
        omega+=max(0,D-cost-j)
        if j and len({V[i]+V[h] for i,h in pairs})>1:unwrapped=False
    assert A==ans['A'] and absents==e
    assert Ec<=Dtot
    assert m-1>=k*(k+1)-Ec
    assert A>=k*(k+1)-m+1-e-omega
    stats['phases']+=1
    if unwrapped:
        assert Ec<=A+e
        if 2 not in V:assert Ec<=A
        stats['unwrapped']+=1
    credits=ans['Orest']+ans['Pplus']+ans['gain']+ans['PAplus']
    if ans['beta']<=1:
        N2={z for z in Q if any(tuple(sorted(z+(i,))) in T for i in range(k))}
        weights=sorted([k+ans['s']+2-sum(z.count(i)+1 for i in range(k) if tuple(sorted(z+(i,))) in T)
                        for z in N2],reverse=True)
        Gamma=sum(j*w for j,w in enumerate(weights))
        condition=ans['s']*(comb(k,2)-2)+Gamma+e-2*k-2*len(T)-1
        if condition>=0:
            assert ans['S']>=0;stats['ONE_BAD_SHAPE']+=1
        if N2:
            rr=min((sum(U[i] for i in z)-rho)%m for z in N2)
            if rr<rho:
                low_condition=condition+rr*sum(weights)+(e if rr==2 else 0)
                if low_condition>=0:
                    assert ans['HC']>=0;stats['ONE_BAD_LOWPAIR']+=1
    if len(T)==1 and ans['OW']+ans['B']==-1 and A<m:
        assert Ec<=A+e
        N2={z for z in Q if any(tuple(sorted(z+(i,))) in T for i in range(k))}
        rmin=min((sum(U[i] for i in z)-rho)%m for z in N2)
        if rmin==2:assert Ec<=A
        stats['ONE_WEIGHTED']+=1
        if not ans['PAplus']:
            assert unwrapped
            stats['ONE_UNWRAPPED']+=1
    assert ans['S']>=0

# A named A<m deficit, so the conditional weighted branch is exercised.
# Unit residues (0,1,3,5), rho=8, original labels are U-rho modulo 17.
check(17,[9,10,12,14],{(0,0),(0,1),(1,1),(0,2),(1,2),(0,3),(1,3),(3,3)},
      {(3,3,3)},9)
for rep in range(2500):
    m=rng.randrange(10,101);k=rng.randrange(2,min(10,m-1)+1)
    P=sorted(rng.sample(range(1,m),k));made=random_core(rng,m,P,3)
    if made is None:continue
    C,P=made;Q={z for z in C if len(z)==2};T={z for z in C if len(z)==3}
    for sig in range(m):check(m,P,Q,T,sig)
    stats['cores']+=1
print(json.dumps(dict(seed=2026101971,stats=stats),sort_keys=True),flush=True)
