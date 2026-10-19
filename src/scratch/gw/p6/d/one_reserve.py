"""Reserve the least nonmaximal-pair residue in the one-cubic profiles."""
import json
from math import comb

data=json.load(open('one_moment100.json'))['profiles']
out=[];cache={};counts={p:0 for p in (1,2,3)}
for row in data:
    k,m,v,e=row['k'],row['m'],row['v'],row['e']
    assert row['s']==0
    for p in (1,2,3):
        surviving=[]
        for r in range(2,(m-5)//6+1):
            # Lower cost for the distinct N2 residues, each >=r.
            coeffcost= (k-1)*r if p==1 else ((2*k+1)*r+k if p==2 else (k+1)*(3*r+3))
            Amax=m-1-coeffcost
            if Amax<0:continue
            key=(v,e,r)
            if key not in cache:
                U=[i+int(i>=r) for i in range(v)]
                best=sum(sorted(U[i]+U[j] for i in range(v) for j in range(i,v))[:e])
                # Cover correction, valid because every defective vertex has degree >=1.
                for cap in U:
                    cv=sorted(min(x,cap)+min(y,cap) for i,x in enumerate(U) for y in U[i:])
                    best=max(best,sum(max(x-cap,0) for x in U)+sum(cv[:e]))
                extra=2*e-v
                # Each delta_i-1 is between 0 and v, with total 2e-v.
                f,rem=divmod(extra,v)
                E=v*sum(U[:f])+(U[f]*rem if rem else 0)
                cache[key]=(max(sum(U),best),E)
            lower,E=cache[key]
            if lower>Amax:continue
            if comb(row['qv'],2)+(v+1)*E>v*Amax:continue
            surviving.append(r)
        if surviving:
            ans=dict(row,p=p,rmin=min(surviving),rmax=max(surviving))
            out.append(ans);counts[p]+=1
print('reserved profiles',len(out),'by p',counts,'maximum k',max(x['k'] for x in out))
for p in (1,2,3):
    rows=[x for x in out if x['p']==p]
    print('p',p,'count',len(rows),'k range',(min(x['k'] for x in rows),max(x['k'] for x in rows)) if rows else None)
with open('one_reserve100.json','w') as f:json.dump(dict(profiles=out,counts=counts),f,indent=2)
