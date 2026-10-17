# Print the mixed-orientation (rotated L-shape) violations at m=9, and the slack vectors.
import itertools
from fractions import Fraction
m=9
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
for P in polyominoes(m):
    o=orient(P)
    if o not in ([(1,-1)],[(-1,1)]): continue
    Pl=sorted(P)
    T={}
    for (x,y) in Pl:
        t=0
        if (x+1,y) not in P: t+=sum(1 for (a,b) in Pl if b==y)
        if (x,y+1) not in P: t+=sum(1 for (a,b) in Pl if a==x)
        T[(x,y)]=t
    for p in itertools.product(range(1,m),repeat=2):
        res={z:(z[0]*p[0]+z[1]*p[1])%m for z in Pl}
        if len(set(res.values()))!=m: continue
        sl=[Fraction(sum(T[z]*((s-res[z])%m) for z in Pl)-m*(m-1)//2,m) for s in range(m)]
        if min(sl)<0 or max(sl)>m-1:
            rows={}
            for x,y in Pl: rows.setdefault(y,[]).append(x)
            pic='\n'.join(''.join('#' if (x,y) in P else '.' for x in range(max(a for a,b in Pl)+1)) for y in range(max(b for a,b in Pl),-1,-1))
            print('orient',o,'p',p,'slack',[str(v) for v in sl]); print(pic); print()
