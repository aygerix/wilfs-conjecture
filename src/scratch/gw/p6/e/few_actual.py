"""Large-k, several-deep-bad actual tiles qualifying for GENERAL-FEW40.

At a prescribed phase force t distinct pure deep cubics. All other pairs
are selected to minimize Lplus for these units and these forced faces:
one pair of largest ordinary sum for every still available residue.
Execution belongs on fejer.
"""
import json,random,sys
from itertools import combinations_with_replacement as cwr
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'d'))
from core import evaluate
from payments import defect

rng=random.Random(2026101974)
out=[]
for t,k in [(t,k) for t in range(2,6) for k in (40*t+8,72*t+10,80*t)]:
    m=(k+1)**2;rho=m//4
    U=[3*rho//5+i for i in range(t)]
    T={(i,i,i) for i in range(t)}
    forced={(i,i) for i in range(t)}
    blocked={rho,*U,*[(2*u-rho)%m for u in U],*[(3*u-2*rho)%m for u in U]}
    while len(U)<k:
        u=rng.randrange(1,m)
        if u not in blocked:
            U.append(u);blocked.add(u)
    Q=set(forced);buckets={}
    for z in cwr(range(k),2):
        r=(sum(U[i] for i in z)-rho)%m
        if r in blocked:continue
        if r not in buckets or sum(U[i] for i in z)>sum(U[i] for i in buckets[r]):
            buckets[r]=z
    Q.update(buckets.values())
    assert {i for z in Q for i in z}==set(range(k))
    rows=[]
    for delta in [0,1,m//2,m-1]+[rng.randrange(m) for _ in range(8)]:
        V=[(u+delta)%m for u in U];r=(rho+delta)%m
        a=evaluate(m,V,Q,T,r)
        v=defect(m,V,Q,a)
        assert a['HC']>=0
        if delta==0:assert a['beta']==t
        rows.append(dict(delta=delta,rho=r,beta=a['beta'],Lplus=a['Lplus'],HC=a['HC'],S=a['S'],v=v))
    out.append(dict(t=t,k=k,m=m,q=len(Q),s=m-1-k-len(Q)-t,e=a['e'],phases=rows))
print(json.dumps(dict(seed=2026101974,data=out),indent=2),flush=True)
