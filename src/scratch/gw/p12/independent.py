"""Independent forward-membership sieve: no Dijkstra and no chain recursion.

Exact small counterexamples; research computations run on fejer only.
"""
import json
from check import check

def sieve(g):
    m=min(g);cap=m*max(g)+m;member=bytearray(cap+1);member[0]=1
    w=[None]*m;left=m
    for x in range(cap+1):
        if not member[x]:continue
        if w[x%m] is None:w[x%m]=x;left-=1
        for n in g:
            if x+n<=cap:member[x+n]=1
        if not left:break
    assert not left
    M=max(w);c=M-m+1;ell=sum(member[:c]);ap=set(w);d=len(g)-1
    N={n:0 for n in g[1:]};con={x:0 for x in w};ellp=0
    for x in w:
        if x:ellp+=sum(1 for z in range(x,c,m) if member[z])
        for n in g[1:]:
            steps=0
            for y in range(x+n,M+1,n):
                if y not in ap:break
                steps+=1
            if x:N[n]+=steps
            con[x]+=(M-x)%m-(M-x-steps*n)
    rest=sum(z for x,z in con.items() if x)
    return dict(generators=g,apery_by_residue=w,M=M,c=c,n1=g[1],ell=ell,ellp=ellp,N=N,
                con=con,REST=rest,con0=con[0],Delta=sum(con.values()),C2=m*(m-1)//2,W=len(g)*ell-c)

if __name__=='__main__':
    cases=[[4,5],[32]+list(range(39,46)),[87]+list(range(105,123)),[102]+list(range(123,144))]
    out=[]
    for g in cases:
        s=sieve(g);q=check(g)
        for key in ('apery_by_residue','M','c','n1','ellp','N','con','REST','con0','Delta','C2'):
            assert s[key]==q[key],(key,s[key],q[key])
        print({k:s[k] for k in ('generators','M','ell','ellp','N','REST','con0','Delta','C2','W')},flush=True)
        out.append(s)
    with open('independent_sieve.json','w') as fp:json.dump(out,fp,indent=2)
