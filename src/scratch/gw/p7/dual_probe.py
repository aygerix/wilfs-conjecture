"""Save floating LP duals as discovery data, not proof certificates."""
import json
from optimize import pool,system,solve,costs

cases=[(17,(7,9,12,13,15),7),(11,(3,6,9,10),9),
       (40,(3,7,11,15,19),18),(40,(7,10,13,17,23,29),20)]
for m,P,theta in cases:
    cells=pool(m,P,20000)
    ss=system(m,P,cells,True,True)
    res,const=solve(m,P,cells,ss,theta,True,False,10)
    c,_=costs(m,P,cells,ss['v'],theta,True)
    edges=[]
    for x in cells:
        for a in range(len(P)):
            if x[a]:
                y=list(x);y[a]-=1
                edges.append((x,tuple(y)))
    print(json.dumps(dict(m=m,P=P,theta=theta,value=float(res.fun+const),
         selected=[(x,float(z),int(cc)) for x,z,cc in zip(cells,res.x,c) if z>1e-7],
         labels=[(j,float(z)) for j,z in enumerate(res.ineqlin.marginals[:m]) if abs(z)>1e-7],
         edges=[(a,b,float(z)) for (a,b),z in zip(edges,res.ineqlin.marginals[m:]) if abs(z)>1e-7],
         lower=[(x,float(z)) for x,z in zip(cells,res.lower.marginals) if abs(z)>1e-7],
         upper=[(x,float(z)) for x,z in zip(cells,res.upper.marginals) if abs(z)>1e-7])))
