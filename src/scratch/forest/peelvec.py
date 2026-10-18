import sys, itertools
def build(h,F,G,q=None):
    D=set()
    for i in range(len(h)):
        for j in range(h[i]):
            for k in range(min(F[i],G[j])):
                if q and i>=q[0] and j>=q[1] and k>=q[2]: continue
                D.add((i,j,k))
    return D
def add(x,a,d=1):
    y=list(x); y[a]+=d; return tuple(y)
def analyze(D):
    ht={}
    for x in sorted(D,key=lambda x:-sum(x)):
        v=0
        for a in range(3):
            y=add(x,a)
            if y in D: v=max(v,ht[y]+1)
        ht[x]=v
    def top(x,a):
        while add(x,a) in D: x=add(x,a)
        return x
    wt={}; kind={}
    for x in D:
        T=[top(x,a) for a in range(3)]; H=[ht[t] for t in T]
        nn=sum(1 for v in H if v==0); hh=sum(H)
        if ht[x]==0: wt[x]=2; kind[x]='M'
        elif nn==3: wt[x]=2; kind[x]='T'
        elif nn==2 and hh==1:
            c=[a for a in range(3) if H[a]][0]
            wt[x]=1; kind[x]='U' if add(x,c) not in D else 'O'
        else: wt[x]=0
    return wt,kind
def corners(D):
    C=0
    for x in D:
        for b in range(3):
            if x[b]!=0: continue
            if all(add(x,a) not in D for a in range(3) if a!=b): C+=1
    return C
def peel(D,s):
    return {tuple(x[a]-s[a] for a in range(3)) for x in D if all(x[a]>=s[a] for a in range(3))}
def report(D,smax=3,show=True):
    wt,kind=analyze(D); C=corners(D); W=sum(wt.values())
    res=[]
    for s in itertools.product(range(smax+1),repeat=3):
        if sum(s)==0 or sum(s)>smax or s not in D: continue
        Ds=peel(D,s); out=sum(wt[x] for x in D if not all(x[a]>=s[a] for a in range(3)))
        res.append((out-4*(C-corners(Ds)),s,out,C-corners(Ds)))
    res.sort()
    if show:
        print("m",len(D),"W",W,"C",C,"W-4C",W-4*C)
        for r in res[:12]: print("  PI %3d s=%s out=%d dC=%d"%r)
    return res
if __name__=="__main__":
    h,F,G=[eval(a) for a in sys.argv[1:4]]
    q=eval(sys.argv[4]) if len(sys.argv)>4 else None
    report(build(h,F,G,q))
