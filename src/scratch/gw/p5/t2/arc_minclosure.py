"""Minimize proposed arc payment over all eligible pure-A down-sets.
All mathematical execution is restricted to fejer.
"""
from itertools import combinations_with_replacement
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
import random,json,argparse
from collections import deque,Counter

def optimize(t,m,h):
    a=len(t);theta=(3*h+1)//2;cells=[];cost=[]
    for deg in range(1,5):
        for x in combinations_with_replacement(range(a),deg):
            tau=sum(t[j] for j in x)
            if deg*m+tau>4*m+h-1:continue
            rr=tau%m;iny=(h<=rr<min(theta,m)) or (1<=rr<theta-m)
            intr=iny and not(deg==2 and tau>=h)
            cc=(a+3)*(deg==2 and tau<h)+(a+1)*(deg==3 and tau<h)-3*(deg==4)-2*intr
            cells.append(x);cost.append(cc)
    idx={x:i for i,x in enumerate(cells)};N=len(cells);src=N;sink=N+1
    ii=[];jj=[];vv=[];INF=sum(map(abs,cost))+a+100
    def edge(i,j,v):
        if v:ii.append(i);jj.append(j);vv.append(v)
    for i,(x,cc) in enumerate(zip(cells,cost)):
        if len(x)==1:edge(src,i,INF)
        if cc<0:edge(src,i,-cc)
        if cc>0:edge(i,sink,cc)
        if len(x)>1:
            for y in set(x[:j]+x[j+1:] for j in range(len(x))):edge(i,idx[y],INF)
    cap=csr_matrix((np.array(vv,dtype=np.int64),(ii,jj)),shape=(N+2,N+2))
    flow=maximum_flow(cap,src,sink);res=(cap-flow.flow).tocsr()
    seen={src};todo=deque([src])
    while todo:
        i=todo.popleft()
        for j,v in zip(res.indices[res.indptr[i]:res.indptr[i+1]],res.data[res.indptr[i]:res.indptr[i+1]]):
            if v>0 and j not in seen:seen.add(j);todo.append(j)
    D=[x for i,x in enumerate(cells) if i in seen]
    result=a-1+sum(cost[i] for i in seen if i<N)
    assert result==a-1+sum(min(v,0) for v in cost)+flow.flow_value
    out=dict(a=a,m=m,h=h,t=t,slack=int(result),cells=len(D)+1,
             residues=len({sum(t[j] for j in x)%m for x in D}|{0}),D=D)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=3000);p.add_argument('--seed',type=int,default=202610192);p.add_argument('--one-low',action='store_true');p.add_argument('--amin',type=int,default=2);args=p.parse_args()
    rng=random.Random(args.seed);hist=Counter();best=None
    for i in range(args.trials):
        a=rng.randrange(args.amin,20);m=rng.randrange(a+3,1001);h=rng.randrange(2,m+1)
        if args.one_low:
            if h<3:continue
            t=sorted([rng.randrange(1,(h+1)//2)]+[rng.randrange((h+1)//2,h) for _ in range(a-1)])
        else:t=sorted(rng.randrange(1,h) for _ in range(a))
        out=optimize(t,m,h);hist['cases']+=1
        if best is None or out['slack']<best['slack']:best=out
        if out['slack']<0:break
    print(json.dumps(dict(seed=args.seed,counts=hist,best=best)),flush=True)
