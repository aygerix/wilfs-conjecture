"""Independent a=7 coverage audit, no optimistic cubic pruning. Fejer only."""
from itertools import combinations_with_replacement
from collections import Counter
import json


def run(m,rho):
    h=m-rho;L=m+h-1;top=(h-1)%m;hist=Counter();best=None
    def leaf(t,seen):
        nonlocal best
        hist['pair_sets']+=1
        triples=[sum(x) for x in combinations_with_replacement(t,3)]
        good=[v for v in triples if v<=L]
        if len(good)<m-36:return
        hist['eligible']+=1
        if L not in good:return
        hist['top_eligible']+=1
        covered=seen|{v%m for v in good}
        holes=m-len(covered)
        if best is None or holes<best['holes']:
            best=dict(t=t,holes=holes,eligible_cubics=len(good),
                      missing_residues=sorted(set(range(m))-covered))
        assert holes>0,(m,rho,t)
    def visit(t,start,seen):
        hist['nodes']+=1
        if len(t)==7:leaf(t,seen);return
        for x in range(start,h-(6-len(t))):
            added=[x%m,2*x%m]+[(x+y)%m for y in t]
            aset=set(added)
            if len(aset)!=len(added) or aset&seen or top in aset:continue
            visit(t+(x,),x+1,seen|aset)
    visit((),(h+1)//2,{0})
    print(json.dumps(dict(m=m,rho=rho,h=h,potential_W=424-4*m+rho,
                          counts=hist,best=best)),flush=True)


if __name__=='__main__':
    for m,rhos in [(107,range(4)),(108,range(8))]:
        for rho in rhos:run(m,rho)
