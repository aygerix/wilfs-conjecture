"""Minimum-weight order ideal for a fixed positive rational weight and maximum.
All execution belongs on fejer.  Network min-cut is exact integer arithmetic.
This tests distinct-weight P4 for M >= 6q-3 (default), independently of
the fixed-cardinality enumerator.  Denominator q represents normalized m.
"""
import argparse, itertools, random, json
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow

def cells(n, cap):
    d=len(n)
    def rec(a, rem, x):
        if a==d:
            yield tuple(x)
        else:
            for z in range(rem//n[a]+1):
                yield from rec(a+1, rem-z*n[a], x+[z])
    return list(rec(0,cap,[]))

def test(n,q,y):
    M=sum(a*b for a,b in zip(n,y)); d=len(n)
    X=cells(n,M); idx={x:i for i,x in enumerate(X)}
    V=[sum(a*b for a,b in zip(n,x)) for x in X]
    c=[d*min(4,(M-v)//q)-min(4,v//q) for v in V]
    N=len(X); source=N; sink=N+1; big=1+sum(abs(t) for t in c)
    ii=[]; jj=[]; vv=[]
    def edge(i,j,w):
        if w: ii.append(i); jj.append(j); vv.append(w)
    for i,x in enumerate(X):
        if c[i]<0: edge(source,i,-c[i])
        elif c[i]>0: edge(i,sink,c[i])
        for a in range(d):
            if x[a]:
                z=list(x); z[a]-=1; edge(i,idx[tuple(z)],big)
    edge(source,idx[y],big)
    G=csr_matrix((np.array(vv,dtype=np.int64),(ii,jj)),shape=(N+2,N+2))
    F=maximum_flow(G,source,sink)
    val=int(F.flow_value)+sum(t for t in c if t<0)
    if val<0:
        R=(G-F.flow).tocsr(); seen={source}; stack=[source]
        while stack:
            a=stack.pop()
            for z in range(R.indptr[a],R.indptr[a+1]):
                b=int(R.indices[z])
                if R.data[z]>0 and b not in seen: seen.add(b); stack.append(b)
        D=[X[i] for i in range(N) if i in seen]
        print(json.dumps(dict(n=n,q=q,M=M,slack=val,D=D,m=len(D))),flush=True)
        return False
    return True

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=10000);p.add_argument('--seed',type=int,default=20261019);p.add_argument('--dmax',type=int,default=6);p.add_argument('--cap',type=int,default=8);p.add_argument('--weightmax',type=int,default=4);p.add_argument('--tops',type=int,default=8);p.add_argument('--q',type=int,default=31);p.add_argument('--offset',type=int,default=3);a=p.parse_args()
    rng=random.Random(a.seed);tests=0
    for trial in range(a.trials):
        d=rng.randrange(2,a.dmax+1);q=a.q;n=tuple(sorted(rng.sample(range(q+1,a.weightmax*q+1),d)))
        Y=cells(n,a.cap*q);Y=[y for y in Y if 6*q-a.offset<=sum(t*z for t,z in zip(n,y))]
        rng.shuffle(Y)
        for y in Y[:a.tops]:
            tests+=1
            if not test(n,q,y): raise SystemExit(2)
        if trial%100==0: print('progress',trial,tests,flush=True)
    print('PASS',a.trials,tests,flush=True)
