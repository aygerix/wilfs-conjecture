"""Independent Python certificate: only missing-count pruning, no A pruning.

In contrast to one_small.c, this enumerates every possible complete core
in each base, then computes the best possible slack. Run on fejer only.
"""
from itertools import combinations_with_replacement
from math import comb
import json

out=[]
for k,e in ((6,3),(7,3),(6,4),(7,4),(8,4),(9,4)):
    m=k+comb(k+1,2)+2-e
    counts=dict(nodes=0,pruned=0,leaves=0,complete=0);minS=None
    def visit(U,pool,start,u,rho):
        global minS
        counts['nodes']+=1
        nu=m-rho;yr=m-u+4
        blocked={rho,yr,*U};groups={}
        for x,y in combinations_with_replacement(U,2):
            w=x+y-rho;r=w%m
            if r in blocked or w>=m or (r>=nu and w>=0):continue
            if r==2 and (x!=u or y!=u):continue
            groups[r]=max(groups.get(r,-1),x+y)
        missing=comb(len(U)+1,2)-len(groups)
        if missing>e:counts['pruned']+=1;return
        if len(U)==k:
            counts['leaves']+=1
            if len(groups)!=m-k-2:return
            counts['complete']+=1
            A=(k+1)*sum(U)-sum(groups.values())
            S=A+2*(k-1)-m
            if minS is None or S<minS:minS=S
            assert S>=0,dict(m=m,k=k,e=e,U=U,u=u,rho=rho,A=A,S=S)
            return
        for j in range(start,len(pool)-(k-len(U))+1):
            visit(U+[pool[j]],pool,j+1,u,rho)
    for u in range(5,(m+3)//4+1):
        rho=2*u-2
        pool=[r for r in range(3,m-rho) if r not in (rho,u)]
        visit([0,1,u],pool,0,u,rho)
    row=dict(k=k,e=e,m=m,counts=counts,minS=minS)
    print(json.dumps(row),flush=True);out.append(row)
print('PASS independent Python certificate',flush=True)
with open('one_small_check.json','w') as f:json.dump(out,f,indent=2)
