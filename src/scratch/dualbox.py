# Dual certificate on the box-injective region R'(p): u (free), f>=0; minimize total flow among optimal.
# Print u by residue and flows; also print the region R' (maximal elements).
import sys, itertools
sys.path.insert(0,'src/scratch')
from exactlp import maximize
from math import prod
d=int(sys.argv[1]); m=int(sys.argv[2]); p=tuple(int(x) for x in sys.argv[3].split(',')); S=[int(x) for x in sys.argv[4].split(',')]
mode=sys.argv[5] if len(sys.argv)>5 else 'upper'
def region(m):
    R=[]
    def rec(pref,pr):
        if len(pref)==d: R.append(tuple(pref)); return
        k=0
        while pr*(k+1)<=m:
            rec(pref+[k],pr*(k+1)); k+=1
    rec([],1); return R
R=[z for z in region(m) if len({sum(x*y for x,y in zip(w,p))%m for w in itertools.product(*[range(c+1) for c in z])})==prod(c+1 for c in z)]
Rs=set(R)
maxl=[z for z in R if all(tuple(z[:a]+(z[a]+1,)+z[a+1:]) not in Rs for a in range(d))]
print('maximal elements of R\'(p):',maxl)
E=[(z,a) for z in R for a in range(d) if z[a]>=1]
phi={z:sum(a*b for a,b in zip(z,p))%m for z in R}
for s in S:
    g={}
    for z in R:
        V=sum(a*b for a,b in zip(z,p)); ph=V%m
        g[z]=sum(z[a] for a in range(d) if (ph-1-s)%m<p[a])-V//m
    if mode=='lower': g={z:-v for z,v in g.items()}
    target=(m-1) if mode=='upper' else 0
    nv=2*m+len(E)+len(R); A=[];b=[]
    A.append([1]*m+[-1]*m+[0]*(len(E)+len(R))); b.append(target)
    for zi,z in enumerate(R):
        row=[0]*nv; r=phi[z]; row[r]+=1; row[m+r]-=1
        for k,(w,a) in enumerate(E):
            if w==z: row[2*m+k]+=1
            zz=list(w); zz[a]-=1
            if tuple(zz)==z: row[2*m+k]-=1
        row[2*m+len(E)+zi]=-1; A.append(row); b.append(g[z])
    val,x=maximize([0]*(2*m)+[-1]*len(E)+[0]*len(R),A,b)
    if val is None: print('s',s,'no certificate at target'); continue
    u=[x[r]-x[m+r] for r in range(m)]
    print(f's={s} flow {-val} u(r):',' '.join(str(v) for v in u))
    for k,(z,a) in enumerate(E):
        if x[2*m+k]!=0:
            zz=list(z); zz[a]-=1; print(f'     {tuple(zz)}->{z}: {x[2*m+k]}  gamma={g[z]}')
