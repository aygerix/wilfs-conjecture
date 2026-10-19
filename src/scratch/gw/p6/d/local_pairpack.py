"""Localized missing-pair fiber packing, exact necessary-profile check."""
import json
from math import comb

def packing(k,v,e,m):
    cap=(v+1)//2 if m%2 else v//2+1
    f,r=divmod(e,cap)
    loss=4*(f*comb(cap+1,2)+comb(r+1,2))
    return k*(k+1)+1-loss

for filename in ('one_moment100.json','one_reserve100.json','one_anchor100.json'):
    rows=json.load(open(filename))['profiles']
    out=[x for x in rows if x['m']>=packing(x['k'],x['v'],x['e'],x['m'])]
    print(filename,'before',len(rows),'after',len(out))
    for p in sorted({x.get('p',0) for x in out}):
        sub=[x for x in out if x.get('p',0)==p]
        print('p',p,'n',len(sub),'k',(min(x['k'] for x in sub),max(x['k'] for x in sub)))
    if filename=='one_anchor100.json':
        with open('one_packed100.json','w') as f:json.dump(dict(profiles=out),f,indent=2)
