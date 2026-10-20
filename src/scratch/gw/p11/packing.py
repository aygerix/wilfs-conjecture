"""Independent ordinary support verification of the packing input. Fejer only."""
from collections import Counter
from itertools import combinations,combinations_with_replacement
from math import comb
from fractions import Fraction as F
import random,json

def check(X,name):
    X=sorted(X);n=len(X)
    pairs=Counter(x+y for x,y in combinations_with_replacement(X,2))
    assert max(pairs.values())==1
    sf=Counter(sum(z) for z in combinations(X,3))
    repeat=Counter(2*x+y for x in X for y in X)
    trip=sf+repeat
    ex=comb(n+2,3)-len(trip)
    heavy=sum(v>=11 for v in sf.values())
    normal=set(X)
    for i,x in enumerate(X):
        for j in range(i,n):
            for k,z in enumerate(X):
                if k!=i and k!=j:normal.add(x+X[j]-z)
    H=n*(comb(n,2)+1)
    bound=F(H)-45*ex-F(126+heavy,2)*n*n+3*n
    assert len(normal)>=bound
    assert len(normal)<=3*(max(X)-min(X)+1)-2
    assert sum(comb(v,2) for v in repeat.values())<=comb(n,2)
    return dict(name=name,n=n,s=max(X)-min(X)+1,ex=ex,heavy=heavy,
                sfmax=max(sf.values(),default=0),signed=len(normal),SM_slack=str(len(normal)-bound))

fixtures=json.load(open('planted_input.json'))
out=[check(v['B'],v['name']) for v in fixtures]
out.append(check([0,1,6,15,19,31,58,65,75],'n9_extremizer'))
rng=random.Random(92)
for n in (3,5,10,15,20,30,40,50,64,80):
    X=[];pairs=set()
    while len(X)<n:
        x=rng.randrange(4*n**3)
        if x in X:continue
        new=[x+y for y in X]+[2*x]
        if len(set(new))<len(new) or set(new)&pairs:continue
        pairs.update(new);X.append(x)
    out.append(check(X,'random_'+str(n)))
json.dump(out,open('packing.json','w'),indent=2)
print(json.dumps({'status':'PASS','cases':out},sort_keys=True))
