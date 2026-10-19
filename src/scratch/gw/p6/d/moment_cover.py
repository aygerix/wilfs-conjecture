"""Finite profile refinements for ONE-RELAY; execute on fejer."""
import json
from math import comb

data=json.load(open('one_moment100.json'))
out=[]; cache={}
for row in data['profiles']:
    v,e=row['v'],row['e']
    if (v,e) not in cache:
        best=0;arg=None
        for cap in range(v):
            vals=sorted(min(i,cap)+min(j,cap) for i in range(v) for j in range(i,v))
            val=comb(v-cap,2)+sum(vals[:e])
            if val>best:best,arg=val,cap
        cache[v,e]=(best,arg)
    M,cap=cache[v,e]
    if M>row['Amax']:continue
    # A covers every defective vertex; degree at a vertex <=v+1.
    # Combine the rank constraints on W_D and on all present pair sums.
    # Stronger threshold-sum constraints will be listed separately.
    row.update(Mcover=M,cap=cap)
    out.append(row)
print('after covered-degree bound',len(out),'max k',max(x['k'] for x in out))
for k in sorted({x['k'] for x in out}):
    rows=[x for x in out if x['k']==k]
    print(k,len(rows),'v',min(x['v'] for x in rows),max(x['v'] for x in rows))
with open('one_cover100.json','w') as f:json.dump(dict(profiles=out),f,indent=2)
