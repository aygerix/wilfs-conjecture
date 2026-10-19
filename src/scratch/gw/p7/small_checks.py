"""Exact checks of the two small failed induction claims in P7_REPORT."""
import json
from core import evaluate


partial=[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]
z=evaluate(7,(4,5),partial)
assert z['rows'][3]['shadow']==-1
full=[x+(0,) for x in partial]+[(0,0,1)]
zz=evaluate(7,(4,5,6),full)
assert zz['rows'][3]['shadow']==0

old=evaluate(4,(1,),[(j,) for j in range(4)])
new=evaluate(4,(1,2),[(0,0),(1,0),(0,1),(1,1)])
o=old['rows'][0];n=new['rows'][0]
assert o['rho']==n['rho']==3
assert o['S']==4 and o['Lam']==0 and o['shadow']==1
assert n['S']==10 and n['Lam']==2 and n['shadow']==2
print(json.dumps(dict(injective_partial=z['rows'][3],spike_completion=zz['rows'][3],
                      compression_old=o,compression_new=n,verified=True),sort_keys=True))
