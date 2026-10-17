# Column-CL by orientation class: D is a "down-set w.r.t. orthant eps" if it is closed under x -> x - eps_a e_a
# (staying in the bounding box corner).  Test violations per orientation (d=2).
import sys, itertools
from fractions import Fraction
M=int(sys.argv[1])
def polyominoes(n):
    cur={frozenset([(0,0)])}
    for _ in range(n-1):
        nxt=set()
        for P in cur:
            for (x,y) in P:
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    c=(x+dx,y+dy)
                    if c in P: continue
                    Q=P|{c}; mx=min(a for a,b in Q); my=min(b for a,b in Q)
                    nxt.add(frozenset((a-mx,b-my) for a,b in Q))
        cur=nxt
    return cur
def orient(P):
    xs=[a for a,b in P]; ys=[b for a,b in P]; X0,X1,Y0,Y1=min(xs),max(xs),min(ys),max(ys)
    out=[]
    for ex,ey in itertools.product((1,-1),repeat=2):
        ok=True
        for x,y in P:
            px=x-ex; py=y-ey
            if X0<=px<=X1 and (px,y) not in P: ok=False;break
            if Y0<=py<=Y1 and (x,py) not in P: ok=False;break
        if ok: out.append((ex,ey))
    return out
def orthoconvex(P):
    rows={};cols={}
    for x,y in P: rows.setdefault(y,[]).append(x); cols.setdefault(x,[]).append(y)
    return all(max(v)-min(v)+1==len(v) for v in list(rows.values())+list(cols.values()))
for m in range(3,M+1):
    stats={}
    for P in polyominoes(m):
        if not orthoconvex(P): continue
        Pl=sorted(P); ors=tuple(orient(P)); key=ors if ors else 'none'
        T={}
        for (x,y) in Pl:
            t=0
            if (x+1,y) not in P: t+=sum(1 for (a,b) in Pl if b==y)
            if (x,y+1) not in P: t+=sum(1 for (a,b) in Pl if a==x)
            T[(x,y)]=t
        for p in itertools.product(range(1,m),repeat=2):
            res={z:(z[0]*p[0]+z[1]*p[1])%m for z in Pl}
            if len(set(res.values()))!=m: continue
            st=stats.setdefault(key,[0,0])
            st[0]+=1
            for s in range(m):
                f=sum(T[z]*((s-res[z])%m) for z in Pl)
                sl=Fraction(f-m*(m-1)//2,m)
                if sl<0 or sl>m-1: st[1]+=1; break
    print('m',m,{k:v for k,v in sorted(stats.items(),key=str)},flush=True)
