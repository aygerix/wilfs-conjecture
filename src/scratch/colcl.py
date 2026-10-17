# Column-CL: D any orthogonally convex fundamental domain of Lambda = ker(phi), phi(x)=<x,p> mod m (d=2).
# T(y) = sum_{a: y+e_a not in D} L_a(y) (length of the a-segment through y).  slack(s) in [0,m-1]?
# Enumerate fixed polyominoes of size m (connected), keep orthogonally convex ones.
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
def orthoconvex(P):
    rows={};cols={}
    for x,y in P: rows.setdefault(y,[]).append(x); cols.setdefault(x,[]).append(y)
    return all(max(v)-min(v)+1==len(v) for v in list(rows.values())+list(cols.values()))
def isdown(P):
    return all((x==0 or (x-1,y) in P) and (y==0 or (x,y-1) in P) for x,y in P)
for m in range(3,M+1):
    tot=0; viol=0; ex=None; nondown=0; mn=None; mx=None
    for P in polyominoes(m):
        if not orthoconvex(P): continue
        Pl=sorted(P); dn=isdown(P)
        # segment lengths and tops
        T={}
        for (x,y) in Pl:
            t=0
            if (x+1,y) not in P:
                L=sum(1 for (a,b) in Pl if b==y); t+=L
            if (x,y+1) not in P:
                L=sum(1 for (a,b) in Pl if a==x); t+=L
            T[(x,y)]=t
        for p in itertools.product(range(1,m),repeat=2):
            res={z:(z[0]*p[0]+z[1]*p[1])%m for z in Pl}
            if len(set(res.values()))!=m: continue
            tot+=1; nondown+= (not dn)
            for s in range(m):
                f=sum(T[z]*((s-res[z])%m) for z in Pl)
                sl=Fraction(f-m*(m-1)//2,m)
                mn=sl if mn is None or sl<mn else mn; mx=sl if mx is None or sl>mx else mx
                if sl<0 or sl>m-1:
                    viol+=1
                    if ex is None: ex=(Pl,p,s,sl,dn)
    print(f'm={m}: ortho-convex (D,p) {tot} (non-down-set {nondown}), slack range [{mn},{mx}], violations {viol}',ex if ex else '',flush=True)
