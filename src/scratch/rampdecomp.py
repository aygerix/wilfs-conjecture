# Ramp decomposition of the Wilf-direction CL:  sum_y beta(y) R(y) >= 0, R = <phi + sigma>,
#   = T1 + T2,  T1 = sum_a sum_C L_C R(base_C) - (d-1) m(m-1)/2   (lex/supermodular part)
#              T2 = sum_a sum_C [2 sum_{c in C} R(c) - L_C (R(base_C)+R(top_C))]  (column trapezoid part)
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
for m in range(3,M+1):
    mn1=mn2=mnt=10**9; c1neg=c2neg=0; tot=0
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        cols=columns(D)
        for p in itertools.product(range(1,m),repeat=d):
            res={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
            if len(set(res.values()))!=m: continue
            for sig in range(m):
                R={z:(res[z]+sig)%m for z in Dl}
                T1=sum(len(C)*R[C[0]] for C in cols)-(d-1)*m*(m-1)//2
                T2=sum(2*sum(R[c] for c in C)-len(C)*(R[C[0]]+R[C[-1]]) for C in cols)
                tot+=1
                mn1=min(mn1,T1); mn2=min(mn2,T2); mnt=min(mnt,T1+T2)
                c1neg+=T1<0; c2neg+=T2<0
    print(f'd={d} m={m}: cases {tot}  min T1 {mn1} (neg {c1neg})  min T2 {mn2} (neg {c2neg})  min T1+T2 {mnt}',flush=True)
