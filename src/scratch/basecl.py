# Base-CL: bslack(sigma) = (sum_a sum_C L_C <phi(base_C)+sigma> - (d-1)m(m-1)/2)/m.  Range? integrality?
# Compare with top-slack tslack(sigma) = ((d+1)m(m-1)/2 - sum_a sum_C L_C <phi(top_C)+sigma>)/m  (Tile-CL: in [0,m-1]).
import sys, itertools
from fractions import Fraction
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2])
def columns(D):
    cols=[]
    for a in range(d):
        for x in D:
            if x[a]!=0: continue
            C=[x]; y=list(x)
            while True:
                y[a]+=1
                if tuple(y) not in D: break
                C.append(tuple(y))
            cols.append(C)
    return cols
for m in range(3,M+1):
    lo=hi=None; nonint=0; tot=0; rel=set()
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        cols=columns(D)
        for p in itertools.product(range(1,m),repeat=d):
            res={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
            if len(set(res.values()))!=m: continue
            bs=[];ts=[]
            for sig in range(m):
                B=sum(len(C)*((res[C[0]]+sig)%m) for C in cols)-(d-1)*m*(m-1)//2
                T=(d+1)*m*(m-1)//2-sum(len(C)*((res[C[-1]]+sig)%m) for C in cols)
                b=Fraction(B,m); t=Fraction(T,m)
                bs.append(b); ts.append(t)
                tot+=1
                if b.denominator!=1: nonint+=1
                lo=b if lo is None or b<lo else lo; hi=b if hi is None or b>hi else hi
            # relation: is sorted base-slack vector a permutation-type? record (sum)
            rel.add((sum(bs)==Fraction(m*(m-1),2)))
    print(f'd={d} m={m}: cases {tot} base-slack range [{lo},{hi}] (m-1={m-1}) nonintegral {nonint}  sum=m(m-1)/2 always: {rel}',flush=True)
