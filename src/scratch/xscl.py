# Extremal single-cut lemma (XSCL): E = {y in N^d : V(y) <= th}, B = outer boundary dE.
# If V injective on E u B then  d|E| <= th + |B|.   (Special case of Tile-CL via virtual completion.)
import sys, random, itertools
def simplex(p,th):
    d=len(p); out=[]
    def rec(pref,v):
        if len(pref)==d: out.append(tuple(pref)); return
        k=0
        while v+k*p[len(pref)]<=th:
            rec(pref+[k],v+k*p[len(pref)]); k+=1
    rec([],0); return out
def test(p,th):
    d=len(p); E=simplex(p,th); Es=set(E)
    B=set()
    for y in E:
        for a in range(d):
            z=list(y); z[a]+=1; z=tuple(z)
            if z not in Es: B.add(z)
    V=lambda z: sum(a*b for a,b in zip(z,p))
    vals=[V(z) for z in E]+[V(z) for z in B]
    if len(set(vals))<len(vals): return None
    return d*len(E)-th-len(B)
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
worst={}
for trial in range(4000):
    d=random.choice([2,3,4,5])
    P=random.choice([10,20,40,80])
    p=[random.randint(1,P) for _ in range(d)]
    for th in range(0, 6*P):
        r=test(p,th)
        if r is None: break   # injectivity fails for this th and (monotonically) beyond
        if d not in worst or r>worst[d][0]: worst[d]=(r,p,th)
print(worst)
