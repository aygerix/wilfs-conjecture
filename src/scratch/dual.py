# Dual certificate for max over down-set transversals: u (class potentials), f>=0 upward edge flow,
#   u[phi(z)] + in(z) - out(z) >= gamma(z)  for z in R,  sum u = m-1 ; among these minimize total flow.
import sys, itertools
sys.path.insert(0,'src/scratch')
from exactlp import maximize
from fractions import Fraction as Fr
d=int(sys.argv[1]); m=int(sys.argv[2]); p=tuple(int(x) for x in sys.argv[3].split(',')); S=[int(x) for x in sys.argv[4].split(',')]
mode=sys.argv[5] if len(sys.argv)>5 else 'upper'
def region(m):
    R=[]
    def rec(pref,prod):
        if len(pref)==d: R.append(tuple(pref)); return
        k=0
        while prod*(k+1)<=m:
            rec(pref+[k],prod*(k+1)); k+=1
    rec([],1); return R
def gam(z,s):
    V=sum(a*b for a,b in zip(z,p)); ph=V%m
    return sum(z[a] for a in range(d) if (ph-1-s)%m<p[a])-V//m
R=region(m); E=[(z,a) for z in R for a in range(d) if z[a]>=1]
phi={z:sum(a*b for a,b in zip(z,p))%m for z in R}
for s in S:
    g={z:gam(z,s) for z in R}
    if mode=='lower': g={z:-v for z,v in g.items()}
    target=(m-1) if mode=='upper' else 0
    # variables: u+ (m), u- (m), f (|E|), slack (|R|)
    nv=2*m+len(E)+len(R)
    A=[];b=[]
    A.append([1]*m+[-1]*m+[0]*(len(E)+len(R))); b.append(target)
    for zi,z in enumerate(R):
        row=[0]*nv; r=phi[z]; row[r]+=1; row[m+r]-=1
        for k,(w,a) in enumerate(E):
            if w==z: row[2*m+k]+=1            # inflow into z on edge (z-e_a -> z)
            zz=list(w); zz[a]-=1
            if tuple(zz)==z: row[2*m+k]-=1    # outflow from z
        row[2*m+len(E)+zi]=-1
        A.append(row); b.append(g[z])
    c=[0]*(2*m)+[-1]*len(E)+[0]*len(R)
    val,x=maximize(c,A,b)
    if val is None: print('s',s,'INFEASIBLE (bound not provable by LP at target',target,')'); continue
    u=[x[r]-x[m+r] for r in range(m)]
    f={E[k]:x[2*m+k] for k in range(len(E)) if x[2*m+k]!=0}
    print(f's={s} total flow {-val}  u by residue r:',[str(v) for v in u])
    print('     u by offset (r-s-1)%m:',[str(u[(s+1+o)%m]) for o in range(m)])
    for (z,a),v in sorted(f.items()):
        zz=list(z); zz[a]-=1
        print(f'     flow {tuple(zz)}->{z} dir{a}: {v}   gamma(z)={g[z]} phi(z)={phi[z]}')
