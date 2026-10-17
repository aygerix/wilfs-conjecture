# With fixed u*(r) = s*[r==0] + [r>s], is max_{down-sets U in R} sum_U (gamma - u*(phi)) <= 0 ?
# Max-weight closure via LP over the down-set (order) polytope: max sum w_z x_z, 0<=x<=1, x_z<=x_{z-e_a}  (integral, TU).
import sys, itertools
sys.path.insert(0,'src/scratch')
from exactlp import maximize
from math import gcd
d=int(sys.argv[1]); m=int(sys.argv[2]); mode=sys.argv[3] if len(sys.argv)>3 else 'upper'
def region(m):
    R=[]
    def rec(pref,prod):
        if len(pref)==d: R.append(tuple(pref)); return
        k=0
        while prod*(k+1)<=m:
            rec(pref+[k],prod*(k+1)); k+=1
    rec([],1); return R
R=region(m); idx={z:i for i,z in enumerate(R)}
down=[(z,a) for z in R for a in range(d) if z[a]>=1]
n=2*len(R)+len(down)
A=[];b=[]
for i in range(len(R)):           # x_i + y_i = 1
    row=[0]*n; row[i]=1; row[len(R)+i]=1; A.append(row); b.append(1)
for k,(z,a) in enumerate(down):   # x_z - x_{z-e_a} + t = 0
    row=[0]*n; row[idx[z]]=1; w=list(z); w[a]-=1; row[idx[tuple(w)]]=-1; row[2*len(R)+k]=1; A.append(row); b.append(0)
tot=bad=0; ex=[]
for p in itertools.product(range(1,m),repeat=d):
  if gcd(m,*p)!=1: continue
  for s in range(m):
    w=[]
    for z in R:
        V=sum(a*b for a,b in zip(z,p)); ph=V%m
        gz=sum(z[a] for a in range(d) if (ph-1-s)%m<p[a])-V//m
        if mode=='upper': u=(s if ph==0 else 0)+(1 if ph>s else 0); w.append(gz-u)
        else:  # lower bound: sum_U gamma >= sum_U l(phi) with l(r) = -(m-1-s)[r==0] + [r>s]... test l = [r>s] - (m-1-s)[r==0]
            l=(1 if ph>s else 0)-((m-1-s) if ph==0 else 0); w.append(l-gz)
    val,x=maximize(w+[0]*(n-len(R)),A,b)
    tot+=1
    if val>0:
        bad+=1
        if len(ex)<4:
            U=[R[i] for i in range(len(R)) if x[i]==1]
            ex.append((p,s,str(val),U))
print('d',d,'m',m,mode,'(p,s)',tot,'max-closure > 0 in',bad)
for e in ex: print('   ',e)
