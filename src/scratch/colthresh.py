# Check: slack(s) = sum_C H_C(tau_C) - sum_C H_C(kappa_C), H_C(t) = #{1<=i<L_C : <i p_a> >= t},
# tau_C = <phi(top_C) - s - 1> + 1,  kappa_C = m - <sum_{b>a} (base_C)_b p_b>   (lex order), all in [1,m].
import sys, itertools
from fractions import Fraction
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
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
            cols.append((a,C))
    return cols
for m in range(3,M+1):
    bad=0; tot=0
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        T=Tvals(D,d); cols=columns(D)
        for p in itertools.product(range(1,m),repeat=d):
            res={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
            if len(set(res.values()))!=m: continue
            for s in range(m):
                tot+=1
                sl=Fraction(sum(T[z]*((s-res[z])%m) for z in Dl)-(d-1)*m*(m-1)//2,m)
                val=0
                for a,C in cols:
                    L=len(C); H=lambda t: sum(1 for i in range(1,L) if (i*p[a])%m>=t)
                    tau=(res[C[-1]]-s-1)%m+1
                    kap=m-(sum(C[0][b]*p[b] for b in range(a+1,d))%m)
                    val+=H(tau)-H(kap)
                if val!=sl: bad+=1
    print(f'd={d} m={m}: cases {tot}, mismatches {bad}',flush=True)
