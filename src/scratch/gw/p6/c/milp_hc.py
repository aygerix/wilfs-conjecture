"""Adversarial fixed-unit/fixed-dimension core search. fejer only, one core.

For fixed P,m,d,sigma, scipy.milp optimizes the SHAPE exactly when it
reaches optimal status. All returned shapes are checked with integers.
This is a search, not a finite certificate for all labelings.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
from itertools import combinations_with_replacement as cwr
from pathlib import Path
from collections import Counter
import json, random, warnings, sys
warnings.filterwarnings('ignore',message='Unrecognized options detected')

rng=random.Random(2026101933); stats=Counter(); best=None; witnesses=[]
def solve(P,m,d,sigma):
    global best
    k=len(P); blocked={0,*P}; L=m-d-1
    Q=[z for z in cwr(range(k),2) if sum(P[i] for i in z)%m not in blocked]
    qi={z:i for i,z in enumerate(Q)}; nq=len(Q)
    T=[y for y in cwr(range(k),3) if sum(P[i] for i in y)%m not in blocked
       and all(y[:j]+y[j+1:] in qi for j in range(3))]
    nt=len(T); nv=2*nq+nt
    if not nt or L<2 or L>nq+nt:return
    rows=[];cols=[];data=[];lo=[];hi=[]
    def con(items,l=-np.inf,h=np.inf):
        row=len(lo);lo.append(l);hi.append(h)
        for j,v in items:rows.append(row);cols.append(j);data.append(v)
    # q_i, n_i (non-maximal pair), t_y. Downward closure and exact OR.
    incidence=[[] for _ in Q]
    buckets={}
    for i,z in enumerate(Q):
        buckets.setdefault(sum(P[j] for j in z)%m,[]).append(i)
        con([(nq+i,1),(i,-1)],h=0)
    for j,y in enumerate(T):
        ty=2*nq+j;buckets.setdefault(sum(P[i] for i in y)%m,[]).append(ty)
        for z in {y[:a]+y[a+1:] for a in range(3)}:
            i=qi[z];incidence[i].append(ty)
            con([(ty,1),(nq+i,-1)],h=0)
    for i,inc in enumerate(incidence):
        con([(nq+i,1),*[(j,-1) for j in inc]],h=0)
    for ids in buckets.values():con([(i,1) for i in ids],h=1)
    for i in range(k):con([(j,1) for j,z in enumerate(Q) if i in z],l=1)
    con([*[(i,1) for i in range(nq)],*[(2*nq+j,1) for j in range(nt)]],l=L,h=L)
    R0=(-sigma)%m; U=[(v-sigma)%m for v in P]
    rz=[(sum(P[i] for i in z)-sigma)%m for z in Q]
    ry=[(sum(P[i] for i in y)-sigma)%m for y in T]
    plus=[int((sum(U[i] for i in z)-R0-rz[j])//m==1) for j,z in enumerate(Q)]
    c=np.array([-rz[i]-m*plus[i] for i in range(nq)]+
               [(d+2)*rz[i]+m*plus[i] for i in range(nq)]+[-2*v for v in ry],dtype=float)
    mat=coo_matrix((data,(rows,cols)),shape=(len(lo),nv)).tocsc()
    res=milp(c,integrality=np.ones(nv),bounds=Bounds(np.zeros(nv),np.ones(nv)),
             constraints=LinearConstraint(mat,np.array(lo),np.array(hi)),
             options=dict(time_limit=1.5,mip_rel_gap=0,threads=1))
    stats['calls']+=1;stats['status_'+str(res.status)]+=1
    if res.x is None:return
    x=np.rint(res.x).astype(int)
    if max(abs(res.x-x))>1e-5:return
    Qs={z for j,z in enumerate(Q) if x[j]};Ts={y for j,y in enumerate(T) if x[2*nq+j]}
    C={(),*[(i,) for i in range(k)],*Qs,*Ts}
    assert len(C)==m-d+k
    assert len({sum(P[i] for i in y)%m for y in C})==len(C)
    assert all(all(y[:j]+y[j+1:] in Qs for j in range(3)) for y in Ts)
    assert all(any(i in z for z in Qs) for i in range(k))
    Ns={z for z in Qs if any(tuple(sorted(z+(i,))) in Ts for i in range(k))}
    assert {z for j,z in enumerate(Q) if x[nq+j]}==Ns
    lab={y:sum(P[i] for i in y)%m for y in C}
    # Validate every phase, not only the optimized one.
    mnS=None;mnHC=None
    for sig in range(m):
        rr={y:(v-sig)%m for y,v in lab.items()};rho0=rr[()]
        S=(d+1)*(rho0+sum(rr[(i,)] for i in range(k))+sum(rr[z] for z in Ns))-sum(rr[z] for z in Qs-Ns)-2*sum(rr[y] for y in Ts)
        pos=sum((sum(rr[(i,)] for i in z)-rho0-rr[z])//m==1 for z in Qs-Ns)
        hc=S-m*pos
        if mnS is None or S<mnS[0]:mnS=(S,sig)
        if mnHC is None or hc<mnHC[0]:mnHC=(hc,sig,S,pos)
        stats['phases']+=1
        if S<0:
            out=dict(P=P,m=m,d=d,sigma=sig,S=S,C=sorted(C))
            Path('MAXCL_COUNTEREXAMPLE.json').write_text(json.dumps(out,indent=2)+'\n')
            print('MAXCL_COUNTEREXAMPLE',out,flush=True);raise SystemExit(2)
    witness=dict(P=P,m=m,d=d,k=k,C=sorted(C),minS=mnS,minHCprime=mnHC,
                 q=len(Qs),p=len(Ns),t=len(Ts),optimized_phase=sigma,status=int(res.status))
    stats['tiles']+=1
    if best is None or mnHC[0]<best['minHCprime'][0]:
        best=witness
        print('BEST',json.dumps(best,sort_keys=True),flush=True)
    if mnHC[0]<0:
        witnesses.append(witness)
        Path('HCprime_COUNTEREXAMPLES.json').write_text(json.dumps(witnesses,indent=2)+'\n')
        print('HCprime_COUNTEREXAMPLE',json.dumps(witness,sort_keys=True),flush=True)
        # A refutation of HC' suffices to guide the next theoretical step.
        return True

trials=int(sys.argv[1]) if len(sys.argv)>1 else 160
for tr in range(trials):
    k=rng.choice((5,6,7,8,9,10,12));m=rng.randint(3*k,max(3*k+1,2*k*k))
    d=k+rng.randint(0,min(k,m-k-1))
    P=sorted(rng.sample(range(1,m),k))
    phase=rng.choice([0,1,m-1,*P,rng.randrange(m)])
    found=solve(P,m,d,phase)
    if found:break
    if tr%10==0:print('PROGRESS',tr,dict(stats),flush=True)
out=dict(seed=2026101933,trials=tr+1,stats=dict(stats),best=best,HCprime_counterexamples=witnesses)
Path('milp_hc.json').write_text(json.dumps(out,indent=2)+'\n')
print('DONE',json.dumps({k:v for k,v in out.items() if k not in ('best','HCprime_counterexamples')},sort_keys=True),flush=True)
