"""Exact exhaustive retained-pair graph checks. fejer only."""
from collections import Counter
from itertools import combinations, combinations_with_replacement
from math import comb

def matchings(vertices):
    if not vertices:
        yield frozenset(); return
    x,*tail=vertices
    for M in matchings(tail):
        yield M
    for y in tail:
        for M in matchings([z for z in tail if z!=y]):
            yield M|{(min(x,y),max(x,y))}

counts={}; nonweak=nonzero_v=nonzero_illegal=0
for n in range(2,8):
    Ms=list(matchings(list(range(n))))
    states=0; sets=0
    for tail in combinations(range(1,15),n-1):
        B=(0,)+tail
        off=list(combinations(range(n),2))
        fibres={}
        for e in off:
            fibres.setdefault(B[e[0]]+B[e[1]],[]).append(e)
        valid=[]
        for M in Ms:
            if all(sum(e not in M for e in es)<=1 for es in fibres.values()):
                valid.append(M)
        if not valid: continue
        sets+=1
        sf=Counter(sum(B[i] for i in T) for T in combinations(range(n),3))
        repeated=Counter(2*x+y for x in B for y in B)
        rp=sum(comb(v,2) for v in repeated.values())
        fr=sum(v*repeated[t] for t,v in sf.items())
        fp=sum(comb(v,2) for v in sf.values())
        sfex=sum(v-1 for v in sf.values())
        G=max(sf.values(),default=1)
        dif=Counter(B[i]-B[j] for i in range(n) for j in range(i))
        signed=set(B)|{B[i]+B[j]-B[k] for i in range(n) for j in range(i,n) for k in range(n) if i!=k and j!=k}
        H=n*(comb(n,2)+1);loss=H-len(signed)
        for M in valid:
            states+=1;r=len(M);D=1 if r else 0
            legal=Counter(sum(B[i] for i in T) for T in combinations(range(n),3) if not any(e in M for e in combinations(T,2)))
            v=sum(c-1 for c in legal.values())
            nonzero_v+=v>0;nonzero_illegal+=r>0
            nonweak+=any(len(es)>1 for es in fibres.values())
            assert max(dif.values(),default=0)<=2*D+2
            assert rp<=(2*D+2)*comb(n,2)
            proper=Counter(B[i]+B[j]-B[k] for i,j in off if (i,j) not in M for k in range(n) if k!=i and k!=j)
            cp=sum(comb(c,2) for c in proper.values())
            overlap=sum(proper[x] for x in B)
            assert overlap<=(D+1)*n
            assert cp<=9*fp+6*fr+4*rp
            assert sfex<=v+r*(n-2)
            assert loss<=n*(n-1)+r*(n-2)+cp+overlap
            assert 2*loss<=9*G*v+(9*G+2)*r*(n-2)+2*(6*G+4*D+5)*n*n-2*(3*D+4)*n
            # A stronger retained version caps only LEGAL SF fibres. The
            # ordinary SF fibres caused by absent pairs may be arbitrarily large.
            Glegal=max(legal.values(),default=1)
            centres=Counter(B[i]+B[j] for i,j in M)
            eta=sum(comb(c,2) for c in centres.values())
            dd=2*D+2
            rhs2=9*Glegal*v+2*(6*Glegal+4*D+5)*n*n
            rhs2+=2*(9*Glegal+6*dd+7)*n*r+18*dd*comb(r,2)+18*n*eta
            rhs2-=2*(3*D+4)*n+4*r
            assert 2*loss<=rhs2
    counts[n]=(sets,states)
    print('n',n,'sets',sets,'retained_graph_states',states,flush=True)
print('nonweak_states',nonweak,'nonzero_v',nonzero_v,'nonzero_illegal',nonzero_illegal)
print('ALL_MATCHING_CHECKS_PASSED',counts)
