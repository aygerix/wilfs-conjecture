"""Two exact evaluations of the rejected global mass shortcut (fejer only)."""
import json
from pathlib import Path
from audit import evaluate


def main():
    m=20;P=[12,3,5,9,19];sigma=18;rho=2
    ss='20000 11000 10100 10010 10001 02000 01100 01001 00110 00020 30000 20010 10020 00030'.split()
    cells=[tuple(i for i,ch in enumerate(st) for _ in range(int(ch))) for st in ss]
    Q={z for z in cells if len(z)==2};T={z for z in cells if len(z)==3}
    data=evaluate(m,P,Q,T,rho)
    # Independently enumerate all cells and test upper covers directly.
    D={(0,)*5}
    for a in range(5):D.add(tuple(int(a==b) for b in range(5)))
    D.update(tuple(st.count(i) for i in range(5)) for st in Q|T)
    label={x:sum(a*p for a,p in zip(x,P))%m for x in D}
    assert len(D)==m and set(label.values())==set(range(m))
    residue={x:(a-sigma)%m for x,a in label.items()}
    maximal=[]
    for x in D:
        if all(tuple(x[b]+int(a==b) for b in range(5)) not in D for a in range(5)):
            maximal.append(x)
    original=6*m*(m-1)//2-sum((5+sum(x))*residue[x] for x in maximal)
    assert original==data['S']==99 and data['HC']==99 and data['L']==79
    assert data['beta']==3
    out=dict(status='COUNTEREXAMPLE TO GLOBAL LPLUS >= mt; NOT TO MAXCL',
             m=m,P=P,Q=sorted(Q),T=sorted(T),sigma=sigma,rho=rho,
             exact=data,original_MaxCL_slack=original,
             all_phase_minimum=min(evaluate(m,P,Q,T,r)['S'] for r in range(m)))
    small=evaluate(6,[2,3],{(0,0),(0,1)},{(0,0,1)},2)
    assert small['pairmass']==2 and small['naive_pair_slack']==-1
    multi=evaluate(7,[5,3],{(0,1),(1,1)},{(0,1,1),(1,1,1)},6)
    assert multi['pairmass']==0 and multi['naive_pair_slack']==-3
    out['minimum_omitted_excess_counter']=dict(m=6,P=[2,3],Q=[[0,0],[0,1]],
                                             T=[[0,0,1]],rho=2,exact=small)
    out['minimum_t_ge_2_omitted_excess_counter']=dict(m=7,P=[5,3],Q=[[0,1],[1,1]],
                                                    T=[[0,1,1],[1,1,1]],rho=6,exact=multi)
    Path('results').mkdir(exist_ok=True)
    Path('results/mass_witness.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2),flush=True)


if __name__=='__main__':main()
