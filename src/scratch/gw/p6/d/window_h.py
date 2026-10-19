"""Exact all-height window identity and discriminating actual-core checks.

All executions on fejer. Integer arithmetic only. No sampled run is a proof.
"""
import argparse,json,random
from collections import Counter
from itertools import combinations_with_replacement as cwr
from math import comb
from core import evaluate as eval3


def faces(y):return {y[:j]+y[j+1:] for j in range(len(y))}


def check(C,P,m,stats,minima):
    C=set(C); k=len(P); H=max(map(len,C)); s=m-len(C); d=k+s
    assert () in C and s>=0
    assert all(faces(y)<=C for y in C if y)
    N={z for z in C if any(tuple(sorted(z+(i,))) in C for i in range(k))}
    assert all((i,) in N for i in range(k))
    lab={z:sum(P[i] for i in z)%m for z in C}
    assert len(set(lab.values()))==len(C)
    Q={z for z in C if len(z)==2}; A2=Q-N; N2=Q&N
    deg=Counter(i for z in Q for i in z)
    delta=[k+1-deg[i] for i in range(k)]
    psi={z:sum(z.count(i)+1 for i in range(k) if tuple(sorted(z+(i,))) in C)
         for z in N if len(z)>=2}
    assert all(v<=k+len(z) for z,v in psi.items())
    for sig in range(m):
        R={z:(a-sig)%m for z,a in lab.items()}; rho=R[()]
        K={z:(sum(R[(i,)] for i in z)-(len(z)-1)*rho-R[z])//m for z in C if len(z)>=2}
        S=(d+1)*sum(R[z] for z in N)-sum((len(z)-1)*R[z] for z in C-N)
        PAplus=sum(K[z]==1 for z in A2)
        HC=S-m*PAplus
        L=sum((s+delta[i])*R[(i,)] for i in range(k))
        L+=sum((d+len(z)-psi[z])*R[z] for z in N if len(z)>=2)
        OW=rho-sum(K[z]==-1 for z in A2)
        Pminus=sum(K[z]==-1 for z in N2)
        Pplus=sum(K[z]==1 for z in N2)
        high={z for z in C if len(z)>=3}
        V=sum(R[z]>=m-rho for z in high)
        orest=OW-Pminus-V
        assert orest>=0
        bs=[]
        for y in high:
            h=len(y)
            kap=(h-1)*K[y]-sum(K[y[:j]+y[j+1:]] for j in range(h))
            assert m*kap==sum(R[y[:j]+y[j+1:]] for j in range(h))-(h-1)*R[y]-rho
            v=int(R[y]>=m-rho); b=kap+v; bs.append(b)
            assert b>=-(h-2)
            if rho==0: assert b>=-(h-2)
        assert HC==L+m*(orest+Pplus+sum(bs))
        assert L>=0
        if H<=3:
            ans=eval3(m,[R[(i,)] for i in range(k)],Q,high,rho)
            assert HC==ans['HC']
            if ans['t']==1 and ans['OW']+ans['B']<0 and s>=1 and k>=5:
                assert ans['Lplus']>=m
                stats['ONE_SPIKE']+=1
            # Origin narrow cluster: all shape degrees arbitrary.
            if rho==0 and k and 2*min(P)>m and 3*max(P)<2*m:
                assert Pplus==len(N2) and all(b==-1 for b in bs)
                assert 2*len(high)<=k*s+2*(comb(k+1,2)-len(Q))+2*len(N2)
                assert HC>=0
                stats['BAD_NARROW']+=1
        if S<0:
            print('STOP MaxCL counterexample',dict(m=m,P=P,C=sorted(C),sig=sig,S=S,HC=HC),flush=True)
            raise SystemExit(2)
        key='H'+str(H)
        if key not in minima or HC<minima[key]['HC']:
            minima[key]=dict(HC=HC,S=S,m=m,P=P,C=sorted(C),sig=sig)
        stats['phases']+=1;stats['height_'+str(H)]+=1
    stats['cores']+=1


def random_core(rng,m,P,H):
    k=len(P);C={()}|{(i,) for i in range(k)};used={0,*P}
    for h in range(2,H+1):
        candidates=list(cwr(range(k),h));rng.shuffle(candidates)
        prob=rng.uniform(.2,1)
        for y in candidates:
            if not faces(y)<=C:continue
            v=sum(P[i] for i in y)%m
            if v in used or rng.random()>prob:continue
            C.add(y);used.add(v)
    active=sorted({i for z in C if len(z)==2 for i in z})
    if not active:return None
    ren={i:j for j,i in enumerate(active)}
    C={tuple(ren[i] for i in z) for z in C if all(i in ren for i in z)}
    return C,[P[i] for i in active]


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=2000)
    ap.add_argument('--seed',type=int,default=2026101964);ap.add_argument('--output',default='window_h.json')
    args=ap.parse_args();rng=random.Random(args.seed);stats=Counter();minima={}
    # Mandatory E47/E51, represented by full binary height-three cores.
    for P in ([5,6],[8,9]):
        C={z for h in range(4) for z in cwr(range(2),h)}
        check(C,P,14,stats,minima)
    # A smallest local quartic counterexample to one-m-per-top-cell.
    C={tuple([0]*h) for h in range(5)}
    check(C,[5],7,stats,minima)
    print('quartic origin: m=7, P=5; K3=2, K4=2, kappa4=-2, S=HC=18',flush=True)
    for step in range(args.trials):
        m=rng.randrange(10,151);k=rng.randrange(2,min(12,m-1)+1);H=rng.choice([3,3,4,5])
        if step%3==0:
            pool=list(range(m//2+1,(2*m-1)//3+1))
            if len(pool)<2:continue
            k=min(k,len(pool));P=sorted(rng.sample(pool,k));H=3
        else:P=sorted(rng.sample(range(1,m),k))
        made=random_core(rng,m,P,H)
        if made is None:continue
        C,P=made
        check(C,P,m,stats,minima)
    out=dict(seed=args.seed,trials=args.trials,stats=stats,minima=minima)
    print('DONE',json.dumps(out,sort_keys=True),flush=True)
    with open(args.output,'w') as f:json.dump(out,f,indent=2)
