"""ONE-DEFICIT count certificate with the forced unit residues 0 and 1.

The input is the weaker necessary-profile list, not actual cores. Each
surviving row is still only a necessary count profile. Run on fejer.
"""
import json
from math import comb

data=json.load(open('one_moment100.json'))['profiles'];cache={};out=[]
for row in data:
    k,v,e,m=row['k'],row['v'],row['e'],row['m'];g=k-v
    for p in (1,2,3):
        good=[]
        for r in range(2,(m-5)//6+1):
            C=(k-1)*r if p==1 else ((2*k+1)*r+k if p==2 else (k+1)*(3*r+3))
            Amax=m-1-C
            if Amax<0:continue
            for inc0 in (False,True):
                for inc1 in (False,True):
                    if int(not inc0)+int(not inc1)>g:continue
                    key=(v,e,r,inc0,inc1)
                    if key not in cache:
                        U=([0] if inc0 else [])+([1] if inc1 else [])
                        j=2
                        while len(U)<v:
                            if j!=r:U.append(j)
                            j+=1
                        allowed=[];degrees=[0]*v
                        for i in range(v):
                            for j in range(i,v):
                                if U[i]==0 and U[j] in (0,1):continue
                                allowed.append((i,j))
                                degrees[i]+=1;degrees[j]+=1
                        if min(degrees)<1 or e>len(allowed):
                            cache[key]=None;continue
                        best=0
                        for cap in U:
                            costs=sorted(min(U[i],cap)+min(U[j],cap) for i,j in allowed)
                            best=max(best,sum(max(x-cap,0) for x in U)+sum(costs[:e]))
                        extra=2*e-v; E=0
                        for i in range(v):
                            take=min(extra,degrees[i]-1)
                            E+=take*U[i];extra-=take
                        if extra:cache[key]=None;continue
                        h=v+int(not inc0)+int(not inc1)
                        qh=comb(h+1,2)-e;c=int(not inc1)
                        mom=(comb(qh,2)+(h+1)*E-(h+1)*c+h-1)//h
                        cache[key]=max(best,mom,sum(U))
                    lb=cache[key]
                    if lb is not None and lb<=Amax:
                        good.append((r,int(inc0),int(inc1),lb))
        if good:
            out.append(dict(row,p=p,rmin=min(x[0] for x in good),rmax=max(x[0] for x in good),
                            anchored_cases=good))
print('anchored profiles',len(out))
for p in (1,2,3):
    rows=[x for x in out if x['p']==p]
    print('p',p,'count',len(rows),'k range',(min(x['k'] for x in rows),max(x['k'] for x in rows)) if rows else None)
print('maximum modulus',max(x['m'] for x in out))
with open('one_anchor100.json','w') as f:json.dump(dict(profiles=out),f,indent=2)
