"""Explicit face and zero-extension matchings; all executions on fejer."""
import json,random,sys
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'d'))
from core import evaluate
from payments import cubic_data
from origin_probe import make
from verify import STRESS


def match(F,allowed):
    own={}
    def augment(y,seen):
        for z in sorted({y[:i]+y[i+1:] for i in range(3)}&allowed):
            if z in seen:continue
            seen.add(z)
            if z not in own or augment(own[z],seen):
                own[z]=y;return True
        return False
    for y in sorted(F):augment(y,set())
    return own


def run(m,P,Q,T,stats,examples):
    for zero in range(len(P)):
        sig=P[zero];rho=(-sig)%m;U=[(u-sig)%m for u in P]
        a=evaluate(m,U,Q,T,rho)
        kp,kt,rt,bad,gain,types=cubic_data(m,U,Q,T,rho)
        Af={y for y in bad if kt[y]==1};Df=set(bad)-Af
        faces={y[:i]+y[i+1:] for y in T for i in range(3)}
        Afac={z for z in faces if kp[z]==1}
        Dfac={y[:i]+y[i+1:] for y in Df for i in range(3)}
        Z={z for z in Dfac if tuple(sorted(z+(zero,))) in T}
        am=match(Af,Afac);dm=match(Df,Z);full=match(Df,Dfac)
        stats['unit_zero_phases']+=1
        stats['positive_bad']+=len(Af);stats['deep_bad']+=len(Df)
        if len(am)==len(Af) and len(dm)==len(Df):
            assert a['HC']>=a['Lplus']+m*a['Orest']
            stats['complete_relay']+=1
            stats['complete_relay_with_deep']+=bool(Df)
        if len(am)==len(Af) and len(full)==len(Df):
            F=set(full)-Z
            psi=Counter(y[:i]+y[i+1:] for y in T for i in range(3))
            rp={z:(sum(U[i] for i in z)-rho)%m for z in faces}
            coeff={z:a['d']+2-psi[z] for z in faces}
            assert all(coeff[z]>=a['s']+1 for z in F)
            LF=a['Lplus']-sum(rp[z] for z in F)
            cost=sum(m-rp[z] for z in F)
            assert LF>=0 and a['HC']>=LF+m*a['Orest']-cost
            weights=[a['s']+d for d in a['delta']]+[c-int(z in F) for z,c in coeff.items()]
            rank=sum(i*c for i,c in enumerate(sorted(weights,reverse=True)))
            assert LF>=rank
            stats['weighted_relay']+=1
            if rank+m*a['Orest']>=cost:
                assert a['HC']>=0;stats['weighted_rank_paid']+=1
        if Df and len(full)<len(Df) and len(examples)<4:
            examples.append(dict(m=m,P=P,Q=sorted(Q),T=sorted(T),sig=sig,
                                 betaD=len(Df),deep_face_matching=len(full),
                                 zero_extension_matching=len(dm),HC=a['HC'],S=a['S']))


if __name__=='__main__':
    rng=random.Random(2026101975);stats=Counter();examples=[]
    for m,P,cells in STRESS:
        C=[tuple(i for i,ch in enumerate(st) for _ in range(int(ch))) for st in cells.split()]
        run(m,P,{z for z in C if len(z)==2},{z for z in C if len(z)==3},stats,examples)
    for _ in range(1200):
        m=rng.randint(12,130);k=rng.randint(2,min(12,m-1));P=sorted(rng.sample(range(1,m),k))
        made=make(rng,m,P,True)
        if made is not None:
            P,Q,T=made;run(m,P,Q,T,stats,examples)
    print(json.dumps(dict(seed=2026101975,stats=stats,shadow_excess_examples=examples),indent=2),flush=True)
