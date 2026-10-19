"""Independent set-based audit of the a=6,m=74 finite exception. Fejer only."""
from itertools import combinations_with_replacement
from collections import Counter
import json


def audit(rho):
    m=74;h=m-rho;L=m+h-1;hist=Counter();cases=[]
    for omitted in combinations_with_replacement(range(6),2):
        def visit(t,start,seen):
            hist['nodes']+=1;depth=len(t)
            if depth==6:
                hist['pair_sets']+=1
                good=[]
                for ijk in combinations_with_replacement(range(6),3):
                    if all(ijk.count(j)>=omitted.count(j) for j in set(omitted)):continue
                    value=sum(t[j] for j in ijk)
                    if value<=L:good.append(value)
                if len(good)<47:return
                hist['eligible']+=1
                if L not in good:return
                hist['top_eligible']+=1
                holes=sorted(set(range(m))-(seen|{v%m for v in good}))
                assert holes
                cases.append(dict(omitted=omitted,t=t,good=len(good),holes=holes))
                return
            for x in range(start,h-(5-depth)):
                sums=[x+(x if j==depth else t[j]) for j in range(depth+1) if (j,depth)!=omitted]
                if any(v<h for v in sums):continue
                residues=[x%m]+[v%m for v in sums]
                added=set(residues)
                if len(added)!=len(residues) or added&seen or h-1 in added:continue
                visit(t+(x,),x+1,seen|added)
        first=1 if omitted==(0,0) else (h+1)//2
        visit((),first,{0})
    print(json.dumps(dict(m=m,rho=rho,counts=hist,cases=cases)),flush=True)

if __name__=='__main__':
    audit(0);audit(1)
