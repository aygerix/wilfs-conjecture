import sys, itertools, collections
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); m=int(sys.argv[2])
def top(D,x,a):
    y=list(x)
    while True:
        y[a]+=1
        if tuple(y) not in D: y[a]-=1; return tuple(y)
hist=collections.Counter(); ex={}
for D in downsets(m,d):
    Dl=sorted(D); S=set(Dl)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    for p in itertools.product(range(1,m),repeat=d):
        ph={x:sum(a*b for a,b in zip(x,p))%m for x in Dl}
        if len(set(ph.values()))!=m: continue
        L=[(ph[top(S,x,a)]-ph[x])%m for x in Dl for a in range(d) if top(S,x,a)!=x]
        c0=sum(L)//m-(m-1)//2 if (m%2==1) else None
        c0x=(2*sum(L)-m*(m-1))/(2*m)
        npairs=len(L)
        key=(npairs-(m-1), c0x)
        hist[key]+=1
        ex.setdefault(key,(Dl,p,sorted(L)))
for k in sorted(hist): print('extra pairs',k[0],'c0',k[1],'count',hist[k],'ex',[''.join(map(str,x)) for x in ex[k][0]],ex[k][1],ex[k][2])
