"""Heuristic search over arbitrary height-3 tiles, not just Apéry normal forms.
fejer only, nice, HiGHS threads=1. Every incumbent is checked with exact ints.
Solver statuses/bounds are search data, never a universal certificate.
"""
import os
for option in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[option]='1'
import json,math,random,sys,warnings
from itertools import combinations_with_replacement
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import coo_matrix
warnings.filterwarnings('ignore',message='Unrecognized options detected')

def cells(d,h):return list(combinations_with_replacement(range(d),h))
def residue(T,p,m):return sum(p[a] for a in T)%m
def solve(p,m,sigma,limit):
    d=len(p);unitres={0,*p};P=[T for T in cells(d,2) if residue(T,p,m) not in unitres]
    pi={T:i for i,T in enumerate(P)}
    T=[];req=[]
    for y in cells(d,3):
        divisors=set(tuple(y[:j]+y[j+1:]) for j in range(3))
        if any(z not in pi for z in divisors) or residue(y,p,m) in unitres:continue
        inds=[pi[z] for z in divisors]
        if len({residue(P[j],p,m) for j in inds})!=len(inds):continue
        T.append(y);req.append(inds)
    q=len(P);t=len(T);nv=2*q+t+d
    pairmax=q+t;unitmax=2*q+t
    rows=[];lower=[];upper=[]
    def row(dd,lo=-np.inf,hi=np.inf):rows.append(dd);lower.append(lo);upper.append(hi)
    for r in range(m):
        if r in unitres:continue
        dd={j:1 for j,z in enumerate(P) if residue(z,p,m)==r}
        dd.update({q+j:1 for j,y in enumerate(T) if residue(y,p,m)==r})
        row(dd,1,1)
    for j,inds in enumerate(req):
        for i in inds:row({q+j:1,i:-1},hi=0)
    for i,z in enumerate(P):
        row({pairmax+i:1,i:-1},hi=0)
        for j,inds in enumerate(req):
            if i in inds:row({pairmax+i:1,q+j:1},hi=1)
        for a in set(z):row({unitmax+a:1,i:1},hi=1)
    ri=[];ci=[];data=[]
    for a,dd in enumerate(rows):
        for b,v in dd.items():ri.append(a);ci.append(b);data.append(v)
    M=coo_matrix((data,(ri,ci)),shape=(len(rows),nv)).tocsc()
    obj=np.zeros(nv)
    for j,y in enumerate(T):obj[q+j]=-(d+3)*((residue(y,p,m)-sigma)%m)
    for i,z in enumerate(P):obj[pairmax+i]=-(d+2)*((residue(z,p,m)-sigma)%m)
    for a in range(d):obj[unitmax+a]=-(d+1)*((p[a]-sigma)%m)
    ans=milp(obj,integrality=np.ones(nv),bounds=Bounds(np.zeros(nv),np.ones(nv)),
             constraints=LinearConstraint(M,np.array(lower),np.array(upper)),
             options=dict(time_limit=limit,mip_rel_gap=0.0,threads=1))
    if ans.x is None:return dict(status=int(ans.status),incumbent=False)
    take=np.rint(ans.x).astype(int)
    assert np.max(np.abs(ans.x-take))<1e-5
    D=[(),*[(a,) for a in range(d)]]
    D += [z for i,z in enumerate(P) if take[i]]
    D += [y for j,y in enumerate(T) if take[q+j]]
    assert len(D)==m and len({residue(x,p,m) for x in D})==m
    DD=set(D)
    assert all(tuple(x[:a]+x[a+1:]) in DD for x in D for a in range(len(x)))
    A=[x for x in D if not any(tuple(sorted(x+(a,))) in DD for a in range(d))]
    values=[]
    for sig in range(m):
        val=(d+1)*m*(m-1)//2-sum((d+len(x))*((residue(x,p,m)-sig)%m) for x in A)
        values.append(val)
    out=dict(status=int(ans.status),incumbent=True,min_slack=min(values),sigma=values.index(min(values)),
             objective_sigma=sigma,slack_objective=values[sigma],gap=float(getattr(ans,'mip_gap',math.inf)),
             m=m,p=p,D=D)
    if min(values)<0:
        Path('MAXCL_COUNTEREXAMPLE.json').write_text(json.dumps(out,indent=2)+'\n')
        print('MAXCL_COUNTEREXAMPLE',json.dumps(out),flush=True);raise SystemExit(2)
    return out

seed=int(sys.argv[1]);samples=int(sys.argv[2]);limit=float(sys.argv[3])
rng=random.Random(seed);profiles=[]
for r in (2,3,4):
    m=(r+1)**3;p=sorted(a*(r+1)**j for j in range(3) for a in range(1,r+1))
    profiles.append((m,p))
while len(profiles)<samples:
    d=rng.randint(6,12);m=rng.randint(3*(d+1)+1,min(8*d+3,math.comb(d+3,3)))
    p=sorted(rng.sample(range(1,m),d))
    cov={0,*p}
    for h in (2,3):cov|={residue(y,p,m) for y in cells(d,h)}
    if len(cov)==m:profiles.append((m,p))
results=[]
print('VERSIONS',sys.version.split()[0],np.__version__,scipy.__version__,'threads=1',flush=True)
for i,(m,p) in enumerate(profiles):
    # Multiplication is a new numerical test, not a normalization of MaxCL.
    if i>=3 and i%2:
        us=[a for a in range(1,m) if math.gcd(a,m)==1];u=rng.choice(us);p=sorted((u*a)%m for a in p)
    for sigma in sorted({0,1,rng.randrange(m)}):
        out=solve(p,m,sigma,limit);out.update(index=i,seed=seed)
        print('CASE',json.dumps({k:v for k,v in out.items() if k!='D'},sort_keys=True),flush=True)
        results.append(out)
Path('milp_'+str(seed)+'.json').write_text(json.dumps(results,indent=2)+'\n')
valid=[z for z in results if z['incumbent']]
print('MILP_SEARCH_FINISHED',json.dumps(dict(calls=len(results),incumbents=len(valid),worst=min((z['min_slack'] for z in valid),default=None)),sort_keys=True))
