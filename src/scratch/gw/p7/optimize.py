"""LP/MILP adversary for fixed canonical residues, with optional spike completion.

All allowed monomials have every immediate divisor of weight <m.  Variables
select a downset; residue rows impose completeness, or at most one core cell
per residue (the latter is completed by spikes).  The shadow objective is
linear via FIRST-ID, independently checked on every integral output.

Usage: python optimize.py --seed 71 --trials 100 --mmax 100 --kmax 8 --spikes
"""
import argparse
import itertools
import json
import random
import time
import numpy as np
from scipy.optimize import milp, linprog, Bounds, LinearConstraint
from scipy.sparse import coo_matrix, vstack
from core import evaluate, brief, add, sub


def pool(m, P, cap):
    k = len(P)
    D = {(0,)*k}
    work = [(0,)*k]
    for x in work:
        if sum(a*b for a,b in zip(x,P)) >= m:
            continue
        for a in range(k):
            y = add(x,a)
            if y in D:
                continue
            vy = sum(c*p for c,p in zip(y,P))
            if any(vy-P[b] >= m for b in range(k) if y[b]):
                continue
            D.add(y)
            work.append(y)
            if len(D) > cap:
                return None
    return sorted(D, key=lambda x:(sum(x),x))


def system(m, P, cells, spikes, active):
    k = len(P)
    n = len(cells)
    ix = {x:j for j,x in enumerate(cells)}
    v = [sum(a*b for a,b in zip(x,P)) for x in cells]
    rr,cc,dd = [],[],[]
    for j,x in enumerate(cells):
        rr.append(v[j]%m);cc.append(j);dd.append(1)
    labels = coo_matrix((dd,(rr,cc)),shape=(m,n)).tocsr()
    rr,cc,dd = [],[],[]
    row = 0
    for j,x in enumerate(cells):
        for a in range(k):
            if not x[a]:
                continue
            rr.extend([row,row]);cc.extend([j,ix[sub(x,a)]]);dd.extend([1,-1]);row+=1
    order = coo_matrix((dd,(rr,cc)),shape=(row,n)).tocsr()
    lo = np.zeros(n)
    hi = np.ones(n)
    lo[0] = 1
    if active:
        for a in range(k):
            lo[ix[add((0,)*k,a)]] = 1
    return dict(v=v, labels=labels, order=order, lo=lo, hi=hi)


def costs(m,P,cells,v,theta,spikes):
    ans=[]
    for x,vx in zip(cells,v):
        b = sum(x[a] for a in range(len(P)) if vx>=theta and vx-P[a]<theta)
        c = b
        if vx>=m:
            c += sum(x)-1 if vx-m>=theta else -1
        if spikes and vx%m>=theta:
            c -= 1
        ans.append(c)
    return np.array(ans,dtype=float), (m-theta if spikes else 0)


def solve(m,P,cells,ss,theta,spikes,integer,limit):
    c,const = costs(m,P,cells,ss['v'],theta,spikes)
    n = len(cells)
    if integer:
        A=vstack([ss['labels'],ss['order']],format='csr')
        lb=np.concatenate([np.zeros(m) if spikes else np.ones(m),np.full(ss['order'].shape[0],-np.inf)])
        ub=np.concatenate([np.ones(m),np.zeros(ss['order'].shape[0])])
        res=milp(c,integrality=np.ones(n),bounds=Bounds(ss['lo'],ss['hi']),
                 constraints=LinearConstraint(A,lb,ub),options={'time_limit':limit,'threads':1})
    else:
        if spikes:
            res=linprog(c,A_ub=vstack([ss['labels'],ss['order']],format='csr'),
                        b_ub=np.concatenate([np.ones(m),np.zeros(ss['order'].shape[0])]),
                        bounds=list(zip(ss['lo'],ss['hi'])),method='highs',options={'threads':1})
        else:
            res=linprog(c,A_eq=ss['labels'],b_eq=np.ones(m),A_ub=ss['order'],
                        b_ub=np.zeros(ss['order'].shape[0]),bounds=list(zip(ss['lo'],ss['hi'])),method='highs',options={'threads':1})
    return res,const


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--seed',type=int,default=71)
    ap.add_argument('--trials',type=int,default=100)
    ap.add_argument('--mmax',type=int,default=100)
    ap.add_argument('--kmax',type=int,default=8)
    ap.add_argument('--cap',type=int,default=10000)
    ap.add_argument('--spikes',action='store_true')
    ap.add_argument('--integer',action='store_true')
    ap.add_argument('--limit',type=float,default=10)
    ap.add_argument('--phases',type=int,default=4)
    ap.add_argument('--out',default='results/optimize.jsonl')
    args=ap.parse_args()
    rng=random.Random(args.seed)
    stats=dict(attempted=0,pools=0,solved=0,infeasible=0,timeouts=0,negative=0,integral_negative=0)
    best=0
    with open(args.out,'w') as out:
        for tr in range(args.trials):
            m=rng.randint(10,args.mmax)
            k=rng.randint(2,min(args.kmax,m-1))
            low=min(m-k,rng.choice([1,max(1,m//8),max(1,m//5),max(1,m//3)]))
            P=tuple(sorted(rng.sample(range(low,m),k)))
            cells=pool(m,P,args.cap)
            stats['attempted']+=1
            if cells is None:
                continue
            stats['pools']+=1
            ss=system(m,P,cells,args.spikes,True)
            tt=set(rng.sample(range(1,m+1),min(args.phases,m)))|{min(P),min(P)+1}
            for theta in sorted(tt):
                res,const=solve(m,P,cells,ss,theta,args.spikes,args.integer,args.limit)
                if res.x is None:
                    stats['infeasible' if res.status==2 else 'timeouts']+=1
                    continue
                val=res.fun+const
                stats['solved']+=1
                if val < -1e-6:
                    stats['negative']+=1
                    rec=dict(m=m,P=P,theta=theta,value=val,integral=args.integer,
                             cells=[(x,float(xx)) for x,xx in zip(cells,res.x) if xx>1e-8])
                    if np.max(np.abs(res.x-np.rint(res.x)))<1e-6:
                        C=[x for x,xx in zip(cells,res.x) if xx>0.5]
                        if args.spikes:
                            labs={sum(a*b for a,b in zip(x,P))%m for x in C}
                            missing=[z for z in range(m) if z not in labs]
                            dim=k+len(missing)
                            DD=[x+(0,)*len(missing) for x in C]
                            for a,z in enumerate(missing):
                                y=[0]*dim;y[k+a]=1;DD.append(tuple(y))
                            PP=P+tuple(missing)
                        else:
                            DD=C;PP=P
                        ev=evaluate(m,PP,DD)
                        assert ev['wrapmax'] and ev['complete']
                        assert ev['rows'][theta-1]['shadow']==round(val)
                        rec['verified']=dict(**brief(ev),row=ev['rows'][theta-1])
                        stats['integral_negative']+=1
                    out.write(json.dumps(rec)+'\n');out.flush()
                    if val<best:
                        best=val
                        print(json.dumps(dict(trial=tr,newbest=val,m=m,P=P,theta=theta,pool=len(cells),stats=stats)),flush=True)
                    if 'verified' in rec:
                        print('COUNTEREXAMPLE',flush=True)
                        return
            if (tr+1)%10==0:
                print(json.dumps(dict(trial=tr+1,stats=stats,best=best)),flush=True)
    print(json.dumps(dict(done=True,stats=stats,best=best)),flush=True)


if __name__=='__main__':
    main()
