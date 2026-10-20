"""Memory-light independent REST check, exact Apéry and two N_a counts.

Fejer only. For every direction, enumerate literal chain tops. Independently
count all endpoint pairs from residue-class sizes modulo that generator.
"""
import collections,json,sys
from check import apery

def sparse_check(g):
    g=sorted(set(g));m=g[0];d=len(g)-1;w=apery(g);ap=set(w);M=max(w)
    assert all(n<2*m for n in g[1:]),'This driver certifies minimality by n<2m.'
    ellp=sum((M-x)//m for x in w if x);N=[];con=[0]*m;con0=0
    for n in g[1:]:
        chain_count=0
        for i,x in enumerate(w):
            t=x;k=0
            while t+n in ap:t+=n;k+=1
            con[i]+=(M-x)%m-(M-t)
            if x:chain_count+=k
        cc=collections.Counter(x%n for x in w)
        pairs=sum(z*(z-1)//2 for z in cc.values())-(cc[0]-1)
        assert pairs==chain_count,(n,pairs,chain_count)
        N.append(pairs)
    rest=sum(con[1:]);rest2=sum(n*z for n,z in zip(g[1:],N))-m*d*ellp
    assert rest==rest2
    return dict(generators=g,apery_by_residue=w,m=m,e=d+1,M=M,n1=g[1],c=M-m+1,
                ellp=ellp,N=N,con_by_residue=con,REST=rest,REST_count=rest2,
                con0=con[0],Delta=sum(con),C2=m*(m-1)//2,
                W=(d+1)*(ellp+M//m)-(M-m+1))

if __name__=='__main__':
    print(json.dumps(sparse_check(list(map(int,sys.argv[1:]))),indent=2))
