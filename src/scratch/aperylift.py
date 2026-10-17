# Is every tile (D,p) an Apery tile for some lift?  Need k in R^d_{>=0} with <lam,k> > 0 for all exit vectors
# lam = z+e_a - z'  (z an a-top, z' in D the cell congruent to z+e_a).  Then p_hat = p + K*k*m (K large) makes
# V(lam) >= 0 for all exits, so V(D)+mN = <m, p_hat> and V(D) is its Apery set.
import sys, itertools
sys.path.insert(0,'src'); sys.path.insert(0,'src/scratch')
from exp_cl_tiling import downsets
from exactlp import maximize
from fractions import Fraction
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(2,M+1):
    tot=0; strict=0; zero=0; neg=0; ex=None
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        for p in itertools.product(range(1,m),repeat=d):
            res={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
            if len(set(res.values()))!=m: continue
            inv={r:n for n,r in res.items()}
            tot+=1
            Ex=set()
            for z in Dl:
                for a in range(d):
                    y=list(z); y[a]+=1; y=tuple(y)
                    if y in D: continue
                    zp=inv[(res[z]+p[a])%m]
                    Ex.add(tuple(u-v for u,v in zip(y,zp)))
            Ex=sorted(Ex)
            # LP: vars k_0..k_{d-1}, tp, tm, slack per lam, slack for sum
            nE=len(Ex); nv=d+2+nE+1
            A=[];b=[]
            for i,lam in enumerate(Ex):
                row=[Fraction(0)]*nv
                for a in range(d): row[a]=Fraction(lam[a])
                row[d]=Fraction(-1); row[d+1]=Fraction(1); row[d+2+i]=Fraction(-1)
                A.append(row); b.append(Fraction(0))
            row=[Fraction(0)]*nv
            for a in range(d): row[a]=Fraction(1)
            row[nv-1]=Fraction(1); A.append(row); b.append(Fraction(1))
            c=[Fraction(0)]*nv; c[d]=Fraction(1); c[d+1]=Fraction(-1)
            val,x=maximize(c,A,b)
            if val=='unbounded': val=Fraction(10**9)
            if val>0: strict+=1
            elif val==0: zero+=1
            else:
                neg+=1
                if ex is None: ex=(Dl,p,Ex,val)
    print(f'd={d} m={m}: tiles {tot}, strict {strict}, borderline {zero}, impossible {neg}', ex if ex else '',flush=True)
