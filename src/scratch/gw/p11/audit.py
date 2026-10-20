"""Independent Dijkstra verification of P11 failed candidates. Fejer only."""
import heapq,json,re
from collections import defaultdict

def apery(m,gens):
    w=[10**30]*m;w[0]=0;pq=[(0,0)]
    while pq:
        v,r=heapq.heappop(pq)
        if v!=w[r]:continue
        for g in gens:
            rr=(r+g)%m;vv=v+g
            if vv<w[rr]:w[rr]=vv;heapq.heappush(pq,(vv,rr))
    assert max(w)<10**30
    return w

def ev(gens):
    m=gens[0];gg=gens[1:];w=apery(m,gg);ap=set(w);M=max(w);c=M-m+1
    C2=m*(m-1)//2;lam={x:(M-x)//m for x in w};ell=sum(lam.values())
    con={x:0 for x in w};bydir={};bylayer=[0]*5
    for g in gg:
        cv={};R=0;B=0
        for x in w:
            y=x
            while y+g in ap:y+=g
            cv[x]=y-x-m*lam[x];con[x]+=cv[x]
            R+=(M-x)%g;B+=M-y
        bydir[g]={'RC':R,'CHAIN':B,'origin':cv[0],'bulk':sum(cv.values())-cv[0]}
    for x in w:bylayer[lam[x]]+=con[x]
    return dict(m=m,gens=gens,apery=w,M=M,c=c,e=len(gens),genus=sum(x//m for x in w),ell=ell,
                W=len(gens)*ell-c,C2=C2,con=con,layers=bylayer,bydir=bydir)

records=defaultdict(list)
for line in open('scan.log'):
    if not line.startswith('FAIL '):continue
    fields=dict(re.findall(r'(\w+)=([^ ]+)',line.strip()))
    records[int(fields['cls']),int(fields['cand'])].append(fields)
out=[]
for key,rr in sorted(records.items()):
    f=min(rr,key=lambda z:int(z['genus']))
    gens=list(map(int,f['gens'].split(',')));v=ev(gens)
    assert v['genus']==int(f['genus'])
    v['class'],v['candidate']=key
    out.append(v)

# A direction-by-direction bulk bound is false even for sparse q=4.
fam=[]
for k in range(2,51):
    m=4*k+1;v=ev([m]+list(range(m+1,m+k+1)))
    assert v['c']==4*m and v['ell']==4+6*k
    assert v['bydir'][m+k]['bulk']==6*k*k
    fam.append({k:v[k] for k in ('m','c','e','ell','W') } | {'k':k,'positive_direction_bulk':6*k*k})

# The co-Kunz RC equality requires the wrap multiplicity, not just an indicator.
correction=[]
for gens in ([4,9,10],[5,9,12]):
    v=ev(gens);m=v['m'];M=v['M'];w=v['apery'];lam=[(M-x)//m for x in w];ss=[(M-x)%m for x in w]
    for g in gens[1:]:
        b=g-m
        wraps=sum(-((s-l*b)//g) for s,l in zip(ss,lam))
        indicators=sum(s<l*b for s,l in zip(ss,lam))
        term=v['bydir'][g]['RC']-v['C2']
        assert term==g*wraps-b*v['ell']
        correction.append(dict(gens=gens,n=g,ell=v['ell'],actual=term,
                               indicator=g*indicators-b*v['ell'],wrap_count=wraps,indicator_count=indicators))
json.dump({'smallest_genus_witnesses':out,'per_direction_bulk_family':fam,'coKunz_audit':correction},
          open('audit.json','w'),indent=2)
for v in out:
    print({k:v[k] for k in ('class','candidate','genus','gens','c','C2','layers')})
print('CO_KUNZ',correction)
print('PER_DIRECTION_FAMILY',fam[0],fam[1],fam[-1])
