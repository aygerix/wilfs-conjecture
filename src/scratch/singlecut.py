# Single-cut lemma test: D down-set, H nonempty up-set of D. X(H) = sum_a #{x in D\H : top_a(x) in H} <= |D|-1 ?
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2])
def tops(D,d):
    t={}
    for x in D:
        for a in range(d):
            y=list(x)
            while tuple(y[:a]+[y[a]+1]+y[a+1:]) in D: y[a]+=1
            t[(x,a)]=tuple(y)
    return t
for m in range(2,M+1):
    worst=-10**9; ex=None; cnt=0
    for D in downsets(m,d):
        Dl=sorted(D); tp=tops(D,d)
        # enumerate up-sets via complements of sub-down-sets: H = D \ E, E down-set subset of D
        Dset=set(Dl)
        # generate all down-subsets E of D by brute force over subsets (m small)
        for mask in range(1,1<<m):
            H={Dl[i] for i in range(m) if mask>>i&1}
            # H up-set in D?
            ok=all((tuple(x[b]+(b==a) for b in range(d)) not in Dset) or (tuple(x[b]+(b==a) for b in range(d)) in H) for x in H for a in range(d))
            if not ok: continue
            cnt+=1
            X=sum(1 for x in Dl if x not in H for a in range(d) if tp[(x,a)] in H)
            if X-(m-1)>worst: worst=X-(m-1); ex=(Dl,sorted(H),X)
    print(d,m,'upsets',cnt,'max X-(m-1)',worst, ex if worst>0 else '',flush=True)
