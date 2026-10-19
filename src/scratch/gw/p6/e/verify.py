"""Exact actual-core audit of P6e. All execution belongs on fejer."""
import argparse,json,random,sys
from collections import Counter
from itertools import combinations_with_replacement as cwr
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'d'))
from core import evaluate
from payments import cubic_data, origin, defect
from origin_probe import make

STRESS = [
(20,[12,13,17,1,15],'20000 11000 10100 10001 02000 01001 00200 00110 00020 00011 00002 00300'),
(28,[8,2,27,11,9,3,12],'2000000 1100000 1010000 1001000 1000100 1000001 0200000 0110000 0101000 0100010 0100001 0020000 0002000 0001001 0000200 0000101 0000020 0000011 0000002 0030000'),
(22,[6,2,9,4,21,8],'200000 101000 100010 100001 011000 010010 010001 002000 001100 001001 000110 000020 000011 000002 000030'),
(22,[3,21,8,5,9],'20000 11000 10100 10001 02000 01100 01010 00200 00110 00101 00020 00011 00002 12000 03000'),
(26,[25,5,10,7,11,3],'200000 110000 101000 100100 100001 011000 010100 010010 010001 002000 001100 001010 001001 000110 000020 000011 300000 200001'),
(26,[3,6,17,14,7,1],'110000 101000 100010 100001 020000 011000 010010 002000 001100 001010 001001 000200 000110 000101 003000 002100 001200 000300'),
(38,[11,25,28,16,17,13,10],'2000000 1100000 1010000 1001000 1000010 1000001 0200000 0110000 0100100 0100001 0020000 0011000 0010100 0010010 0002000 0001100 0001010 0000200 0000110 0000020 0000011 0000002 0300000 0210000 0120000 0030000'),
(30,[29,26,7,6,25,4],'200000 100100 100010 100001 020000 010100 010010 002000 001100 001001 000200 000110 000101 000020 000002 300000 200010 100020 030000 020010 010020 000030')]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trials',type=int,default=2500)
    ap.add_argument('--seed',type=int,default=2026101973)
    ap.add_argument('--output',default='verify.json')
    args=ap.parse_args(); rng=random.Random(args.seed);stats=Counter();mins={};stress=[]
    def check(m,P,Q,T,allphase=True):
        local=[]
        for sig in range(m) if allphase else [0]:
            U=[(u-sig)%m for u in P];rho=(-sig)%m
            a=evaluate(m,U,Q,T,rho)
            kp,kt,rt,bad,gain,types=cubic_data(m,U,Q,T,rho)
            stats.update({'bad_'+key:value for key,value in types.items()})
            assert types['D']<=rho//2
            assert types['A']<=(m-rho)//2
            assert all((m-rho+1)//2<=rt[y]<m-rho for y in bad if kt[y]==1)
            assert all(m-rho//2<=rt[y]<m for y in bad if kt[y]==-1)
            if types['D']==0 and types['A']<=3:
                assert a['HC']>=0
                stats['NO-DEEP-THREE']+=1
            v=defect(m,U,Q,a)
            for y in bad:
                if kt[y]==-1:
                    r=min(sum(U[i] for i in z)-rho for z in {y[:j]+y[j+1:] for j in range(3)})
                    assert rho>=3*r+2
                    assert all(2*r+1<=U[i]<=rho-r-1 for i in y)
                    stats['DEEP-HOLES']+=1
            if 0 in U:
                a0=U.index(0)
                Dfaces={y[:j]+y[j+1:] for y in bad if kt[y]==-1 for j in range(3)}
                for z in Dfaces:
                    w=tuple(sorted(z+(a0,)))
                    if w not in T:continue
                    kap=2*kt[w]-sum(kp[w[:j]+w[j+1:]] for j in range(3))
                    assert kap+int(rt[w]>=m-rho)==1
                    stats['ZERO-DEEP-GAIN']+=1
                Afaces={y[:j]+y[j+1:] for y in bad if kt[y]==1 for j in range(3)}
                for z in Afaces:
                    w=tuple(sorted(z+(a0,)))
                    if w not in T:continue
                    kap=2*kt[w]-sum(kp[w[:j]+w[j+1:]] for j in range(3))
                    b=kap+int(rt[w]>=m-rho)
                    rz=(sum(U[i] for i in z)-rho)%m
                    assert b==int(rz>=rho)
                    stats['ZERO-POSITIVE-FORMULA']+=1
            if rho==0:
                o=origin(m,U,Q,T,a)
                stats['origins']+=1
                stats['at_most_one_low']+=o['l']<=1
                stats['at_most_one_high']+=o['H']<=1
                stats['origin_beta_le_3']+=a['beta']<=3
                stats['bimodal']+=all(4*u<=m or 2*u>m for u in U)
                if o['l']==0:
                    stats['all_high']+=1
                if o['l']==1:
                    stats['one_low']+=1
            assert a['S']>=0
            stats['phases']+=1
            for key in ['HC','S']:
                if key not in mins or a[key]<mins[key]['value']:
                    mins[key]=dict(value=a[key],m=m,P=P,Q=sorted(Q),T=sorted(T),sig=sig)
            local.append(a['S'])
        stats['cores']+=1
        return min(local)
    for m,P,cells in STRESS:
        C=[tuple(i for i,ch in enumerate(st) for _ in range(int(ch))) for st in cells.split()]
        Q={z for z in C if len(z)==2};T={z for z in C if len(z)==3}
        stress.append(dict(m=m,minS=check(m,P,Q,T)))
    for P in [[5,6],[8,9]]:
        check(14,P,set(cwr(range(2),2)),set(cwr(range(2),3)))
    for step in range(args.trials):
        m=rng.randint(10,130);k=rng.randint(2,min(12,m-1))
        mode=step%6
        if mode==0:
            pool=range(m//2+1,m);k=min(k,len(pool));P=sorted(rng.sample(pool,k))
        elif mode==1:
            pool=range(m//2+1,m);k=min(k,len(pool)+1)
            P=sorted(rng.sample(pool,k-1)+[rng.randint(1,m//2)])
        elif mode==2:
            lo=range(1,m//4+1);hi=range(m//2+1,m)
            nl=min(rng.randint(1,3),len(lo),k-1);nh=min(k-nl,len(hi))
            P=sorted(rng.sample(lo,nl)+rng.sample(hi,nh))
        elif mode==3:
            P=sorted(rng.sample(range(1,m//2+1),k-1)+[rng.randint(m//2+1,m-1)]) if k<=m//2+1 else sorted(rng.sample(range(1,m),k))
        else:
            P=sorted(rng.sample(range(1,m),k))
        made=make(rng,m,P,True)
        if made is None:continue
        P,Q,T=made
        check(m,P,Q,T)
    out=dict(seed=args.seed,trials=args.trials,stats=stats,minima=mins,stress=stress)
    Path(args.output).write_text(json.dumps(out,indent=2))
    print('DONE',json.dumps(out),flush=True)


if __name__=='__main__':main()
