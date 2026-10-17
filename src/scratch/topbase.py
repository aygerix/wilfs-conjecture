# Relation between Top-slack and Base-slack vectors.  For each tile (D,p): top(s) and base(sigma) vectors.
# (1) Is base-vector of (D,p) equal (up to rotation and/or reversal) to the top-vector of some tile (D',p') of same m,d?
# (2) Q-CL: Q(w) = sum_C L_C [w in arc(base_C, top_C]]  fluctuation.
import sys, itertools
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
def canon(v):
    m=len(v); cands=[]
    for w in (v, v[::-1]):
        for k in range(m): cands.append(tuple(w[k:]+w[:k]))
    return min(cands)
for m in range(3,M+1):
    tops=set(); bases=set(); qmax=0
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        cols=columns(D)
        for p in itertools.product(range(1,m),repeat=d):
            res={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
            if len(set(res.values()))!=m: continue
            A_top=[sum(1 for C in cols for i,x in enumerate(C) if (res[C[-1]]+sg)%m < (res[x]+sg)%m) for sg in range(m)]
            A_base=[sum(1 for C in cols for i,x in enumerate(C) if (res[C[0]]+sg)%m > (res[x]+sg)%m) for sg in range(m)]
            t=[a-min(A_top) for a in A_top]; b=[a-min(A_base) for a in A_base]
            tops.add(canon(t)); bases.add(canon(b))
            Q=[sum(len(C) for C in cols if len(C)>1 and ((res[C[-1]]-res[C[0]])%m) >= ((w-res[C[0]])%m) and (w-res[C[0]])%m>0) for w in range(m)]
            qmax=max(qmax,max(Q)-min(Q))
    print(f'd={d} m={m}: distinct top-shapes {len(tops)}, base-shapes {len(bases)}, base not in top {len(bases-tops)}, top not in base {len(tops-bases)}; max Q range {qmax} (m-1={m-1})',flush=True)
