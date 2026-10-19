"""Exhaustive modular audit of symmetric rectangle packing (fejer only).

For each unit set, enumerate every maximal residue-injective quadratic
selection. Every other selection is obtained by deleting pairs, which
decreases the proposed lower bound, so those selections are covered too.
"""
import argparse,json
from itertools import combinations,combinations_with_replacement as cwr
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--max-m',type=int,default=16)
    ap.add_argument('--max-k',type=int,default=5)
    ap.add_argument('--output',default='results/pack_check.json')
    args=ap.parse_args();sets=leaves=0;minslack=None;by=[]
    for m in range(3,args.max_m+1):
        ms=ml=0
        for k in range(2,min(args.max_k,m-1)+1):
            for P in combinations(range(1,m),k):
                sets+=1;ms+=1;used={0,*P};fs={}
                for z in cwr(range(k),2):
                    r=(P[z[0]]+P[z[1]])%m
                    if r not in used:fs.setdefault(r,[]).append(z)
                fibres=list(fs.values());q=len(fibres);e=k*(k+1)//2-q
                degree=[0]*k
                def dfs(j):
                    nonlocal leaves,ml,minslack
                    if j<len(fibres):
                        for a,b in fibres[j]:
                            degree[a]+=1;degree[b]+=1;dfs(j+1);degree[a]-=1;degree[b]-=1
                        return
                    leaves+=1;ml+=1
                    bad=[i for i in range(k) if degree[i]!=k+1];v=len(bad)
                    G=[0]+[P[i] for i in range(k) if degree[i]==k+1]
                    AA=[0,*P]
                    DD={(a-b)%m for a in G for b in AA if a!=b}
                    assert len(DD)==len(G)*k
                    inter=DD&{(-z)%m for z in DD}
                    assert len(inter)<=len(G)*(len(G)-1)+4*e
                    lb=k*(k+1)+1-v*(v-1)-4*e
                    slack=m-lb;assert slack>=0
                    if minslack is None or slack<minslack['slack']:
                        minslack=dict(slack=slack,m=m,P=P,v=v,e=e)
                dfs(0)
        by.append(dict(m=m,unit_sets=ms,maximal_quadratic_selections=ml))
        print('progress',m,ms,ml,flush=True)
    out=dict(status='FINITE EXHAUSTIVE MODULAR AUDIT',max_m=args.max_m,max_k=args.max_k,
             unit_sets=sets,maximal_quadratic_selections=leaves,min_slack=minslack,by_modulus=by)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print('DONE',json.dumps({k:v for k,v in out.items() if k!='by_modulus'}),flush=True)


if __name__=='__main__':main()
