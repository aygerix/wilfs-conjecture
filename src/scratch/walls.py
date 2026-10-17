"""Per-wall excess E_j = |U_j| - dU_j, U_j = {y in D: sigma + N0(y) >= j m}, dU_j = sum_a #{x notin U_j: top_a x in U_j}.
CL: sum_j E_j <= sigma.  Look for a per-wall bound that telescopes."""
import sys, itertools, random
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
def tops(D,d):
    top={}
    for n in D:
        for a in range(d):
            x=list(n)
            while tuple(x[:a]+[x[a]+1]+x[a+1:]) in D: x[a]+=1
            top[(n,a)]=tuple(x)
    return top
d=int(sys.argv[1]); m=int(sys.argv[2]); random.seed(1)
stats={'Ej<=0 for j>=2':0,'cases':0}
shown=0
for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    top=tops(D,d)
    for p in itertools.product(range(m),repeat=d):
        N0={n:sum(x*y for x,y in zip(n,p)) for n in Dl}
        if len({v%m for v in N0.values()})!=m: continue
        for sg in range(m):
            N={n:sg+N0[n] for n in Dl}
            J=max(N.values())//m
            E=[]
            for j in range(1,J+1):
                U={n for n in Dl if N[n]>=j*m}
                dU=sum(1 for (n,a),t in top.items() if n not in U and t in U)
                E.append(len(U)-dU)
            stats['cases']+=1
            if all(e<=0 for e in E[1:]): stats['Ej<=0 for j>=2']+=1
            if J>=3 and shown<12 and random.random()<0.02:
                shown+=1; print('p',p,'sigma',sg,'E_j',E,'sum',sum(E),'<=',sg, 'D',Dl)
print(stats)
