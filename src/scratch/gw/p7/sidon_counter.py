r"""Exact structured adversary: all pairs and one cubic for each distinct 3-sum.

For a positive integer Sidon set A in [1,L], choose even m=6L+2 and
P_a=m/2-A_a.  The core consists of 0, all units, all pairs, and one cubic
per element of 3A\A.  Complete by spikes.  At theta=m-2L, H1' slack is
2L+binom(k+1,2)-|3A\A|.  This script checks every claim using integers.
"""
import argparse
import itertools
import json


def prime(n):
    return n>=2 and all(n%d for d in range(2,int(n**0.5)+1))


def analyze(A, keep=False):
    A=tuple(sorted(A))
    k=len(A)
    L=max(A)
    pairs={}
    for i,j in itertools.combinations_with_replacement(range(k),2):
        s=A[i]+A[j]
        assert s not in pairs, (A,pairs[s],(i,j))
        pairs[s]=(i,j)
    triples={}
    aset=set(A)
    for i,j,l in itertools.combinations_with_replacement(range(k),3):
        s=A[i]+A[j]+A[l]
        if s not in aset and s not in triples:
            triples[s]=(i,j,l)
    q=3*L+1
    m=2*q
    P=tuple(q-a for a in A)
    theta=m-2*L
    Q=k*(k+1)//2
    slack=2*L+Q-len(triples)
    # Disjoint label bands; only the unit/cubic collisions need explicit deletion.
    labels={0}
    labels.update(P)
    assert len(labels)==k+1
    for s in pairs:
        assert m-s not in labels
        labels.add(m-s)
    for s in triples:
        assert 0<q-s<theta and q-s not in labels
        labels.add(q-s)
    n=1+k+Q+len(triples)
    assert n==len(labels)<=m
    high=[z for z in labels if z>=theta]
    assert len(high)==Q
    assert min(P)>0 and max(P)<theta
    assert all(theta<=m-s<m for s in pairs)
    assert slack==2*Q-len(triples)+(m-theta-Q)
    ans=dict(A=A,k=k,L=L,m=m,P=P,theta=theta,rho=2*L,Q=Q,
             triples=len(triples),core_cells=n,spikes=m-n,
             high_spikes=2*L-Q,H1_slack=slack,
             max_pair=m-min(pairs),min_cubic=m+q-max(triples),
             max_cubic=m+q-min(triples))
    if keep:
        ans['triple_indices']=list(triples.values())
        ans['spike_labels']=[z for z in range(1,m) if z not in labels]
    return ans


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pmax',type=int,default=103)
    ap.add_argument('--out',default='results/sidon_counter.json')
    args=ap.parse_args()
    first=None
    for p in range(3,args.pmax+1,2):
        if not prime(p):continue
        A=[1+2*p*i+(i*i%p) for i in range(p)]
        z=analyze(A)
        print(json.dumps(z),flush=True)
        if z['H1_slack']<0 and first is None:
            first=analyze(A,keep=True)
            with open(args.out,'w') as f:json.dump(first,f)
            print('NEGATIVE',p,flush=True)
            break
    print('DONE first', first['k'] if first else None,flush=True)


if __name__=='__main__':main()
