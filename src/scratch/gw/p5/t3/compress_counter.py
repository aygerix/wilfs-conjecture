"""Compress a fixed-arc counterexample within one residue-order cone.

All execution is on fejer. HiGHS is restricted to one thread. This
proves no global minimum; the exact integer output is independently
verified as a numerical-semigroup Apéry tile by verify_saved.py.
"""
from itertools import combinations_with_replacement
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
import json

src=json.loads(Path('tile_fixed_negative.json').read_text());m0=src['m'];h0=src['h']
t0=sorted(z-m0 for z in src['weights'] if z< m0+h0)[:7]
a=len(t0);assert a==7
D=[()]+[x for dg in range(1,4) for x in combinations_with_replacement(range(a),dg)]
ks={x:sum(t0[j] for j in x)//m0 for x in D}
order=sorted(D,key=lambda x:sum(t0[j] for j in x)%m0)
N=a+2;mi=a;hi=a+1
rows=[];lbs=[];ubs=[]
def raw(x):
    r=np.zeros(N,dtype=np.int64)
    for j in x:r[j]+=1
    return r
def res(x):
    r=raw(x);r[mi]-=ks[x];return r
def add(row,lo=-np.inf,up=np.inf):rows.append(row);lbs.append(lo);ubs.append(up)
for j in range(len(order)-1):add(res(order[j+1])-res(order[j]),1)
rr=res(order[-1]);rr[mi]-=1;add(rr,up=-1)
for x in D:
    rr=res(x);rr[hi]-=1
    if sum(t0[j] for j in x)%m0<h0-1:add(rr,up=-2)
    else:add(rr,lo=0)
    if x:
        rr=raw(x);rr[mi]+=len(x)-4;rr[hi]-=1;add(rr,up=-1)
for j in range(a):
    rr=raw((j,));rr[hi]-=1;add(rr,up=-1)
    rr=2*raw((j,));rr[hi]-=1
    if j<2:add(rr,up=-1)
    else:add(rr,lo=0)
for i in range(2):
    for j in range(2,a):
        rr=raw((i,j));rr[hi]-=1;add(rr,lo=0)
for x in D:
    if len(x)==3:
        rr=raw(x);rr[hi]-=1;add(rr,lo=0)
        if sum(j<2 for j in x)>=2:
            rr=2*raw(x);rr[hi]-=3;add(rr,up=-1)
rr=np.zeros(N,dtype=np.int64);rr[mi]=1;rr[hi]=-1;add(rr,lo=0)
obj=np.zeros(N);obj[mi]=1
mat=np.array(rows,dtype=np.int64)
out=milp(obj,integrality=np.ones(N),bounds=Bounds(np.ones(N),np.full(N,np.inf)),
    constraints=LinearConstraint(mat,np.array(lbs),np.array(ubs)),
    options=dict(time_limit=120,threads=1,mip_rel_gap=0))
assert out.x is not None
xx=np.rint(out.x).astype(np.int64)
assert all((not np.isfinite(lo) or z>=lo) and (not np.isfinite(up) or z<=up)
    for z,lo,up in zip(mat@xx,lbs,ubs))
m,h=map(int,xx[-2:]);t=list(map(int,xx[:a]));weights=[m+z for z in t]
used={sum(t[j] for j in x)%m for x in D};assert len(used)==len(D) and h-1 not in used
for r in range(m):
    if r not in used:
        j=len(weights);weights.append(3*m+h+(r-h)%m);D.append((j,))
Path('compressed_counter.json').write_text(json.dumps(dict(m=m,h=h,weights=weights,D=D))+'\n')
print(json.dumps(dict(scope='one fixed residue-order cone',status=int(out.status),message=out.message,
    old_m=m0,old_h=h0,m=m,h=h,A_offsets=t,nodes=int(out.mip_node_count),gap=float(out.mip_gap))),flush=True)
