# Single-cut lemma test: D' any down-set in N^d, phat positive, V injective on D'.
# E = {V <= s}; F(E) = #{(w,a): w in E, top_a w notin E}.  Claim: F(E) <= s + |D'\E|.
# Also record the tighter quantity F(E) - |D'\E| - (max V(E)) etc.
import sys, itertools, random
from math import prod
def downsets(d, N):
    # all down-sets of size N in N^d (generate by adding minimal-addable cells; canonical via frozenset)
    seen={frozenset([tuple([0]*d)])}; frontier=list(seen)
    for k in range(1,N):
        new=set()
        for S in frontier:
            for z in S:
                for a in range(d):
                    y=list(z); y[a]+=1; y=tuple(y)
                    if y in S: continue
                    if all(y[b]==0 or tuple(y[:b]+(y[b]-1,)+y[b+1:]) in S for b in range(d)):
                        new.add(S|{y})
        frontier=list(new)
    return frontier
def F(D,E,d):
    cnt=0
    for w in E:
        for a in range(d):
            t=list(w)
            while True:
                t[a]+=1
                if tuple(t) not in D: break
            t[a]-=1
            if tuple(t) not in E: cnt+=1
    return cnt
d=int(sys.argv[1]); N=int(sys.argv[2]); P=int(sys.argv[3])
worst=None; viol=0; tot=0
for D in downsets(d,N):
    for ph in itertools.product(range(1,P+1),repeat=d):
        V={z:sum(a*b for a,b in zip(z,ph)) for z in D}
        if len(set(V.values()))<len(D): continue
        vals=sorted(V.values())
        for s in range(-1,max(vals)+1):
            E={z for z in D if V[z]<=s}
            f=F(D,E,d); rhs=s+len(D)-len(E)
            tot+=1
            ex=f-rhs
            if worst is None or ex>worst[0]: worst=(ex,sorted(D),ph,s,f,rhs)
            if ex>0: viol+=1
print('d',d,'N',N,'P',P,'tests',tot,'viol',viol,'worst',worst)
