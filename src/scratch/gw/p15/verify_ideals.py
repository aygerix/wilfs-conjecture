"""Independent direct all-p checks of recorded ideal witnesses. Fejer only."""
import itertools,json,re
from pathlib import Path
cases=[]
def test(tag,m,r,D,reported=None):
 DD=set(map(tuple,D));assert len(DD)==len(D)
 assert all(tuple(f[b]-(a==b) for b in range(len(r))) in DD for f in DD for a in range(len(r)) if f[a])
 RR={f:sum(x*y for x,y in zip(f,r)) for f in DD}
 assert len({v%m for v in RR.values()})==len(DD)
 rows=[]
 for p in range(1,m+1):
  C=lambda y:sum(1 for z in range(p,y+1,m))
  K={f:C(RR[f])-sum(f[a]*(C(RR[f])-C(RR[f]-r[a])) for a in range(len(r)) if f[a]) for f in DD}
  ex=sum(K.values())-sum(sum(f)>=2 for f in DD)
  rows.append(dict(p=p,sumK=sum(K.values()),excess=ex,K=[K[f] for f in sorted(DD)]))
 if reported is not None:assert max(z['excess'] for z in rows)==reported
 cases.append(dict(tag=tag,m=m,r=r,D=sorted(DD),phases=rows))

D=[(i,j) for i in range(4) for j in range(4-i)]
for d in range(2,6):
 rr=[9,10]+[8,11,12][:d-2]
 DD=[f+(0,)*(d-2) for f in D]+[tuple(int(i==a) for i in range(d)) for a in range(2,d)]
 test('m13_dim'+str(d),13,rr,DD,1)
rr=[8,9,1,5,6,7]
DD=[f+(0,)*4 for f in D]+[tuple(int(i==a) for i in range(6)) for a in range(2,6)]
test('m14_dim6',14,rr,DD,1)
yy=[0,1,4,13,32,71];m=1712;rr=[m//2+1+4*y for y in yy]
DD=[(0,)*6]
for j in range(1,4):
 for inds in itertools.combinations(range(6),j):DD.append(tuple(int(a in inds) for a in range(6)))
test('squarefree_six',m,rr,DD,5)
for H in [3,5,10]:
 L=H*H+H+10;m=(H-1)*L+3;r=m-L
 DD=[(i,j) for i in range(H+1) for j in range(H+1-i)]
 test('dilute_height_'+str(H),m,[r,r+1],DD,(H-1)*(H-2)//2)
for ln in Path('ideal_search.log').read_text().splitlines():
 if not ln.startswith(('SMALLEST','LARGEST')):continue
 m=int(re.search(r' m=(\d+)',ln).group(1));ex=int(re.search(r' excess=(-?\d+)',ln).group(1))
 match=re.search(r' r=(\[.*?\]) D=(\[.*\])',ln)
 test('anneal_'+str(len(cases)),m,json.loads(match.group(1)),json.loads(match.group(2)),ex)
Path('verified_ideals.json').write_text(json.dumps(cases,indent=2))
print('SUMMARY verified_ideals='+str(len(cases))+' phases='+str(sum(len(c['phases']) for c in cases)))
