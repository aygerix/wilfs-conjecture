import sys, itertools
sys.path.insert(0,'src'); sys.path.insert(0,'src/scratch')
from exp_cl_tiling import Tvals
from exactlp import feasible
from fractions import Fraction as Fr
d=2; m=8
Dl=[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)]; p=(5,7)
S=set(Dl); T=Tvals(S,d); tgt=(d-1)*m*(m-1)//2
ph={x:sum(a*b for a,b in zip(x,p))%m for x in Dl}
sl=[(sum(T[x]*((s-ph[x])%m) for x in Dl)-tgt)//m for s in range(m)]
print('slack',sl,'sorted',sorted(sl),'phi',ph)
# all-arc LP; verify solution if feasible on a perturbed (known feasible) rhs
cells=[z for z in Dl if any(z)]
cols=[];owner=[]
for zi,z in enumerate(cells):
    for st in range(m):
        cols.append(frozenset((st+k)%m for k in range(ph[z]))); owner.append(zi)
rows=[[1 if owner[j]==zi else 0 for j in range(len(cols))] for zi in range(len(cells))]
rows+=[[1 if s in cols[j] else 0 for j in range(len(cols))] for s in range(m)]
x=feasible(rows,[1]*len(cells)+sl); print('LP anyarc feasible?',x is not None)
# a random known-feasible rhs: pick rotation 0 for all
rhs=[sum(1 for zi in range(len(cells)) if s in cols[zi*m]) for s in range(m)]
x=feasible(rows,[1]*len(cells)+rhs); print('control feasible?',x is not None, 'check', all(sum(r[j]*x[j] for j in range(len(cols)))==b for r,b in zip(rows,[1]*len(cells)+rhs)))
# Farkas-style check by brute force: integer solutions? (each cell picks one rotation)
import itertools
cnt=0
lens=[ph[z] for z in cells]
best=None
for rots in itertools.product(range(m),repeat=len(cells)):
    cov=[0]*m
    for l,st in zip(lens,rots):
        for k in range(l): cov[(st+k)%m]+=1
    if cov==sl: cnt+=1; break
print('integer arc solutions found:',cnt)
