"""Residue-count obstruction for the a=17,r=5 matching tile.
Only the 5 absent pairs are required to share their residue P.
This is a structured subfamily, not a search over all matchings.
Execute only on fejer.
"""
import json
from math import comb
def comps(n,p):
    if p==1:yield (n,);return
    for x in range(n+1):
        for y in comps(n-x,p-1):yield (x,)+y
def counts(ns,p,P):
    f=[[0]*p for _ in range(4)];f[0][0]=1
    for r,n in enumerate(ns):
        for _ in range(n):
            for d in range(1,4):
                for z in range(p):f[d][(z+r)%p]+=f[d-1][z]
    out=[sum(f[d][z] for d in range(4)) for z in range(p)]
    out[P]-=5
    for r,n in enumerate(ns):out[(P+r)%p]-=5*n
    return out
for p in (2,3,5):
    good=[];tested=0
    for ns in comps(17,p):
        for P in range(p):
            cap=0
            for r in range(p):
                s=(P-r)%p
                if r==s:cap+=ns[r]//2
                elif r<s:cap+=min(ns[r],ns[s])
            if cap<5:continue
            tested+=1
            cc=counts(ns,p,P)
            assert sum(cc)==1050
            if len(set(cc))==1:good.append((ns,P))
    print(json.dumps(dict(modulus=p,tested=tested,balanced=len(good),profiles=good)),flush=True)
