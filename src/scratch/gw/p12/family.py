"""Interval family <5k+2, 6k+3, ..., 7k+3>. Fejer only."""
import json,sys
from fractions import Fraction
from check import check

def formula(k):
    m=5*k+2
    A=[0]+list(range(6*k+3,7*k+4))+list(range(12*k+6,14*k+7))
    A+=list(range(19*k+9,20*k+8))+list(range(20*k+9,21*k+9))
    assert len(A)==m and len({x%m for x in A})==m
    N=[3*k+2+i-max(k-2*i,0)-(k//2<=i<k)-2*(i==k) for i in range(k+1)]
    rest=sum((6*k+3+i)*N[i] for i in range(k+1))-m*(k+1)*(4*k+3)
    aset=set(A)
    tops=[(6*k+3+i)*(3 if 3*(6*k+3+i) in aset else 2) for i in range(k+1)]
    con0=sum(tops)-4*m*(k+1)
    return dict(k=k,m=m,gens=[m]+list(range(6*k+3,7*k+4)),Ap=A,N=N,M=21*k+8,n1=6*k+3,
                ellp=4*k+3,REST=rest,con0=con0,Delta=rest+con0,C2=m*(m-1)//2,
                W=4*k*k-k+7)

def fit(xs,ys):
    a=[[Fraction(x)**j for j in range(len(xs))]+[Fraction(y)] for x,y in zip(xs,ys)]
    for i in range(len(xs)):
        q=a[i][i];a[i]=[x/q for x in a[i]]
        for j in range(len(xs)):
            if i!=j:
                q=a[j][i];a[j]=[u-q*v for u,v in zip(a[j],a[i])]
    return [a[i][-1] for i in range(len(xs))]

if __name__=='__main__':
    limit=int(sys.argv[1]) if len(sys.argv)>1 else 80
    for parity in (0,1):
        xs=[2*i+2+parity for i in range(4)]
        coef=fit(xs,[formula(k)['REST'] for k in xs])
        assert all(sum(coef[j]*k**j for j in range(4))==formula(k)['REST'] for k in range(1+parity,2001) if k%2==parity)
        print('REST polynomial parity',parity,':',list(map(str,coef)),flush=True)
    firstrest=None;firstchain=None
    for k in range(1,limit+1):
        f=formula(k);s=check(f['gens'])
        assert sorted(s['apery_by_residue'])==f['Ap']
        for key in ('M','n1','ellp','REST','con0','Delta','C2'):assert s[key]==f[key],(k,key,s[key],f[key])
        assert list(s['N'].values())==f['N']
        if f['REST']>0 and firstrest is None:firstrest=k
        if f['Delta']>f['C2'] and firstchain is None:
            firstchain=k
            with open('chain_counter.json','w') as out:json.dump(s,out,indent=2)
        print('CHECK',k,{key:f[key] for key in ('m','M','n1','REST','con0','Delta','C2','W')},flush=True)
    print('SUMMARY first positive REST',firstrest,'first CHAIN failure',firstchain,flush=True)
    print('DELTA_MINUS_C2_SHIFT_CERTIFICATES',flush=True)
    for k0 in range(17,23):
        coeff=fit(list(range(4)),[formula(k0+6*j)['Delta']-formula(k0+6*j)['C2'] for j in range(4)])
        for j in range(1001):
            k=k0+6*j;f=formula(k)
            assert sum(coeff[i]*j**i for i in range(4))==f['Delta']-f['C2']
        assert all(x>0 for x in coeff)
        print(k0,list(map(str,coeff)),flush=True)
