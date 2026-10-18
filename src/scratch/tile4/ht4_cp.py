#!/usr/bin/env python3
"""Small adversarial CP-SAT search; only exact weight witnesses are accepted."""
import sys
sys.dont_write_bytecode=True
import argparse
import itertools
import json
import math
from pathlib import Path
import socket
import subprocess
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
from ortools.sat.python import cp_model
import enumerate as e
from ht4_tasks import reference

HERE=Path(__file__).resolve().parent


def grid(N):
    return [x for x in itertools.product(range(N+1),repeat=4) if sum(x)<=N]


def work(m,b,seconds,sample=None):
    r=tuple(sample['r']) if sample else tuple(pow(b,k,m) for k in range(4))
    assert len(set(r))==4 and 0 not in r
    initial=(frozenset(map(tuple,sample['tile'])) if sample else e.tile_for_weight(m,r,(1,1,1,1)))
    if sample:assert reference(initial)[0]==sample['H']
    N=max(map(sum,initial))+1
    points=grid(N);index={x:i for i,x in enumerate(points)}
    if len(points)>3000:return dict(m=m,r=r,status='skipped: grid above 3000 points',N=N)
    model=cp_model.CpModel();chosen=[model.new_bool_var(f'x{i}') for i in range(len(points))]
    height=[model.new_int_var(0,N,f'h{i}') for i in range(len(points))]
    tops=[[model.new_int_var(0,N,f't{i}_{a}') for a in range(4)] for i in range(len(points))]
    classes=[[] for _ in range(m)]
    for i,x in enumerate(points):classes[sum(a*b for a,b in zip(r,x))%m].append(chosen[i])
    if any(not c for c in classes):return dict(m=m,r=r,status='uncovered residue',N=N)
    for c in classes:model.add(sum(c)==1)
    for a in range(4):model.add(chosen[index[tuple(int(i==a) for i in range(4))]]==1)
    for i,x in enumerate(points):
        model.add_hint(chosen[i],int(x in initial));candidates=[0]
        for a in range(4):
            y=x[:a]+(x[a]+1,)+x[a+1:];j=index.get(y)
            model.add(tops[i][a]==0).only_enforce_if(chosen[i].Not())
            if j is None:
                model.add(tops[i][a]==height[i]).only_enforce_if(chosen[i])
            else:
                model.add(chosen[j]<=chosen[i])
                c=model.new_int_var(0,N,f'c{i}_{a}')
                model.add(c==height[j]+1).only_enforce_if(chosen[j])
                model.add(c==0).only_enforce_if(chosen[j].Not());candidates.append(c)
                model.add(tops[i][a]==tops[j][a]).only_enforce_if(chosen[j])
                model.add(tops[i][a]==height[i]).only_enforce_if([chosen[i],chosen[j].Not()])
        model.add_max_equality(height[i],candidates)
    model.minimize(sum(t for row in tops for t in row))
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=seconds
    solver.parameters.num_search_workers=1;solver.parameters.random_seed=20261018
    status=solver.solve(model)
    D=(frozenset(x for i,x in enumerate(points) if solver.value(chosen[i]))
       if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else initial)
    e.check_tile(m,r,D);H,R,t,hcr,non_two=reference(D)
    cons=e.cone_constraints(m,r,D)
    lp=linprog(np.zeros(4),A_ub=-np.array(cons,dtype=float),b_ub=-np.ones(len(cons)),bounds=[(1,None)]*4,method='highs')
    witness=None
    if lp.success:
        q=[F(str(v)).limit_denominator(10**6) for v in lp.x];den=math.lcm(*(v.denominator for v in q))
        p=tuple(int(v*den) for v in q)
        if min(p)>0 and all(e.dot(v,p)>0 for v in cons):
            assert e.tile_for_weight(m,r,p)==D;witness=p
    result=dict(m=m,r=r,N=N,grid_cells=len(points),solver_status=solver.status_name(status),
                seconds=solver.wall_time,H=H,H_over_m=str(F(H,m)),t=t,R=R,HCR=str(hcr),
                non_two_face=non_two,initial_H=reference(initial)[0],
                exact_positive_weight_witness=witness,realizable_certified=witness is not None,
                tile=e.tile_record(D),interpretation='Finite search only. LP failure is not an infeasibility certificate; no infinite-family claim.')
    result['construction']='lowest H among 10000 sampled minimum-degree tiles' if sample else 'geometric residue basis'
    (HERE/f'ht4_cp_{m}_{"sample" if sample else b}.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    assert socket.gethostname().split('.')[0]=='fejer'
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=60);args=p.parse_args()
    for m,b in ((50,3),(61,4),(80,3),(101,4)):
        result=work(m,b,args.seconds);print(json.dumps(result),flush=True)
    for m in (50,100,150,200):
        path=HERE/f'ht4_sample_{m}.json'
        with path.open('w') as out:
            subprocess.run([str(HERE/'ht4_scan'),'--sample',str(m),'10000',str(20261018+m)],stdout=out,check=True)
        sample=json.loads(path.read_text())['metrics']['min_H_tiles'][0]
        result=work(m,0,args.seconds,sample);print(json.dumps(result),flush=True)


if __name__=='__main__':main()
